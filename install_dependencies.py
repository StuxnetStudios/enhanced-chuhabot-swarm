#!/usr/bin/env python3
"""
ChuhaBot Enhanced Framework - Dependency Installation Script
===========================================================

This script installs all necessary dependencies for the enhanced ChuhaBot framework.
It handles both core requirements and optional packages for advanced features.
"""

import subprocess
import sys
import os
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
        return True

def check_pip():
    """Check if pip is available"""
    print("📦 Checking pip availability...")
    
    try:
        import pip
        print("✅ pip is available")
        return True
    except ImportError:
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
            print("✅ pip is available via module")
            return True
        except subprocess.CalledProcessError:
            print("❌ pip is not available!")
            print("   Please install pip first: https://pip.pypa.io/en/stable/installation/")
            return False

def is_package_installed(package_name):
    """Check if a package is already installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(package):
    """Install a single package using pip"""
    try:
        print(f"📥 Installing {package}...")
        subprocess.run([sys.executable, "-m", "pip", "install", package], 
                      check=True, capture_output=True, text=True)
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}")
        print(f"   Error: {e.stderr}")
        return False

def install_core_dependencies():
    """Install core dependencies required for the framework"""
    print("\n🔧 Installing core dependencies...")
    
    core_packages = [
        "numpy",
        "typing-extensions"
    ]
    
    success_count = 0
    for package in core_packages:
        # Check if already installed
        package_name = package.split(">=")[0].split("==")[0]
        if is_package_installed(package_name):
            print(f"✅ {package_name} already installed")
            success_count += 1
        else:
            if install_package(package):
                success_count += 1
    
    print(f"\n📊 Core dependencies: {success_count}/{len(core_packages)} installed")
    return success_count == len(core_packages)

def install_optional_dependencies():
    """Install optional dependencies for advanced features"""
    print("\n🎯 Installing optional dependencies...")
    
    optional_packages = [
        ("matplotlib", "Advanced plotting and visualization"),
        ("scipy", "Scientific computing and optimization"),
        ("scikit-learn", "Machine learning algorithms"),
        ("networkx", "Network analysis and communication simulation")
    ]
    
    installed_optional = []
    
    for package, description in optional_packages:
        if is_package_installed(package):
            print(f"✅ {package} already installed ({description})")
            installed_optional.append(package)
        else:
            print(f"📥 Installing {package} ({description})...")
            if install_package(package):
                installed_optional.append(package)
            else:
                print(f"⚠️  {package} installation failed, but framework will work without it")
    
    print(f"\n📊 Optional dependencies: {len(installed_optional)}/{len(optional_packages)} installed")
    return installed_optional

def install_from_requirements():
    """Install all dependencies from requirements.txt"""
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ {requirements_file} not found!")
        return False
    
    print(f"\n📋 Installing from {requirements_file}...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], 
                      check=True, capture_output=True, text=True)
        print("✅ All requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install some requirements")
        print(f"   Error: {e.stderr}")
        return False

def verify_installation():
    """Verify that key packages can be imported"""
    print("\n🔍 Verifying installation...")
    
    test_imports = [
        ("numpy", "import numpy as np"),
        ("math", "import math"),
        ("time", "import time"),
        ("typing", "from typing import List, Tuple, Dict, Optional"),
        ("dataclasses", "from dataclasses import dataclass"),
        ("enum", "from enum import Enum")
    ]
    
    success_count = 0
    for package_name, import_statement in test_imports:
        try:
            exec(import_statement)
            print(f"✅ {package_name} import successful")
            success_count += 1
        except ImportError as e:
            print(f"❌ {package_name} import failed: {e}")
        except Exception as e:
            print(f"⚠️  {package_name} import error: {e}")
    
    print(f"\n📊 Import verification: {success_count}/{len(test_imports)} successful")
    return success_count == len(test_imports)

def check_webots_controller():
    """Check if Webots controller module is available (expected to fail outside Webots)"""
    print("\n🤖 Checking Webots environment...")
    
    try:
        from controller import Robot
        print("✅ Webots controller module available")
        print("   (Running inside Webots environment)")
        return True
    except ImportError:
        print("ℹ️  Webots controller module not available")
        print("   (This is normal when running outside Webots)")
        print("   The framework will work when running inside Webots simulator")
        return False

def create_compatibility_layer():
    """Create a compatibility layer for development outside Webots"""
    print("\n🔧 Creating development compatibility layer...")
    
    compat_file = os.path.join("controllers", "enhanced_swarm_framework", "webots_compat.py")
    
    compat_content = '''"""
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
'''
    
    try:
        os.makedirs(os.path.dirname(compat_file), exist_ok=True)
        with open(compat_file, 'w') as f:
            f.write(compat_content)
        print(f"✅ Compatibility layer created: {compat_file}")
        return True
    except Exception as e:
        print(f"❌ Failed to create compatibility layer: {e}")
        return False

def show_next_steps():
    """Show next steps after installation"""
    print("\n🎉 Installation Complete!")
    print("=" * 50)
    
    steps = [
        "1. Open Webots simulator",
        "2. Load the demo world: worlds/enhanced_swarm_demo.wbt",
        "3. Run the enhanced ChuhaBot controllers",
        "4. Experiment with different swarm behaviors!"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n💡 Tips:")
    print("   • Check ENHANCED_README.md for detailed documentation")
    print("   • Use setup_enhanced_framework.py to verify your setup")
    print("   • Modify behavior weights in enhanced_chuha_controller.py")
    
    print("\n🐛 Troubleshooting:")
    print("   • If imports fail in Webots, the controller module is expected")
    print("   • For development outside Webots, use the compatibility layer")
    print("   • Check Python version compatibility (3.6+)")

def main():
    """Main installation process"""
    print("🤖 ChuhaBot Enhanced Framework - Dependency Installer")
    print("=" * 55)
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    # Install dependencies
    print("\n" + "=" * 30)
    print("INSTALLING DEPENDENCIES")
    print("=" * 30)
    
    # Try requirements.txt first
    if os.path.exists("requirements.txt"):
        if install_from_requirements():
            success = True
        else:
            print("⚠️  Falling back to manual installation...")
            success = install_core_dependencies()
    else:
        success = install_core_dependencies()
    
    # Install optional packages
    install_optional_dependencies()
    
    # Verify installation
    if not verify_installation():
        print("⚠️  Some core packages failed to install correctly")
        success = False
    
    # Check Webots environment
    check_webots_controller()
    
    # Create compatibility layer for development
    create_compatibility_layer()
    
    # Show results
    if success:
        show_next_steps()
        return True
    else:
        print("\n❌ Installation completed with errors")
        print("   Some features may not work properly")
        return False

if __name__ == "__main__":
    main()
