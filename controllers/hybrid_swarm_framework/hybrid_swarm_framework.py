#!/usr/bin/env python3.6
"""
ChuhaBot + e-puck Hybrid Swarm Framework
======================================

This framework combines the best of both ChuhaBot and e-puck robotics platforms,
creating a unified approach that can work with different robot types in the same swarm.

Features:
- Robot abstraction layer for different platforms
- Sensor fusion between different robot types
- Scalable communication protocols
- Cross-platform behavior compatibility
- Performance optimization for different hardware
"""

from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
import math

class RobotPlatform(Enum):
    CHUHA_BASIC = "chuha_basic"
    CHUHA_LIDAR = "chuha_lidar"
    EPUCK = "epuck"
    EPUCK2 = "epuck2"
    GENERIC = "generic"

@dataclass
class SensorCapabilities:
    """Defines what sensors are available on a robot platform"""
    has_lidar: bool = False
    has_camera: bool = False
    has_proximity_sensors: bool = False
    has_light_sensors: bool = False
    has_accelerometer: bool = False
    has_gyroscope: bool = False
    has_microphone: bool = False
    has_speaker: bool = False
    has_led_ring: bool = False
    
    # Sensor ranges and specifications
    proximity_range: float = 0.1  # meters
    camera_resolution: Tuple[int, int] = (64, 64)
    lidar_range: float = 1.0
    lidar_resolution: int = 512

@dataclass
class RobotSpecification:
    """Complete specification of a robot platform"""
    platform: RobotPlatform
    sensors: SensorCapabilities
    max_velocity: float  # rad/s or m/s
    wheel_radius: float  # meters
    body_radius: float   # meters
    mass: float         # kg
    differential_drive: bool = True

class RobotAbstraction(ABC):
    """Abstract base class for robot platforms"""
    
    def __init__(self, robot_id: str, specification: RobotSpecification):
        self.robot_id = robot_id
        self.spec = specification
        self.position = (0.0, 0.0, 0.0)  # x, y, theta
        self.velocity = (0.0, 0.0)       # linear, angular
        
    @abstractmethod
    def get_neighbor_positions(self) -> List[Tuple[float, float]]:
        """Get positions of nearby robots using available sensors"""
        pass
    
    @abstractmethod
    def set_motor_velocities(self, left: float, right: float):
        """Set motor velocities for differential drive"""
        pass
    
    @abstractmethod
    def get_sensor_data(self) -> Dict:
        """Get all available sensor data"""
        pass
    
    @abstractmethod
    def update_position(self):
        """Update robot's position estimate"""
        pass

class ChuhaRobot(RobotAbstraction):
    """ChuhaBot implementation of robot abstraction"""
    
    def __init__(self, robot_id: str, robot, has_lidar: bool = True):
        # Define ChuhaBot specifications
        sensors = SensorCapabilities(
            has_lidar=has_lidar,
            has_camera=has_lidar,  # ChuhaLidarCamera has both
            proximity_range=1.13,  # From LIDAR specs
            lidar_range=1.13,
            lidar_resolution=512
        )
        
        spec = RobotSpecification(
            platform=RobotPlatform.CHUHA_LIDAR if has_lidar else RobotPlatform.CHUHA_BASIC,
            sensors=sensors,
            max_velocity=60.0,  # rad/s
            wheel_radius=0.0075,  # 1.5cm diameter
            body_radius=0.03,     # 6cm diameter
            mass=0.1,             # estimated
            differential_drive=True
        )
        
        super().__init__(robot_id, spec)
        self.robot = robot
        self._initialize_hardware()
    
    def _initialize_hardware(self):
        """Initialize ChuhaBot-specific hardware"""
        # Motors
        self.left_motor = self.robot.getMotor("left motor")
        self.right_motor = self.robot.getMotor("right motor")
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        
        # LIDAR (if available)
        if self.spec.sensors.has_lidar:
            self.lidar = self.robot.getLidar("lidar")
            timestep = int(self.robot.getBasicTimeStep())
            self.lidar.enable(timestep)
            
            # ChuhaBot LIDAR parameters
            self.lidar_ranges = [1.13114178, 0.85820043, 0.57785118, 0.43461093, 
                               0.38639969, 0.31585345, 0.2667459, 0.23062678, 
                               0.21593061, 0.19141567, 0.17178488, 0.15571462, 
                               0.14872716, 0.13643947, 0.12597121, 0.11696267]
            self.lidar_sizes = (16, 512)
            self.lidar_epsilon = 0.6
    
    def get_neighbor_positions(self) -> List[Tuple[float, float]]:
        """Get neighbor positions using LIDAR data"""
        if not self.spec.sensors.has_lidar:
            return []
        
        # Use existing ChuhaBot LIDAR processing
        # This would call the existing functions from swarm_basic_flocking
        # For now, return mock data
        return [(0.3, 0.2), (-0.2, 0.4)]  # Mock neighbor positions
    
    def set_motor_velocities(self, left: float, right: float):
        """Set motor velocities"""
        self.left_motor.setVelocity(left)
        self.right_motor.setVelocity(right)
    
    def get_sensor_data(self) -> Dict:
        """Get all sensor data"""
        data = {"platform": self.spec.platform.value}
        
        if self.spec.sensors.has_lidar:
            # Get LIDAR data
            image_array = self.lidar.getRangeImage()
            data["lidar"] = image_array
        
        return data
    
    def update_position(self):
        """Update position using odometry"""
        # Simple odometry would go here
        pass

