#!/usr/bin/env python3
"""
GitHub Deployment Preparation Script
===================================

This script prepares the Enhanced ChuhaBot Swarm Framework for GitHub deployment
by checking all files, creating necessary configurations, and providing deployment guidance.
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

def print_header():
    """Print deployment preparation header"""
    print("🚀" + "=" * 78 + "🚀")
    print("  ENHANCED CHUHABOT SWARM FRAMEWORK - GITHUB DEPLOYMENT PREP")
    print("🚀" + "=" * 78 + "🚀")
    print()

def check_project_structure() -> Dict[str, bool]:
    """Check if all necessary files exist for deployment"""
    print("📂 CHECKING PROJECT STRUCTURE:")
    print("-" * 50)
    
    required_files = {
        # Core framework files
        "controllers/enhanced_swarm_framework/enhanced_swarm_framework.py": False,
        "controllers/enhanced_swarm_framework/enhanced_chuha_controller.py": False,
        "controllers/enhanced_swarm_framework/hybrid_swarm_framework.py": False,
        "controllers/enhanced_swarm_framework/webots_compat.py": False,
        
        # C controller files
        "controllers/chuha_c_controller/chuha_c_controller.c": False,
        "controllers/chuha_c_controller/Makefile": False,
        "controllers/chuha_c_controller/README.md": False,
        
        # Demo and setup files
        "worlds/enhanced_swarm_demo.wbt": False,
        "requirements.txt": False,
        "setup_enhanced_framework.py": False,
        "demo_enhanced_features.py": False,
        
        # Documentation files
        "ENHANCED_README.md": False,
        "README_GITHUB.md": False,
        "RELEASE_NOTES.md": False,
        "CONTRIBUTING.md": False,
        "GITHUB_DEPLOYMENT_GUIDE.md": False,
        
        # GitHub files
        ".github/workflows/ci.yml": False,
        ".gitignore_new": False,
    }
    
    for file_path in required_files:
        if os.path.exists(file_path):
            required_files[file_path] = True
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
    
    return required_files

def check_file_sizes() -> Dict[str, int]:
    """Check file sizes to ensure they're substantial"""
    print("\n📊 FILE SIZE ANALYSIS:")
    print("-" * 50)
    
    important_files = [
        "controllers/enhanced_swarm_framework/enhanced_swarm_framework.py",
        "controllers/enhanced_swarm_framework/enhanced_chuha_controller.py",
        "controllers/chuha_c_controller/chuha_c_controller.c",
        "README_GITHUB.md",
        "ENHANCED_README.md",
        "RELEASE_NOTES.md"
    ]
    
    file_sizes = {}
    
    for file_path in important_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            file_sizes[file_path] = size
            size_kb = size / 1024
            
            if size_kb > 10:
                status = "✅"
            elif size_kb > 1:
                status = "⚠️"
            else:
                status = "❌"
                
            print(f"  {status} {file_path}: {size_kb:.1f} KB")
        else:
            print(f"  ❌ {file_path}: Not found")
            file_sizes[file_path] = 0
    
    return file_sizes

def create_deployment_checklist():
    """Create a deployment checklist"""
    print("\n📋 DEPLOYMENT CHECKLIST:")
    print("-" * 50)
    
    checklist = [
        "Initialize Git repository (git init)",
        "Copy .gitignore_new to .gitignore",
        "Copy README_GITHUB.md to README.md",
        "Stage all files (git add .)",
        "Create initial commit with descriptive message",
        "Create GitHub repository (web interface or CLI)",
        "Add remote origin (git remote add origin <url>)",
        "Push to main branch (git push -u origin main)",
        "Create v2.0.0 release tag",
        "Create GitHub release with release notes",
        "Configure repository settings and topics",
        "Share with the community!"
    ]
    
    for i, item in enumerate(checklist, 1):
        print(f"  {i:2d}. ⬜ {item}")

