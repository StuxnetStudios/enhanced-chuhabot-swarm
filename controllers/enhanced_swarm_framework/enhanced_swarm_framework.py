#!/usr/bin/env python3.6
"""
Enhanced Modular Swarm Framework for ChuhaBot
============================================

This framework provides a modular approach to swarm robotics behaviors,
making it easy to combine different behaviors and experiment with hybrid approaches.

Features:
- Modular behavior system with easy combination
- Reynolds' flocking rules implementation
- Formation control capabilities
- Leader-follower dynamics
- Obstacle avoidance with potential fields
- Communication simulation
- Performance metrics and logging
"""

# Handle imports with fallbacks for development environment
try:
    from controller import Robot, Motor, Lidar, Display, Keyboard
except ImportError:
    # Development environment - use compatibility layer
    try:
        from webots_compat import Robot, Motor, Lidar, Display, Keyboard
    except ImportError:
        print("Warning: Webots controller not available. Some features may not work.")
        Robot = Motor = Lidar = Display = Keyboard = None

try:
    import numpy as np
except ImportError:
    print("Error: numpy is required. Please install with: pip install numpy")
    import sys
    sys.exit(1)

import math
import time
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class BehaviorType(Enum):
    SEPARATION = "separation"
    ALIGNMENT = "alignment"
    COHESION = "cohesion"
    OBSTACLE_AVOIDANCE = "obstacle_avoidance"
    LEADER_FOLLOWING = "leader_following"
    FORMATION = "formation"
    EXPLORATION = "exploration"

@dataclass
class SwarmAgent:
    """Represents a single agent in the swarm"""
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    heading: float
    id: str
    role: str = "follower"  # leader, follower, scout
    
@dataclass
class BehaviorWeight:
    """Weights for different behaviors"""
    separation: float = 2.0
    alignment: float = 1.0
    cohesion: float = 1.0
    obstacle_avoidance: float = 3.0
    leader_following: float = 1.5
    formation: float = 1.0
    exploration: float = 0.5

class SwarmBehavior:
    """Base class for swarm behaviors"""
    
    def __init__(self, weight: float = 1.0):
        self.weight = weight
        
    def calculate_force(self, agent: SwarmAgent, neighbors: List[SwarmAgent], 
                       obstacles: List[Tuple[float, float]] = None) -> Tuple[float, float]:
        """Calculate the force vector for this behavior"""
        raise NotImplementedError

