# Enhanced ChuhaBot Swarm Framework

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.6%2B-green.svg)](https://www.python.org/)
[![C](https://img.shields.io/badge/C-C99-blue.svg)](https://en.wikipedia.org/wiki/C99)
[![Webots](https://img.shields.io/badge/Webots-R2024a%2B-orange.svg)](https://cyberbotics.com/)
[![GitHub Release](https://img.shields.io/github/v/release/StuxnetStudios/enhanced-chuhabot-swarm?color=brightgreen)](https://github.com/StuxnetStudios/enhanced-chuhabot-swarm/releases)
[![GitHub Stars](https://img.shields.io/github/stars/StuxnetStudios/enhanced-chuhabot-swarm?style=social)](https://github.com/StuxnetStudios/enhanced-chuhabot-swarm)

> **Next-generation intelligent swarm robotics framework with dual Python/C implementation**

A comprehensive, modular, and high-performance swarm robotics framework that transforms the original ChuhaBot project into an intelligent, adaptive system with both Python and C implementations.

## 🚀 Features

### 🧠 **Intelligent Python Framework**
- **Adaptive Behaviors**: Auto-tuning detection parameters
- **Machine Learning**: Formation quality-based optimization  
- **Mission Modes**: Exploration, Formation, Following, Patrol, Search
- **Emergency Systems**: Collision detection and avoidance
- **Smart Visualization**: Force vectors, formation quality, color coding

### ⚡ **High-Performance C Controller**
- **Real-time Execution**: <0.1ms per control step
- **Memory Efficient**: ~2KB fixed allocation
- **Native Integration**: Direct Webots C API
- **Core Behaviors**: Separation, Alignment, Cohesion, Obstacle Avoidance

### 🎯 **Advanced Capabilities**
- **Cross-platform Support**: ChuhaBot + e-puck robots
- **Modular Architecture**: Extensible behavior system
- **Dynamic Adaptation**: Real-time parameter adjustment
- **Performance Metrics**: Comprehensive tracking and analysis

## 📦 Quick Start

### Prerequisites
- [Webots](https://cyberbotics.com/) R2024a or later
- Python 3.6+ with pip
- C compiler (optional, for C controller)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/StuxnetStudios/enhanced-chuhabot-swarm.git
cd enhanced-chuhabot-swarm
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify setup**
```bash
python setup_enhanced_framework.py
```

4. **Run demo**
```bash
python demo_enhanced_features.py
```

### Usage in Webots

1. **Open Webots**
2. **Load world**: `File → Open World → worlds/enhanced_swarm_demo.wbt`
3. **Set controller**: Select robot → Controller → `enhanced_chuha_controller`
4. **Start simulation**: Play button or Ctrl+1
5. **Watch intelligent swarm behaviors!**

## 🎮 Demo Scenarios

### 🔍 **Intelligent Exploration**
Robots autonomously explore with auto-tuning detection and obstacle avoidance
- **Duration**: Continuous operation
- **Features**: Dynamic parameter adjustment, coverage optimization

### ⭕ **Adaptive Formation Control**
Dynamic formation maintenance with quality monitoring
- **Formations**: Circle, Line, V-shape
- **Features**: Quality assessment, automatic adaptation

### 🚨 **Emergency Behaviors**
Collision avoidance and safety response demonstration
- **Features**: Emergency separation, safe navigation

## 📊 Performance Comparison

| Feature | Python Framework | C Framework |
|---------|------------------|-------------|
| **Execution Speed** | 1-5ms/step | ~0.1ms/step |
| **Memory Usage** | 10-50MB | ~2KB |
| **AI Features** | ✅ Full Suite | ❌ Basic |
| **Development Speed** | ✅ Fast | ⚠️ Moderate |
| **Real-time** | ✅ Good | ✅ Excellent |

## 🛠️ Development

### Python Framework Development
```bash
# Edit behavior weights
nano controllers/enhanced_swarm_framework/enhanced_chuha_controller.py

# Add custom behaviors
# Extend SwarmBehavior class in enhanced_swarm_framework.py
```

### C Framework Development
```bash
# Navigate to C controller
cd controllers/chuha_c_controller

# Build (Unix/Linux/Mac)
make

# Build (Windows)
.\build.ps1 build
```

## 📁 Project Structure

```
enhanced-chuhabot-swarm/
├── controllers/
│   ├── enhanced_swarm_framework/     # 🐍 Python Framework
│   │   ├── enhanced_swarm_framework.py
│   │   ├── enhanced_chuha_controller.py
│   │   ├── hybrid_swarm_framework.py
│   │   └── webots_compat.py
│   ├── chuha_c_controller/          # 🔥 C Framework  
│   │   ├── chuha_c_controller.c
│   │   ├── Makefile
│   │   └── README.md
│   └── swarm_basic_flocking/        # 🔄 Original ChuhaBot
├── worlds/
│   └── enhanced_swarm_demo.wbt     # Demo world
├── protos/                         # Robot definitions
├── docs/                          # Documentation
└── requirements.txt               # Python dependencies
```

## 🎯 Use Cases

### **Research & Academia**
- Multi-robot coordination studies
- Swarm intelligence algorithms
- Machine learning integration
- Educational demonstrations

### **Industry & Production**
- Real-time swarm control systems
- Autonomous exploration missions
- Formation flying applications
- Emergency response robotics

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Complete installation instructions
- **[API Reference](docs/API.md)** - Behavior system documentation
- **[Examples](docs/EXAMPLES.md)** - Usage examples and tutorials
- **[C Controller Guide](controllers/chuha_c_controller/README.md)** - C implementation details

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original ChuhaBot project by [aniruddhkb](https://github.com/aniruddhkb/swarm_robotics_webots)
- Webots robotics simulator by [Cyberbotics](https://cyberbotics.com/)
- Research community for swarm robotics algorithms

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/StuxnetStudios/enhanced-chuhabot-swarm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/StuxnetStudios/enhanced-chuhabot-swarm/discussions)
- **Documentation**: [Wiki](https://github.com/StuxnetStudios/enhanced-chuhabot-swarm/wiki)

---

**🚀 Ready to revolutionize swarm robotics? Get started today!** 🤖✨
