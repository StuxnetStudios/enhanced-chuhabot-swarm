"""
Webots Compatibility Layer for Development
=========================================

This module provides mock classes for Webots controller components,
allowing development and testing outside the Webots environment.
"""

class MockRobot:
    def getBasicTimeStep(self):
        return 32
    
    def getName(self):
        return "MockRobot"
    
    def step(self, timestep):
        return 0
    
    def getLidar(self, name):
        return MockLidar()
    
    def getMotor(self, name):
        return MockMotor()
    
    def getDisplay(self, name):
        return MockDisplay()

class MockMotor:
    def setPosition(self, position):
        pass
    
    def setVelocity(self, velocity):
        pass

class MockLidar:
    def enable(self, timestep):
        pass
    
    def getRangeImage(self):
        import numpy as np
        return np.random.random((16, 512))

class MockDisplay:
    def getWidth(self):
        return 1024
    
    def getHeight(self):
        return 1024
    
    def setColor(self, color):
        pass
    
    def drawPixel(self, x, y):
        pass
    
    def fillRectangle(self, x, y, width, height):
        pass

# Mock controller module
class MockController:
    Robot = MockRobot
    Motor = MockMotor
    Lidar = MockLidar
    Display = MockDisplay
    Keyboard = None

# Make it importable as 'controller'
import sys
sys.modules['controller'] = MockController()