def generate_deployment_stats():
    """Generate deployment statistics"""
    print("\n📈 PROJECT STATISTICS:")
    print("-" * 50)
    
    # Count lines of code
    python_files = []
    c_files = []
    md_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.py'):
                python_files.append(file_path)
            elif file.endswith('.c') or file.endswith('.h'):
                c_files.append(file_path)
            elif file.endswith('.md'):
                md_files.append(file_path)
    
    def count_lines(files):
        total_lines = 0
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    total_lines += sum(1 for line in f)
            except:
                pass
        return total_lines
    
    python_lines = count_lines(python_files)
    c_lines = count_lines(c_files)
    md_lines = count_lines(md_files)
    
    print(f"  📄 Python files: {len(python_files)} files, {python_lines:,} lines")
    print(f"  🔧 C files: {len(c_files)} files, {c_lines:,} lines") 
    print(f"  📚 Documentation: {len(md_files)} files, {md_lines:,} lines")
    print(f"  📊 Total project: {python_lines + c_lines + md_lines:,} lines of code/docs")

def create_git_commands():
    """Generate Git commands for deployment"""
    print("\n🔧 GIT DEPLOYMENT COMMANDS:")
    print("-" * 50)
    
    commands = [
        "# 1. Prepare files",
        "copy .gitignore_new .gitignore",
        "copy README_GITHUB.md README.md",
        "",
        "# 2. Initialize and commit",
        "git init",
        "git add .",
        'git commit -m "feat: Enhanced ChuhaBot Swarm Framework v2.0.0"',
        "",
        "# 3. Connect to GitHub (replace 'yourusername')",
        "git remote add origin https://github.com/yourusername/enhanced-chuhabot-swarm.git",
        "git branch -M main",
        "git push -u origin main",
        "",
        "# 4. Create release tag",
        'git tag -a v2.0.0 -m "Enhanced ChuhaBot Swarm Framework v2.0.0"',
        "git push origin --tags"
    ]
    
    for command in commands:
        if command.startswith("#"):
            print(f"  {command}")
        elif command == "":
            print()
        else:
            print(f"  $ {command}")

def check_dependencies():
    """Check if all dependencies are properly documented"""
    print("\n📦 DEPENDENCY CHECK:")
    print("-" * 50)
    
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            deps = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        print(f"  ✅ requirements.txt found with {len(deps)} dependencies:")
        for dep in deps:
            print(f"     - {dep}")
    else:
        print("  ❌ requirements.txt not found")

def main():
    """Main deployment preparation function"""
    print_header()
    
    # Check project structure
    file_status = check_project_structure()
    missing_files = [f for f, exists in file_status.items() if not exists]
    
    # Analyze file sizes
    file_sizes = check_file_sizes()
    
    # Check dependencies
    check_dependencies()
    
    # Generate statistics
    generate_deployment_stats()
    
    # Create deployment checklist
    create_deployment_checklist()
    
    # Generate Git commands
    create_git_commands()
    
    # Final summary
    print("\n🎯 DEPLOYMENT READINESS SUMMARY:")
    print("-" * 50)
    
    total_files = len(file_status)
    ready_files = sum(file_status.values())
    readiness_percent = (ready_files / total_files) * 100
    
    print(f"  📊 Files ready: {ready_files}/{total_files} ({readiness_percent:.1f}%)")
    
    if missing_files:
        print(f"  ⚠️  Missing files: {len(missing_files)}")
        for file in missing_files[:3]:  # Show first 3 missing files
            print(f"     - {file}")
        if len(missing_files) > 3:
            print(f"     ... and {len(missing_files) - 3} more")
    
    if readiness_percent >= 90:
        print("  🎉 PROJECT IS READY FOR GITHUB DEPLOYMENT!")
        print("  📋 Follow the deployment checklist above")
        print("  📖 See GITHUB_DEPLOYMENT_GUIDE.md for detailed instructions")
    elif readiness_percent >= 75:
        print("  ⚠️  PROJECT IS MOSTLY READY - address missing files")
    else:
        print("  ❌ PROJECT NEEDS MORE WORK BEFORE DEPLOYMENT")
    
    print("\n🚀 NEXT STEPS:")
    print("-" * 50)
    print("  1. 📖 Read GITHUB_DEPLOYMENT_GUIDE.md")
    print("  2. 🔧 Follow the Git commands above")
    print("  3. 🌐 Create GitHub repository")
    print("  4. 📤 Push your amazing swarm framework!")
    print("  5. 🎊 Share with the robotics community!")
    
    print("\n" + "🤖" + "=" * 76 + "🤖")
    print("  READY TO REVOLUTIONIZE SWARM ROBOTICS ON GITHUB!")
    print("🤖" + "=" * 76 + "🤖")

if __name__ == "__main__":
    main()
