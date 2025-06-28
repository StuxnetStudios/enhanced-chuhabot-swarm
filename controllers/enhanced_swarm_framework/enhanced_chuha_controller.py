#!/usr/bin/env python3.6
"""
Enhanced ChuhaBot Controller - Integration Example
================================================

This controller demonstrates how to use the enhanced swarm framework
with the existing ChuhaBot system, providing more sophisticated behaviors
while maintaining compatibility with the original LIDAR-based detection.
"""

# Import the enhanced framework with proper error handling
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Handle Webots controller import with fallback
try:
    from controller import Robot, Motor, Lidar, Display, Keyboard
except ImportError:
    print("Warning: Webots controller not available. Using compatibility layer.")
    try:
        from webots_compat import Robot, Motor, Lidar, Display, Keyboard
    except ImportError:
        print("Error: Neither Webots controller nor compatibility layer found!")
        sys.exit(1)

# Import scientific computing libraries
try:
    import numpy as np
except ImportError:
    print("Error: NumPy is required but not installed!")
    print("Please run: pip install numpy")
    sys.exit(1)

# Import enhanced framework components
from enhanced_swarm_framework import (
    EnhancedSwarmController, SwarmAgent, BehaviorWeight, 
    BehaviorType, SeparationBehavior, FormationBehavior
)

# Import existing ChuhaBot functions with error handling
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'swarm_basic_flocking'))
    from swarm_basic_flocking import (
        Grapher, lidar_filter, get_theta_data_aligned, 
        get_theta_data_colored, get_neighbours
    )
    CHUHABOT_FUNCTIONS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Original ChuhaBot functions not available: {e}")
    print("Some features may be limited.")
    CHUHABOT_FUNCTIONS_AVAILABLE = False
    
    # Provide minimal fallback implementations
    class Grapher:
        def __init__(self, display): 
            self.display = display
        def clear(self): pass
        def drawPointCenter(self, x, y, size=5, color=0xFFFFFF): pass
    
    def get_theta_data_aligned(lidar, sizes, ranges, epsilon):
        return []
    
    def get_theta_data_colored(data, delta_theta, delta_r):
        return []
    
    def get_neighbours(data):
        return [], []

import math
import time
from typing import List, Tuple, Optional