class EPuckRobot(RobotAbstraction):
    """e-puck implementation of robot abstraction"""
    
    def __init__(self, robot_id: str, robot, version: int = 2):
        # Define e-puck specifications
        sensors = SensorCapabilities(
            has_proximity_sensors=True,
            has_light_sensors=True,
            has_camera=True,
            has_accelerometer=True,
            has_microphone=True,
            has_speaker=True,
            has_led_ring=True,
            proximity_range=0.1,
            camera_resolution=(640, 480) if version == 2 else (160, 120)
        )
        
        spec = RobotSpecification(
            platform=RobotPlatform.EPUCK2 if version == 2 else RobotPlatform.EPUCK,
            sensors=sensors,
            max_velocity=7.536,  # rad/s for e-puck
            wheel_radius=0.0205,  # 4.1cm diameter
            body_radius=0.037,    # 7.4cm diameter
            mass=0.15,            # 150g
            differential_drive=True
        )
        
        super().__init__(robot_id, spec)
        self.robot = robot
        self._initialize_hardware()
    
    def _initialize_hardware(self):
        """Initialize e-puck specific hardware"""
        # Motors
        self.left_motor = self.robot.getMotor("left wheel motor")
        self.right_motor = self.robot.getMotor("right wheel motor")
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        
        # Proximity sensors
        self.proximity_sensors = []
        for i in range(8):
            ps = self.robot.getDistanceSensor(f"ps{i}")
            timestep = int(self.robot.getBasicTimeStep())
            ps.enable(timestep)
            self.proximity_sensors.append(ps)
        
        # Camera
        if self.spec.sensors.has_camera:
            self.camera = self.robot.getCamera("camera")
            timestep = int(self.robot.getBasicTimeStep())
            self.camera.enable(timestep)
    
    def get_neighbor_positions(self) -> List[Tuple[float, float]]:
        """Get neighbor positions using proximity sensors"""
        neighbors = []
        
        for i, ps in enumerate(self.proximity_sensors):
            value = ps.getValue()
            if value > 100:  # Detection threshold
                # Convert sensor reading to position
                angle = i * (2 * math.pi / 8)  # 8 sensors around the robot
                distance = (1000 - value) / 1000 * self.spec.sensors.proximity_range
                x = distance * math.cos(angle)
                y = distance * math.sin(angle)
                neighbors.append((x, y))
        
        return neighbors
    
    def set_motor_velocities(self, left: float, right: float):
        """Set motor velocities"""
        self.left_motor.setVelocity(left)
        self.right_motor.setVelocity(right)
    
    def get_sensor_data(self) -> Dict:
        """Get all sensor data"""
        data = {"platform": self.spec.platform.value}
        
        # Proximity sensors
        data["proximity"] = [ps.getValue() for ps in self.proximity_sensors]
        
        # Camera data (if available)
        if self.spec.sensors.has_camera:
            data["camera"] = self.camera.getImage()
        
        return data
    
    def update_position(self):
        """Update position using odometry"""
        # e-puck odometry implementation
        pass