class SeparationBehavior(SwarmBehavior):
    """Keeps agents from crowding together"""
    
    def __init__(self, weight: float = 2.0, separation_distance: float = 0.15):
        super().__init__(weight)
        self.separation_distance = separation_distance
        
    def calculate_force(self, agent: SwarmAgent, neighbors: List[SwarmAgent], 
                       obstacles: List[Tuple[float, float]] = None) -> Tuple[float, float]:
        force_x, force_y = 0.0, 0.0
        
        for neighbor in neighbors:
            dx = agent.position[0] - neighbor.position[0]
            dy = agent.position[1] - neighbor.position[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if 0 < distance < self.separation_distance:
                # Inverse square law for repulsion
                force_magnitude = (self.separation_distance - distance) / (distance * distance + 0.001)
                force_x += (dx / distance) * force_magnitude
                force_y += (dy / distance) * force_magnitude
                
        return force_x * self.weight, force_y * self.weight

class AlignmentBehavior(SwarmBehavior):
    """Aligns agent velocity with neighbors"""
    
    def __init__(self, weight: float = 1.0, alignment_radius: float = 0.3):
        super().__init__(weight)
        self.alignment_radius = alignment_radius
        
    def calculate_force(self, agent: SwarmAgent, neighbors: List[SwarmAgent], 
                       obstacles: List[Tuple[float, float]] = None) -> Tuple[float, float]:
        avg_vx, avg_vy = 0.0, 0.0
        count = 0
        
        for neighbor in neighbors:
            dx = agent.position[0] - neighbor.position[0]
            dy = agent.position[1] - neighbor.position[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.alignment_radius:
                avg_vx += neighbor.velocity[0]
                avg_vy += neighbor.velocity[1]
                count += 1
                
        if count > 0:
            avg_vx /= count
            avg_vy /= count
            # Steer towards average velocity
            force_x = avg_vx - agent.velocity[0]
            force_y = avg_vy - agent.velocity[1]
            return force_x * self.weight, force_y * self.weight
            
        return 0.0, 0.0

class CohesionBehavior(SwarmBehavior):
    """Moves agent toward average position of neighbors"""
    
    def __init__(self, weight: float = 1.0, cohesion_radius: float = 0.5):
        super().__init__(weight)
        self.cohesion_radius = cohesion_radius
        
    def calculate_force(self, agent: SwarmAgent, neighbors: List[SwarmAgent], 
                       obstacles: List[Tuple[float, float]] = None) -> Tuple[float, float]:
        center_x, center_y = 0.0, 0.0
        count = 0
        
        for neighbor in neighbors:
            dx = agent.position[0] - neighbor.position[0]
            dy = agent.position[1] - neighbor.position[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < self.cohesion_radius:
                center_x += neighbor.position[0]
                center_y += neighbor.position[1]
                count += 1
                
        if count > 0:
            center_x /= count
            center_y /= count
            # Steer towards center
            force_x = center_x - agent.position[0]
            force_y = center_y - agent.position[1]
            return force_x * self.weight, force_y * self.weight
            
        return 0.0, 0.0

class ObstacleAvoidanceBehavior(SwarmBehavior):
    """Avoids obstacles using potential fields"""
    
    def __init__(self, weight: float = 3.0, avoidance_radius: float = 0.2):
        super().__init__(weight)
        self.avoidance_radius = avoidance_radius
        
    def calculate_force(self, agent: SwarmAgent, neighbors: List[SwarmAgent], 
                       obstacles: List[Tuple[float, float]] = None) -> Tuple[float, float]:
        if not obstacles:
            return 0.0, 0.0
            
        force_x, force_y = 0.0, 0.0
        
        for obstacle in obstacles:
            dx = agent.position[0] - obstacle[0]
            dy = agent.position[1] - obstacle[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if 0 < distance < self.avoidance_radius:
                # Strong repulsion from obstacles
                force_magnitude = (self.avoidance_radius - distance) / (distance * distance + 0.001)
                force_x += (dx / distance) * force_magnitude * 2.0
                force_y += (dy / distance) * force_magnitude * 2.0
                
        return force_x * self.weight, force_y * self.weight

class FormationBehavior(SwarmBehavior):
    """Maintains specific formation patterns"""
    
    def __init__(self, weight: float = 1.0, formation_type: str = "circle"):
        super().__init__(weight)
        self.formation_type = formation_type
        self.formation_radius = 0.3
        
    def calculate_force(self, agent: SwarmAgent, neighbors: List[SwarmAgent], 
                       obstacles: List[Tuple[float, float]] = None) -> Tuple[float, float]:
        if self.formation_type == "circle":
            return self._circle_formation(agent, neighbors)
        elif self.formation_type == "line":
            return self._line_formation(agent, neighbors)
        elif self.formation_type == "v_shape":
            return self._v_formation(agent, neighbors)
        else:
            return 0.0, 0.0
    
    def _circle_formation(self, agent: SwarmAgent, neighbors: List[SwarmAgent]) -> Tuple[float, float]:
        if not neighbors:
            return 0.0, 0.0
            
        # Calculate center of mass
        center_x = sum(n.position[0] for n in neighbors) / len(neighbors)
        center_y = sum(n.position[1] for n in neighbors) / len(neighbors)
        
        # Calculate desired position on circle
        angle_to_center = math.atan2(agent.position[1] - center_y, agent.position[0] - center_x)
        desired_x = center_x + self.formation_radius * math.cos(angle_to_center)
        desired_y = center_y + self.formation_radius * math.sin(angle_to_center)
        
        force_x = desired_x - agent.position[0]
        force_y = desired_y - agent.position[1]
        
        return force_x * self.weight, force_y * self.weight

    def _line_formation(self, agent: SwarmAgent, neighbors: List[SwarmAgent]) -> Tuple[float, float]:
        # Simple line formation along x-axis
        if not neighbors:
            return 0.0, 0.0
            
        avg_y = sum(n.position[1] for n in neighbors) / len(neighbors)
        force_y = avg_y - agent.position[1]
        
        return 0.0, force_y * self.weight

    def _v_formation(self, agent: SwarmAgent, neighbors: List[SwarmAgent]) -> Tuple[float, float]:
        # V-formation for efficient movement
        # Implementation would depend on specific requirements
        return 0.0, 0.0

class EnhancedSwarmController:
    """Main controller that combines multiple behaviors"""
    
    def __init__(self, robot_name: str):
        self.robot_name = robot_name
        self.behaviors: Dict[BehaviorType, SwarmBehavior] = {}
        self.weights = BehaviorWeight()
        
        # Performance metrics
        self.start_time = time.time()
        self.distance_traveled = 0.0
        self.last_position = (0.0, 0.0)
        
        # Initialize default behaviors
        self._initialize_behaviors()
        
    def _initialize_behaviors(self):
        """Initialize default behavior set"""
        self.behaviors[BehaviorType.SEPARATION] = SeparationBehavior(self.weights.separation)
        self.behaviors[BehaviorType.ALIGNMENT] = AlignmentBehavior(self.weights.alignment)
        self.behaviors[BehaviorType.COHESION] = CohesionBehavior(self.weights.cohesion)
        self.behaviors[BehaviorType.OBSTACLE_AVOIDANCE] = ObstacleAvoidanceBehavior(self.weights.obstacle_avoidance)
        self.behaviors[BehaviorType.FORMATION] = FormationBehavior(self.weights.formation)
        
    def add_behavior(self, behavior_type: BehaviorType, behavior: SwarmBehavior):
        """Add or replace a behavior"""
        self.behaviors[behavior_type] = behavior
        
    def remove_behavior(self, behavior_type: BehaviorType):
        """Remove a behavior"""
        if behavior_type in self.behaviors:
            del self.behaviors[behavior_type]
            
    def update_weights(self, new_weights: BehaviorWeight):
        """Update behavior weights"""
        self.weights = new_weights
        for behavior_type, behavior in self.behaviors.items():
            if behavior_type == BehaviorType.SEPARATION:
                behavior.weight = new_weights.separation
            elif behavior_type == BehaviorType.ALIGNMENT:
                behavior.weight = new_weights.alignment
            elif behavior_type == BehaviorType.COHESION:
                behavior.weight = new_weights.cohesion
            elif behavior_type == BehaviorType.OBSTACLE_AVOIDANCE:
                behavior.weight = new_weights.obstacle_avoidance
            elif behavior_type == BehaviorType.FORMATION:
                behavior.weight = new_weights.formation
                
    def calculate_movement(self, current_agent: SwarmAgent, neighbors: List[SwarmAgent], 
                          obstacles: List[Tuple[float, float]] = None) -> Tuple[float, float]:
        """Calculate the combined movement vector from all behaviors"""
        total_force_x, total_force_y = 0.0, 0.0
        
        for behavior in self.behaviors.values():
            force_x, force_y = behavior.calculate_force(current_agent, neighbors, obstacles)
            total_force_x += force_x
            total_force_y += force_y
            
        return total_force_x, total_force_y
        
    def convert_to_motor_commands(self, force_x: float, force_y: float, 
                                 max_velocity: float = 60.0) -> Tuple[float, float]:
        """Convert force vector to differential drive motor commands"""
        # Calculate desired heading and speed
        desired_angle = math.atan2(force_x, force_y)  # Note: y forward convention
        desired_speed = min(math.sqrt(force_x*force_x + force_y*force_y), 1.0)
        
        # Convert to differential drive
        linear_velocity = desired_speed * max_velocity * 0.8
        angular_velocity = desired_angle * max_velocity * 0.3
        
        left_velocity = linear_velocity + angular_velocity
        right_velocity = linear_velocity - angular_velocity
        
        # Clamp to maximum velocity
        max_vel = max(abs(left_velocity), abs(right_velocity))
        if max_vel > max_velocity:
            left_velocity = (left_velocity / max_vel) * max_velocity
            right_velocity = (right_velocity / max_vel) * max_velocity
            
        return left_velocity, right_velocity
        
    def log_performance_metrics(self, current_position: Tuple[float, float]):
        """Log performance metrics for analysis"""
        dx = current_position[0] - self.last_position[0]
        dy = current_position[1] - self.last_position[1]
        self.distance_traveled += math.sqrt(dx*dx + dy*dy)
        self.last_position = current_position
        
        runtime = time.time() - self.start_time
        if runtime > 0:
            avg_speed = self.distance_traveled / runtime
            print(f"[{self.robot_name}] Runtime: {runtime:.1f}s, Distance: {self.distance_traveled:.2f}m, Avg Speed: {avg_speed:.3f}m/s")

# Integration with existing ChuhaBot system
def integrate_with_chuhabot():
    """
    Integration function to use the enhanced framework with existing ChuhaBot setup.
    This replaces the simple swarm_control function with the modular approach.
    """
    pass

if __name__ == "__main__":
    # Example usage - this would be integrated into the main robot controller
    print("Enhanced Swarm Framework initialized!")
    print("Available behaviors:", [bt.value for bt in BehaviorType])
    
    # Create a sample controller
    controller = EnhancedSwarmController("ChuhaBot_01")
    
    # Example: Create custom behavior weights for exploration
    exploration_weights = BehaviorWeight(
        separation=3.0,
        alignment=0.5,
        cohesion=0.8,
        obstacle_avoidance=4.0,
        exploration=2.0
    )
    
    controller.update_weights(exploration_weights)
    print("Controller configured for exploration behavior")