class ChuhaEnhancedController:
    """Enhanced ChuhaBot controller with modular swarm behaviors and adaptive intelligence"""
    
    def __init__(self, robot):
        self.robot = robot
        self.robot_name = robot.getName()
        self.timestep = int(robot.getBasicTimeStep())
        
        # Initialize enhanced swarm controller
        self.swarm_controller = EnhancedSwarmController(self.robot_name)
        
        # Initialize hardware components
        self._initialize_hardware()
        
        # Mission state and intelligence
        self.mission_mode = "exploration"  # exploration, formation, following, patrol, search
        self.leader_id = None
        self.formation_type = "circle"  # circle, line, v_shape, diamond
        
        # Advanced tracking and memory
        self.step_count = 0
        self.last_neighbor_count = 0
        self.neighbor_history = []  # Track neighbor positions over time
        self.performance_metrics = {
            'distance_traveled': 0.0,
            'time_in_formation': 0.0,
            'collision_count': 0,
            'exploration_coverage': 0.0
        }
        
        # Adaptive behavior parameters
        self.learning_rate = 0.01
        self.adaptation_threshold = 0.8
        self.last_position = (0.0, 0.0)
        
        # Communication and coordination
        self.message_queue = []
        self.shared_map = {}  # Shared environmental knowledge
        
        print(f"🤖 Enhanced ChuhaBot '{self.robot_name}' initialized!")
        print(f"   Available features: Adaptive behaviors, Formation control, Learning")
        
    def _initialize_hardware(self):
        """Initialize all robot hardware components with enhanced capabilities"""
        try:
            # LIDAR setup
            self.lidar = self.robot.getLidar("lidar")
            self.lidar.enable(self.timestep)
            self.has_lidar = True
        except:
            print(f"Warning: No LIDAR available for {self.robot_name}")
            self.has_lidar = False
        
        # Motor setup
        self.left_motor = self.robot.getMotor("left motor")
        self.right_motor = self.robot.getMotor("right motor")
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)
        
        # Display for enhanced visualization
        try:
            self.display = self.robot.getDisplay("extra_display")
            self.grapher = Grapher(self.display)
            self.has_display = True
        except:
            print(f"Warning: No display available for {self.robot_name}")
            self.has_display = False
        
        # Enhanced LIDAR parameters with auto-tuning capability
        if self.has_lidar:
            ranges_str = "1.13114178 0.85820043 0.57785118 0.43461093 0.38639969 0.31585345 0.2667459 0.23062678 0.21593061 0.19141567 0.17178488 0.15571462 0.14872716 0.13643947 0.12597121 0.11696267"
            self.RANGES = [float(i) for i in ranges_str.split(' ')]
            self.SIZES = (16, 512)
            self.EPSILON = 0.6  # Will be auto-tuned
            self.DELTA_THETA = 0.1
            self.DELTA_R = 0.02
        
        # Enhanced visualization with more colors and patterns
        self.colors = [
            0xFF0000, 0x800000, 0xFFFF00, 0x808000, 0x00FF00, 0x008000, 
            0x00FFFF, 0x008080, 0x0000FF, 0x000080, 0xFF00FF, 0x800080,
            0xFFA500, 0x800080, 0x90EE90, 0x20B2AA, 0xF0E68C, 0xDDA0DD
        ]
    
    def detect_neighbors(self):
        """Enhanced neighbor detection with position prediction and tracking"""
        if not self.has_lidar or not CHUHABOT_FUNCTIONS_AVAILABLE:
            # Fallback: simulate neighbor detection for testing
            return self._simulate_neighbors(), ([], [])
        
        # Use existing ChuhaBot detection pipeline with enhancements
        theta_data_aligned = get_theta_data_aligned(
            self.lidar, self.SIZES, self.RANGES, self.EPSILON
        )
        theta_data_colored = get_theta_data_colored(
            theta_data_aligned, self.DELTA_THETA, self.DELTA_R
        )
        neighbors_x, neighbors_y = get_neighbours(theta_data_colored)
        
        # Enhanced neighbor tracking with velocity estimation
        neighbors = []
        for i, (x, y) in enumerate(zip(neighbors_x, neighbors_y)):
            # Estimate velocity from position history
            velocity = self._estimate_neighbor_velocity(i, (x, y))
            
            neighbor = SwarmAgent(
                position=(x, y),
                velocity=velocity,
                heading=np.arctan2(y, x),
                id=f"neighbor_{i}",
                role="follower"
            )
            neighbors.append(neighbor)
        
        # Update neighbor history for learning
        self._update_neighbor_history(neighbors)
        
        return neighbors, (neighbors_x, neighbors_y)
    
    def _simulate_neighbors(self):
        """Simulate neighbors for testing when LIDAR is not available"""
        # Create some mock neighbors for demonstration
        mock_neighbors = []
        if self.step_count > 50:  # Add neighbors after some time
            for i in range(2):
                angle = (self.step_count * 0.01 + i * math.pi) % (2 * math.pi)
                distance = 0.3 + 0.1 * math.sin(self.step_count * 0.02)
                x = distance * math.cos(angle)
                y = distance * math.sin(angle)
                
                neighbor = SwarmAgent(
                    position=(x, y),
                    velocity=(0.0, 0.0),
                    heading=angle,
                    id=f"mock_neighbor_{i}",
                    role="follower"
                )
                mock_neighbors.append(neighbor)
        
        return mock_neighbors
    
    def _estimate_neighbor_velocity(self, neighbor_id: int, current_pos: Tuple[float, float]) -> Tuple[float, float]:
        """Estimate neighbor velocity from position history"""
        if len(self.neighbor_history) < 2:
            return (0.0, 0.0)
        
        # Simple velocity estimation using last two positions
        try:
            last_positions = self.neighbor_history[-2:]
            if len(last_positions) >= 2 and neighbor_id < len(last_positions[0]):
                prev_pos = last_positions[0][neighbor_id].position
                dt = self.timestep / 1000.0  # Convert to seconds
                
                vx = (current_pos[0] - prev_pos[0]) / dt
                vy = (current_pos[1] - prev_pos[1]) / dt
                
                return (vx, vy)
        except (IndexError, AttributeError):
            pass
        
        return (0.0, 0.0)
    
    def _update_neighbor_history(self, neighbors: List[SwarmAgent]):
        """Update neighbor history for learning and prediction"""
        self.neighbor_history.append(neighbors.copy())
        
        # Keep only recent history (last 10 steps)
        if len(self.neighbor_history) > 10:
            self.neighbor_history.pop(0)
    
    def auto_tune_parameters(self):
        """Automatically tune detection and behavior parameters based on performance"""
        if self.step_count % 200 == 0 and self.step_count > 0:
            # Analyze recent performance
            avg_neighbors = np.mean([len(h) for h in self.neighbor_history[-5:]] if self.neighbor_history else [0])
            
            # Adjust EPSILON based on neighbor detection quality
            if avg_neighbors < 1 and self.EPSILON > 0.3:
                self.EPSILON -= 0.1  # More sensitive detection
                print(f"[{self.robot_name}] Auto-tuned EPSILON to {self.EPSILON:.2f} (more sensitive)")
            elif avg_neighbors > 4 and self.EPSILON < 0.9:
                self.EPSILON += 0.1  # Less sensitive detection
                print(f"[{self.robot_name}] Auto-tuned EPSILON to {self.EPSILON:.2f} (less sensitive)")
    
    def detect_formation_quality(self, neighbors: List[SwarmAgent]) -> float:
        """Analyze how well the swarm maintains formation"""
        if len(neighbors) < 2:
            return 0.0
        
        if self.formation_type == "circle":
            # Measure how circular the formation is
            center_x = np.mean([n.position[0] for n in neighbors])
            center_y = np.mean([n.position[1] for n in neighbors])
            
            distances = [math.sqrt((n.position[0] - center_x)**2 + (n.position[1] - center_y)**2) 
                        for n in neighbors]
            
            if len(distances) > 1:
                std_dev = np.std(distances)
                mean_dist = np.mean(distances)
                # Quality is high when distances are similar (low std deviation)
                quality = max(0.0, 1.0 - std_dev / (mean_dist + 0.001))
                return quality
        
        return 0.5  # Default quality for other formations
    
    def create_current_agent(self):
        """Create SwarmAgent representation of current robot"""
        return SwarmAgent(
            position=(0.0, 0.0),  # Robot is at origin in its own frame
            velocity=(0.0, 0.0),  # Could track from odometry
            heading=0.0,
            id=self.robot_name,
            role="follower" if not self.is_leader() else "leader"
        )
    
    def is_leader(self):
        """Determine if this robot should act as leader"""
        # Simple leadership election: robot with specific name or lowest ID
        return self.robot_name.endswith("_0") or "leader" in self.robot_name.lower()
    
    def adapt_behavior_to_mission(self, neighbors: List[SwarmAgent]):
        """Dynamically adapt behaviors based on mission, environment, and learning"""
        neighbor_count = len(neighbors)
        formation_quality = self.detect_formation_quality(neighbors)
        
        # Update performance metrics
        self.performance_metrics['time_in_formation'] += (1.0 if formation_quality > 0.7 else 0.0)
        
        # Adaptive behavior selection with learning
        if self.mission_mode == "exploration":
            # Emphasize exploration and obstacle avoidance
            weights = BehaviorWeight(
                separation=2.5 + (0.5 if neighbor_count > 3 else 0),  # More separation when crowded
                alignment=0.8,
                cohesion=1.2 - (0.3 if neighbor_count > 4 else 0),  # Less cohesion when many neighbors
                obstacle_avoidance=3.5,
                exploration=2.0 + (1.0 if neighbor_count < 2 else 0)  # More exploration when alone
            )
            
        elif self.mission_mode == "formation":
            # Adaptive formation control based on quality
            base_formation_weight = 2.5
            if formation_quality < 0.5:
                base_formation_weight += 1.0  # Increase formation weight if quality is poor
                
            weights = BehaviorWeight(
                separation=1.5,
                alignment=2.0 + (0.5 if formation_quality < 0.6 else 0),
                cohesion=1.8 + (0.7 if formation_quality < 0.5 else 0),
                obstacle_avoidance=3.0,
                formation=base_formation_weight
            )
            
        elif self.mission_mode == "following" and neighbor_count > 0:
            # Adaptive leader-following with distance consideration
            avg_distance = np.mean([math.sqrt(n.position[0]**2 + n.position[1]**2) for n in neighbors])
            
            weights = BehaviorWeight(
                separation=2.0 + (1.0 if avg_distance < 0.2 else 0),
                alignment=1.5,
                cohesion=2.5 - (0.5 if avg_distance > 0.5 else 0),
                obstacle_avoidance=3.0,
                leader_following=3.0 + (1.0 if avg_distance > 0.4 else 0)
            )
            
        elif self.mission_mode == "patrol":
            # New patrol mode: systematic area coverage
            weights = BehaviorWeight(
                separation=3.0,
                alignment=1.2,
                cohesion=0.8,
                obstacle_avoidance=4.0,
                exploration=1.5
            )
            
        elif self.mission_mode == "search":
            # New search mode: coordinated search pattern
            weights = BehaviorWeight(
                separation=2.0,
                alignment=2.5,
                cohesion=1.5,
                obstacle_avoidance=3.5,
                exploration=2.5
            )
        else:
            # Default balanced behavior with slight learning adjustment
            weights = BehaviorWeight(
                separation=2.0 + self.learning_rate * formation_quality,
                alignment=1.0,
                cohesion=1.0 + self.learning_rate * (1.0 - formation_quality),
                obstacle_avoidance=3.0
            )
        
        self.swarm_controller.update_weights(weights)
        
        # Update formation type based on environment
        self._adapt_formation_type(neighbors)
    
    def visualize_swarm_state(self, neighbors_positions, force_vector, obstacles=None, formation_quality=0.0):
        """Enhanced visualization with formation quality, obstacles, and force vectors"""
        if not self.has_display:
            return
            
        try:
            self.grapher.clear()
            
            # Draw robot at center with status color
            robot_color = 0xFFFFFF  # White default
            if self.is_leader():
                robot_color = 0xFFD700  # Gold for leader
            elif formation_quality > 0.8:
                robot_color = 0x00FF00  # Green for good formation
            elif formation_quality > 0.5:
                robot_color = 0xFFA500  # Orange for okay formation
            else:
                robot_color = 0xFF4500  # Red-orange for poor formation
                
            self.grapher.drawPointCenter(0, 0, size=10, color=robot_color)
            
            # Draw neighbors with enhanced info
            if len(neighbors_positions[0]) > 0:
                DISPLAY_SCALING_FACTOR = 1024 / (self.RANGES[0] if self.has_lidar else 2.0)
                
                for i, (x, y) in enumerate(zip(neighbors_positions[0], neighbors_positions[1])):
                    color = self.colors[i % len(self.colors)]
                    x_scaled = int(x * DISPLAY_SCALING_FACTOR)
                    y_scaled = int(y * DISPLAY_SCALING_FACTOR)
                    
                    # Size based on distance (closer = larger)
                    distance = math.sqrt(x*x + y*y)
                    size = max(4, int(8 - distance * 10))
                    
                    self.grapher.drawPointCenter(x_scaled, y_scaled, size=size, color=color)
                    
                    # Draw connection lines for formation visualization
                    if self.mission_mode == "formation" and i == 0:
                        # Draw line to first neighbor
                        steps = max(abs(x_scaled), abs(y_scaled)) // 5
                        if steps > 0:
                            for step in range(steps):
                                line_x = int((step / steps) * x_scaled)
                                line_y = int((step / steps) * y_scaled)
                                self.grapher.drawPointCenter(line_x, line_y, size=1, color=0x404040)
            
            # Draw obstacles
            if obstacles:
                DISPLAY_SCALING_FACTOR = 1024 / (self.RANGES[0] if self.has_lidar else 2.0)
                for obs_x, obs_y in obstacles:
                    x_scaled = int(obs_x * DISPLAY_SCALING_FACTOR)
                    y_scaled = int(obs_y * DISPLAY_SCALING_FACTOR)
                    self.grapher.drawPointCenter(x_scaled, y_scaled, size=8, color=0xFF0000)
            
            # Draw force vector
            if force_vector[0] != 0 or force_vector[1] != 0:
                force_magnitude = math.sqrt(force_vector[0]**2 + force_vector[1]**2)
                if force_magnitude > 0.01:
                    DISPLAY_SCALING_FACTOR = 1024 / (self.RANGES[0] if self.has_lidar else 2.0)
                    force_x_scaled = int(force_vector[0] * DISPLAY_SCALING_FACTOR * 0.5)
                    force_y_scaled = int(force_vector[1] * DISPLAY_SCALING_FACTOR * 0.5)
                    
                    # Draw force vector as arrow
                    self.grapher.drawPointCenter(force_x_scaled, force_y_scaled, size=6, color=0x00FF00)
                    
                    # Draw force magnitude indicator
                    magnitude_indicator = min(int(force_magnitude * 20), 15)
                    for i in range(magnitude_indicator):
                        indicator_x = int((i / magnitude_indicator) * force_x_scaled * 0.8)
                        indicator_y = int((i / magnitude_indicator) * force_y_scaled * 0.8)
                        self.grapher.drawPointCenter(indicator_x, indicator_y, size=2, color=0x40FF40)
            
            # Display mission mode and formation quality
            # (This would require text rendering capability in the display)
            
        except Exception as e:
            print(f"Warning: Visualization failed: {e}")
    
    def run_step(self):
        """Execute one enhanced control step with adaptive intelligence"""
        self.step_count += 1
        
        # Auto-tune parameters periodically
        self.auto_tune_parameters()
        
        # Detect neighbors with enhanced tracking
        neighbors, neighbors_positions = self.detect_neighbors()
        self.last_neighbor_count = len(neighbors)
        
        # Intelligent obstacle detection
        obstacles = self.intelligent_obstacle_detection(neighbors)
        
        # Create current agent representation
        current_agent = self.create_current_agent()
        
        # Adapt behavior based on mission, environment, and learning
        self.adapt_behavior_to_mission(neighbors)
        
        # Calculate formation quality for feedback
        formation_quality = self.detect_formation_quality(neighbors)
        
        # Calculate enhanced swarm behavior forces
        force_x, force_y = self.swarm_controller.calculate_movement(
            current_agent, neighbors, obstacles
        )
        
        # Add emergency behaviors
        force_x, force_y = self._apply_emergency_behaviors(force_x, force_y, neighbors, obstacles)
        
        # Convert to motor commands with enhanced control
        left_velocity, right_velocity = self.swarm_controller.convert_to_motor_commands(
            force_x, force_y, max_velocity=60.0
        )
        
        # Apply smoothing to reduce jittery movements
        left_velocity, right_velocity = self._smooth_motor_commands(left_velocity, right_velocity)
        
        # Apply motor commands
        self.left_motor.setVelocity(left_velocity)
        self.right_motor.setVelocity(right_velocity)
        
        # Update performance metrics
        self._update_performance_metrics(neighbors, obstacles, formation_quality)
        
        # Enhanced visualization
        self.visualize_swarm_state(neighbors_positions, (force_x, force_y), obstacles, formation_quality)
        
        # Intelligent status updates
        if self.step_count % 150 == 0:
            self._print_enhanced_status(neighbors, obstacles, formation_quality, force_x, force_y)
        
        # Automatic mission mode switching based on conditions
        self._auto_switch_mission_mode(neighbors, formation_quality)
    
    def _apply_emergency_behaviors(self, force_x: float, force_y: float, 
                                 neighbors: List[SwarmAgent], obstacles: List[Tuple[float, float]]) -> Tuple[float, float]:
        """Apply emergency behaviors for collision avoidance and safety"""
        emergency_force_x, emergency_force_y = 0.0, 0.0
        
        # Emergency separation from very close neighbors
        for neighbor in neighbors:
            distance = math.sqrt(neighbor.position[0]**2 + neighbor.position[1]**2)
            if distance < 0.08:  # Very close (8cm)
                # Strong repulsion
                angle = math.atan2(neighbor.position[1], neighbor.position[0])
                emergency_force_x -= math.cos(angle) * 2.0
                emergency_force_y -= math.sin(angle) * 2.0
                
                # Count collision
                self.performance_metrics['collision_count'] += 0.1
        
        # Emergency obstacle avoidance
        for obstacle in obstacles:
            distance = math.sqrt(obstacle[0]**2 + obstacle[1]**2)
            if distance < 0.12:  # Very close to obstacle (12cm)
                angle = math.atan2(obstacle[1], obstacle[0])
                emergency_force_x -= math.cos(angle) * 3.0
                emergency_force_y -= math.sin(angle) * 3.0
        
        # Combine with normal forces
        return force_x + emergency_force_x, force_y + emergency_force_y
    
    def _smooth_motor_commands(self, left_vel: float, right_vel: float) -> Tuple[float, float]:
        """Apply smoothing to motor commands to reduce jittery movement"""
        if not hasattr(self, '_last_left_vel'):
            self._last_left_vel = 0.0
            self._last_right_vel = 0.0
        
        # Simple exponential smoothing
        alpha = 0.7  # Smoothing factor
        smooth_left = alpha * left_vel + (1 - alpha) * self._last_left_vel
        smooth_right = alpha * right_vel + (1 - alpha) * self._last_right_vel
        
        self._last_left_vel = smooth_left
        self._last_right_vel = smooth_right
        
        return smooth_left, smooth_right
    
    def _update_performance_metrics(self, neighbors: List[SwarmAgent], obstacles: List[Tuple[float, float]], formation_quality: float):
        """Update comprehensive performance metrics"""
        # Distance traveled
        current_pos = (0.0, 0.0)  # Robot is always at origin in its frame
        # In a real implementation, this would use odometry or GPS
        
        # Exploration coverage (simplified)
        self.performance_metrics['exploration_coverage'] += 0.1 if len(neighbors) < 3 else 0.05
        
        # Formation time
        if formation_quality > 0.7:
            self.performance_metrics['time_in_formation'] += 1
    
    def _print_enhanced_status(self, neighbors: List[SwarmAgent], obstacles: List[Tuple[float, float]], 
                             formation_quality: float, force_x: float, force_y: float):
        """Print comprehensive status information"""
        status_parts = [
            f"[{self.robot_name}] Step {self.step_count}:",
            f"Neighbors: {len(neighbors)}",
            f"Obstacles: {len(obstacles)}",
            f"Mode: {self.mission_mode}",
            f"Formation: {self.formation_type} (Q: {formation_quality:.2f})",
            f"Force: ({force_x:.2f}, {force_y:.2f})"
        ]
        
        # Add performance summary every 1000 steps
        if self.step_count % 1000 == 0:
            metrics = self.performance_metrics
            status_parts.extend([
                f"\n   📊 Performance Summary:",
                f"   Formation Time: {metrics['time_in_formation']:.0f}s",
                f"   Collisions: {metrics['collision_count']:.1f}",
                f"   Coverage: {metrics['exploration_coverage']:.1f}"
            ])
        
        print(" ".join(status_parts))
    
    def _auto_switch_mission_mode(self, neighbors: List[SwarmAgent], formation_quality: float):
        """Automatically switch mission modes based on intelligent analysis"""
        neighbor_count = len(neighbors)
        
        # Auto-switch logic based on conditions
        if self.step_count > 500 and self.step_count % 800 == 0:
            if self.mission_mode == "exploration" and neighbor_count >= 3:
                self.switch_mission_mode("formation")
            elif self.mission_mode == "formation" and formation_quality > 0.8:
                self.switch_mission_mode("patrol")
            elif self.mission_mode == "patrol" and self.step_count % 1600 == 0:
                self.switch_mission_mode("exploration")
    
    def switch_mission_mode(self, new_mode):
        """Switch mission mode dynamically"""
        if new_mode in ["exploration", "formation", "following"]:
            self.mission_mode = new_mode
            print(f"[{self.robot_name}] Switched to {new_mode} mode")
    
    def _adapt_formation_type(self, neighbors: List[SwarmAgent]):
        """Intelligently adapt formation type based on environment and neighbors"""
        neighbor_count = len(neighbors)
        
        # Auto-switch formation types based on conditions
        if neighbor_count >= 4:
            if self.formation_type != "circle":
                self.formation_type = "circle"
                print(f"[{self.robot_name}] Switched to circle formation (4+ neighbors)")
        elif neighbor_count >= 2:
            if self.formation_type != "line":
                self.formation_type = "line"
                print(f"[{self.robot_name}] Switched to line formation (2-3 neighbors)")
    
    def intelligent_obstacle_detection(self, neighbors: List[SwarmAgent]) -> List[Tuple[float, float]]:
        """Enhanced obstacle detection using LIDAR data and neighbor information"""
        obstacles = []
        
        if not self.has_lidar:
            return obstacles
        
        try:
            # Get raw LIDAR data
            range_image = self.lidar.getRangeImage()
            
            # Process LIDAR data to find obstacles (not other robots)
            for layer in range(min(self.SIZES[0], len(range_image))):
                for theta_idx in range(min(self.SIZES[1], len(range_image[layer]))):
                    point_range = range_image[layer][theta_idx]
                    
                    # Check if this is likely an obstacle (not a robot)
                    if point_range < self.RANGES[layer] * 0.8:  # Closer than expected
                        theta = (theta_idx / self.SIZES[1]) * 2 * math.pi
                        x = point_range * math.cos(theta)
                        y = point_range * math.sin(theta)
                        
                        # Check if this point is too close to any known neighbor
                        is_neighbor = False
                        for neighbor in neighbors:
                            dist = math.sqrt((x - neighbor.position[0])**2 + (y - neighbor.position[1])**2)
                            if dist < 0.1:  # Within 10cm of a neighbor
                                is_neighbor = True
                                break
                        
                        if not is_neighbor:
                            obstacles.append((x, y))
            
            # Cluster nearby obstacle points
            obstacles = self._cluster_obstacles(obstacles)
            
        except Exception as e:
            print(f"Warning: Obstacle detection failed: {e}")
        
        return obstacles
    
    def _cluster_obstacles(self, obstacles: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """Cluster nearby obstacle points into single obstacles"""
        if len(obstacles) < 2:
            return obstacles
        
        clustered = []
        used = set()
        
        for i, obs1 in enumerate(obstacles):
            if i in used:
                continue
                
            cluster_x, cluster_y = obs1[0], obs1[1]
            cluster_count = 1
            used.add(i)
            
            # Find nearby obstacles to cluster
            for j, obs2 in enumerate(obstacles[i+1:], i+1):
                if j in used:
                    continue
                    
                dist = math.sqrt((obs1[0] - obs2[0])**2 + (obs1[1] - obs2[1])**2)
                if dist < 0.15:  # Cluster if within 15cm
                    cluster_x += obs2[0]
                    cluster_y += obs2[1]
                    cluster_count += 1
                    used.add(j)
            
            # Add clustered obstacle center
            clustered.append((cluster_x / cluster_count, cluster_y / cluster_count))
        
        return clustered

def main():
    """Main controller execution with enhanced capabilities demonstration"""
    try:
        # Initialize robot
        robot = Robot()
        
        # Create enhanced controller
        controller = ChuhaEnhancedController(robot)
        
        print("🚀 Enhanced ChuhaBot Controller V2.0 Started!")
        print(f"   Robot: {controller.robot_name}")
        print(f"   Leader: {'Yes' if controller.is_leader() else 'No'}")
        print(f"   LIDAR: {'Available' if controller.has_lidar else 'Simulated'}")
        print(f"   Display: {'Available' if controller.has_display else 'Disabled'}")
        print("   Available modes: exploration, formation, following, patrol, search")
        print("   Features: Auto-tuning, Learning, Emergency behaviors, Obstacle detection")
        print()
        
        # Enhanced mission scenarios
        mission_schedule = [
            (0, "exploration", "Initial area exploration"),
            (600, "formation", "Demonstrate formation control"),
            (1200, "patrol", "Systematic area patrol"),
            (1800, "search", "Coordinated search pattern"),
            (2400, "following", "Leader-follower dynamics")
        ]
        
        current_mission_idx = 0
        
        # Main enhanced control loop
        timestep = controller.timestep
        while robot.step(timestep) != -1:
            # Execute enhanced control step
            controller.run_step()
            
            # Advanced mission scheduling
            if (current_mission_idx < len(mission_schedule) and 
                controller.step_count >= mission_schedule[current_mission_idx][0]):
                
                step, mode, description = mission_schedule[current_mission_idx]
                controller.switch_mission_mode(mode)
                print(f"🎯 Mission Update: {description}")
                current_mission_idx += 1
            
            # Demonstrate dynamic formation switching
            if controller.step_count % 500 == 0 and controller.step_count > 0:
                # Cycle through formation types
                formation_types = ["circle", "line", "v_shape"]
                current_formation = formation_types[
                    (controller.step_count // 500) % len(formation_types)
                ]
                if controller.formation_type != current_formation:
                    controller.formation_type = current_formation
                    print(f"🔄 Formation switched to: {current_formation}")
            
            # Emergency stop example (optional)
            if controller.step_count > 3000:  # Run for ~1.5 minutes
                print("🏁 Demonstration complete!")
                break
                
    except Exception as e:
        print(f"❌ Error in main controller: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