class HybridSwarmController:
    """Controller that works with multiple robot platforms"""
    
    def __init__(self):
        self.robots: Dict[str, RobotAbstraction] = {}
        self.communication_range = 0.5  # meters
        self.message_buffer: Dict[str, List] = {}
        
    def register_robot(self, robot: RobotAbstraction):
        """Register a robot with the swarm controller"""
        self.robots[robot.robot_id] = robot
        self.message_buffer[robot.robot_id] = []
        print(f"Registered {robot.spec.platform.value} robot: {robot.robot_id}")
    
    def get_platform_capabilities(self, robot_id: str) -> SensorCapabilities:
        """Get sensor capabilities for a specific robot"""
        return self.robots[robot_id].spec.sensors
    
    def sensor_fusion(self, robot_id: str) -> Dict:
        """Combine data from different sensor types"""
        robot = self.robots[robot_id]
        capabilities = robot.spec.sensors
        
        # Get neighbor positions using available sensors
        if capabilities.has_lidar:
            # High-precision LIDAR data (ChuhaBot)
            neighbors = robot.get_neighbor_positions()
            confidence = 0.95
        elif capabilities.has_proximity_sensors:
            # Lower precision proximity data (e-puck)
            neighbors = robot.get_neighbor_positions()
            confidence = 0.7
        else:
            neighbors = []
            confidence = 0.0
        
        return {
            "neighbors": neighbors,
            "confidence": confidence,
            "sensor_type": "lidar" if capabilities.has_lidar else "proximity"
        }
    
    def cross_platform_communication(self, sender_id: str, message: Dict):
        """Simulate communication between different robot platforms"""
        sender_robot = self.robots[sender_id]
        
        # Broadcast message to robots within range
        for robot_id, robot in self.robots.items():
            if robot_id == sender_id:
                continue
                
            # Calculate distance (simplified)
            distance = self._calculate_distance(sender_robot, robot)
            
            if distance <= self.communication_range:
                # Add platform-specific message formatting
                formatted_message = self._format_message_for_platform(
                    message, robot.spec.platform
                )
                self.message_buffer[robot_id].append(formatted_message)
    
    def _calculate_distance(self, robot1: RobotAbstraction, robot2: RobotAbstraction) -> float:
        """Calculate distance between two robots"""
        dx = robot1.position[0] - robot2.position[0]
        dy = robot1.position[1] - robot2.position[1]
        return math.sqrt(dx*dx + dy*dy)
    
    def _format_message_for_platform(self, message: Dict, platform: RobotPlatform) -> Dict:
        """Format message based on receiving platform capabilities"""
        formatted = message.copy()
        
        if platform in [RobotPlatform.EPUCK, RobotPlatform.EPUCK2]:
            # e-puck has limited processing, simplify message
            formatted = {
                "type": message.get("type", "info"),
                "data": str(message.get("data", ""))[:50]  # Truncate long messages
            }
        
        return formatted
    
    def optimize_behavior_for_platform(self, robot_id: str, base_behavior: Dict) -> Dict:
        """Optimize behavior parameters based on robot platform"""
        robot = self.robots[robot_id]
        platform = robot.spec.platform
        
        optimized = base_behavior.copy()
        
        if platform in [RobotPlatform.CHUHA_BASIC, RobotPlatform.CHUHA_LIDAR]:
            # ChuhaBot optimizations
            optimized["max_velocity"] = min(optimized.get("max_velocity", 60), 60)
            optimized["precision_factor"] = 1.0  # High precision with LIDAR
            
        elif platform in [RobotPlatform.EPUCK, RobotPlatform.EPUCK2]:
            # e-puck optimizations
            optimized["max_velocity"] = min(optimized.get("max_velocity", 7.5), 7.5)
            optimized["precision_factor"] = 0.7  # Lower precision with proximity sensors
            optimized["update_frequency"] = 0.5  # Reduce update frequency for efficiency
        
        return optimized

def create_robot_factory(robot, robot_id: str, platform_hint: str = None) -> RobotAbstraction:
    """Factory function to create appropriate robot abstraction"""
    
    if platform_hint:
        if "chuha" in platform_hint.lower():
            has_lidar = "lidar" in platform_hint.lower()
            return ChuhaRobot(robot_id, robot, has_lidar)
        elif "epuck" in platform_hint.lower():
            version = 2 if "2" in platform_hint else 1
            return EPuckRobot(robot_id, robot, version)
    
    # Auto-detect based on available devices
    try:
        # Try to get ChuhaBot devices
        robot.getLidar("lidar")
        return ChuhaRobot(robot_id, robot, has_lidar=True)
    except:
        try:
            # Try to get e-puck devices
            robot.getDistanceSensor("ps0")
            return EPuckRobot(robot_id, robot)
        except:
            raise ValueError(f"Could not determine robot platform for {robot_id}")

# Example usage
def example_hybrid_swarm():
    """Example of mixed ChuhaBot + e-puck swarm"""
    
    controller = HybridSwarmController()
    
    # This would be called from individual robot controllers
    print("Hybrid Swarm Framework Example")
    print("Supports: ChuhaBot (Basic/LIDAR) + e-puck (v1/v2)")
    print("Features: Cross-platform communication, sensor fusion, adaptive behaviors")
    
    return controller

if __name__ == "__main__":
    example_hybrid_swarm()
