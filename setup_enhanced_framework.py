#!/usr/bin/env python3
"""
ChuhaBot Enhanced Framework - Quick Setup Script
==============================================

This script helps you quickly set up and test the enhanced ChuhaBot framework.
Run this script to see the available features and get started with advanced behaviors.
"""

import os
import sys

def print_header():
    print("=" * 60)
    print("🤖 ChuhaBot Enhanced Swarm Framework")
    print("=" * 60)
    print("Advanced modular swarm robotics for Webots simulation")
    print()

def print_features():
    print("🚀 Available Features:")
    features = [
        "✅ Modular Behavior System (Separation, Alignment, Cohesion)",
        "✅ Formation Control (Circle, Line, V-formation)",
        "✅ Leader-Follower Dynamics",
        "✅ Dynamic Obstacle Avoidance",
        "✅ Real-time Mission Switching",
        "✅ Cross-platform Support (ChuhaBot + e-puck)",
        "✅ Performance Metrics & Logging",
        "✅ Advanced Visualization"
    ]
    
    for feature in features:
        print(f"  {feature}")
    print()

def check_requirements():
    print("🔍 Checking Requirements:")
    
    # Check if we're in the right directory
    current_dir = os.getcwd()
    if "swarm_robotics_webots" not in current_dir:
        print("  ❌ Please run this script from the swarm_robotics_webots directory")
        return False
    else:
        print("  ✅ Running from correct directory")
    
    # Check for required directories
    required_dirs = [
        "controllers",
        "protos", 
        "worlds",
        "controllers/enhanced_swarm_framework"
    ]
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"  ✅ Found {dir_name}/")
        else:
            print(f"  ❌ Missing {dir_name}/")
            return False
    
    # Check for enhanced framework files
    framework_files = [
        "controllers/enhanced_swarm_framework/enhanced_swarm_framework.py",
        "controllers/enhanced_swarm_framework/enhanced_chuha_controller.py",
        "controllers/enhanced_swarm_framework/hybrid_swarm_framework.py"
    ]
    
    for file_name in framework_files:
        if os.path.exists(file_name):
            print(f"  ✅ Found {os.path.basename(file_name)}")
        else:
            print(f"  ❌ Missing {file_name}")
            return False
    
    print("  ✅ All requirements satisfied!")
    print()
    return True

def show_demo_scenarios():
    print("🎯 Demo Scenarios:")
    
    scenarios = [
        {
            "name": "Basic Enhanced Flocking",
            "world": "enhanced_swarm_demo.wbt",
            "robots": "6 ChuhaBot variants",
            "behaviors": "Advanced flocking with obstacle avoidance",
            "duration": "2-3 minutes"
        },
        {
            "name": "Formation Control",
            "world": "enhanced_swarm_demo.wbt", 
            "robots": "6 ChuhaBot variants",
            "behaviors": "Circle formation maintenance",
            "duration": "3-5 minutes"
        },
        {
            "name": "Leader-Follower Chain",
            "world": "enhanced_swarm_demo.wbt",
            "robots": "1 Leader + 5 Followers",
            "behaviors": "Dynamic leadership with obstacle navigation",
            "duration": "5-10 minutes"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"  {i}. {scenario['name']}")
        print(f"     World: {scenario['world']}")
        print(f"     Robots: {scenario['robots']}")
        print(f"     Behaviors: {scenario['behaviors']}")
        print(f"     Duration: {scenario['duration']}")
        print()

def show_next_steps():
    print("🛠️ Quick Start Steps:")
    
    steps = [
        "1. Open Webots simulator",
        "2. Load world: File → Open World → worlds/enhanced_swarm_demo.wbt",
        "3. Set controller: Select robot → Controller → enhanced_chuha_controller",
        "4. Start simulation: Play button or Ctrl+1",
        "5. Watch advanced swarm behaviors in action!"
    ]
    
    for step in steps:
        print(f"  {step}")
    print()

def show_customization_tips():
    print("⚙️ Customization Tips:")
    
    tips = [
        "📝 Edit behavior weights in enhanced_chuha_controller.py",
        "🎯 Change mission modes: 'exploration', 'formation', 'following'",
        "🔧 Add custom behaviors by extending SwarmBehavior class",
        "📊 Monitor performance with built-in logging",
        "🤖 Mix ChuhaBot variants for heterogeneous swarms",
        "🌐 Experiment with formation patterns (circle, line, V-shape)"
    ]
    
    for tip in tips:
        print(f"  {tip}")
    print()

def show_file_structure():
    print("📁 Enhanced Framework Structure:")
    
    structure = """
  controllers/enhanced_swarm_framework/
  ├── enhanced_swarm_framework.py      # Core behavior system
  ├── enhanced_chuha_controller.py     # ChuhaBot integration  
  └── hybrid_swarm_framework.py        # Cross-platform support
  
  worlds/
  └── enhanced_swarm_demo.wbt          # Demo world with obstacles
  
  Original ChuhaBot files:
  ├── controllers/swarm_basic_flocking/
  ├── controllers/swarm_flocking_anticollision/
  └── protos/ChuhaBasic.proto, ChuhaLidarCamera.proto
"""
    
    print(structure)

def main():
    print_header()
    print_features()
    
    if not check_requirements():
        print("❌ Setup incomplete. Please ensure all files are present.")
        return
    
    show_demo_scenarios()
    show_next_steps()
    show_customization_tips()
    show_file_structure()
    
    print("🎉 Ready to explore advanced swarm robotics!")
    print("💡 Tip: Start with the enhanced_swarm_demo.wbt world")
    print("📚 See ENHANCED_README.md for detailed documentation")
    print()
    print("Happy swarming! 🤖✨")

if __name__ == "__main__":
    main()
