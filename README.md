# VPN Blocking Network Simulation

[![OMNeT++](https://img.shields.io/badge/OMNeT%2B%2B-6.0.3-blue.svg)](https://omnetpp.org/)
[![INET Framework](https://img.shields.io/badge/INET-4.5-green.svg)](https://inet.omnetpp.org/)
[![License](https://img.shields.io/badge/license-Academic-orange.svg)](LICENSE)

A network simulation project built with OMNeT++ that demonstrates VPN traffic detection and blocking mechanisms in a firewall/gateway router environment.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Results Analysis](#results-analysis)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project simulates a network environment where a client attempts to establish VPN connections through a gateway/firewall to reach a blocked server. The simulation implements VPN detection mechanisms to identify and block different types of VPN traffic including IPsec, OpenVPN, and PPTP protocols.

### Key Components:
- **VPN Traffic Generator**: Simulates VPN client traffic with configurable protocols
- **VPN Detector**: Analyzes packets to detect VPN signatures and patterns
- **Firewall Router**: Gateway with integrated VPN detection capabilities
- **Network Topology**: Client → Gateway/Firewall → Blocked Server

## ✨ Features

- **Multiple VPN Protocol Detection**:
  - IPsec (ESP protocol detection)
  - OpenVPN (port-based detection on UDP 1194)
  - PPTP (port-based detection on TCP 1723)

- **Configurable Traffic Patterns**:
  - Adjustable packet sizes (default: 1200 bytes)
  - Exponential inter-arrival times (configurable mean)
  - Simulation time control

- **Comprehensive Logging**:
  - CSV-based packet logging (`vpn_detection_log.csv`)
  - Real-time statistics collection
  - Vector and scalar result files for analysis

- **Multiple Simulation Scenarios**:
  - IPsec blocking configuration
  - OpenVPN blocking configuration
  - No blocking baseline
  - High traffic load testing
  - Long-duration statistical analysis

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Client    │────────▶│ Firewall/Gateway │────────▶│ Blocked Server  │
│             │         │  with VPN        │         │                 │
│ VPNTraffic  │  VPN    │  Detector        │ Filtered│  UdpBasicApp    │
│    App      │ Traffic │                  │ Traffic │                 │
└─────────────┘         └──────────────────┘         └─────────────────┘
  192.168.1.10           192.168.1.1/10.0.0.1           10.0.0.10
```

### Network Details:
- **Link Type**: Ethernet (100 Mbps, 0.1μs delay)
- **Client Subnet**: 192.168.1.0/24
- **Server Subnet**: 10.0.0.0/24
- **Protocol**: UDP (default port 5000)

## 📦 Requirements

### Software Requirements:
- **OMNeT++ 6.0.3** or later
- **INET Framework 4.5** or later
- **C++ Compiler**: MinGW (Windows) or GCC/Clang (Linux/macOS)
- **Python 3.x** (optional, for result analysis scripts)

### System Requirements:
- Operating System: Windows 10/11, Linux, or macOS
- RAM: 4 GB minimum, 8 GB recommended
- Disk Space: 2 GB for OMNeT++ and project files

## 🚀 Installation

### 1. Install OMNeT++

Download and install OMNeT++ 6.0.3 from [omnetpp.org](https://omnetpp.org/):

```bash
# Extract OMNeT++
cd omnetpp-6.0.3

# Configure environment (Windows)
mingwenv.cmd

# Configure environment (Linux/macOS)
./configure
make
```

### 2. Install INET Framework

```bash
cd omnetpp-6.0.3/samples
git clone https://github.com/inet-framework/inet.git inet4.5
cd inet4.5
git checkout v4.5.0
make makefiles
make MODE=release
```

### 3. Clone and Build VPNBlocking Project

```bash
cd omnetpp-6.0.3/samples
git clone https://github.com/Ashsifat1511/VPNBlocking.git
cd VPNBlocking

# Generate Makefile
opp_makemake --deep -O out -I../inet4.5/src -I. -L../inet4.5/src -lINET -f

# Build the project
make MODE=debug
# or
make MODE=release
```

## 🎮 Usage

### Running from OMNeT++ IDE

1. Import the project into OMNeT++ IDE
2. Right-click `omnetpp.ini` → **Run As** → **OMNeT++ Simulation**
3. Select a configuration (e.g., `IPsecBlocking`)
4. Choose GUI mode (Qtenv) or command-line mode (Cmdenv)

### Running from Command Line

```bash
# Run with default configuration
./VPNBlocking_dbg.exe

# Run specific configuration
./VPNBlocking_dbg.exe -c IPsecBlocking

# Run in GUI mode
./VPNBlocking_dbg.exe -u Qtenv

# Run in command-line mode (faster)
./VPNBlocking_dbg.exe -u Cmdenv
```

## ⚙️ Configuration

### Available Configurations in `omnetpp.ini`:

| Configuration | Description | Key Parameters |
|---------------|-------------|----------------|
| **Default** | Standard VPN blocking | 100s duration, IPsec enabled |
| **IPsecBlocking** | Focus on IPsec detection | simulateIPsec = true |
| **OpenVPNBlocking** | OpenVPN port detection | destPort = 1194 |
| **NoBlocking** | Baseline without blocking | All detection disabled |
| **HighTraffic** | High load testing | 0.1s interval, 1500B packets |
| **LongSimulation** | Extended statistics | 500s duration |

### Key Parameters:

```ini
# Simulation duration
sim-time-limit = 100s

# Traffic timing
**.client.app[0].startTime = 1s
**.client.app[0].stopTime = 90s
**.client.app[0].sendInterval = exponential(0.5s)

# Packet configuration
**.client.app[0].packetLength = 1200B
**.client.app[0].simulateIPsec = true

# Network bandwidth
**.client.eth[*].bitrate = 100Mbps
```

### Customizing Parameters:

Edit `omnetpp.ini` to modify:
- **Packet size**: Change `packetLength` (e.g., `1500B`)
- **Traffic rate**: Adjust `sendInterval` (e.g., `exponential(0.2s)`)
- **Simulation time**: Modify `sim-time-limit` (e.g., `200s`)
- **VPN type**: Toggle `simulateIPsec` or change `destPort`

## 📊 Results Analysis

### Using OMNeT++ IDE Analysis Tool

1. Open the **Analysis Tool** (Window → Show View → Analysis)
2. Load result files from `results/` directory
3. Open `analysis.anf` for pre-configured charts:
   - Client Packets Sent vs Server Received
   - VPN Detector Statistics
   - Network Traffic Summary
   - MAC Layer Statistics
   - End-to-End Traffic Flow

### Using Python Script

```bash
python analyze_results.py
```

This generates:
- Console output with statistics summary
- PNG charts in `results/` directory

### Result Files

- **`.sca` files**: Scalar statistics (packet counts, averages)
- **`.vec` files**: Vector data (time-series)
- **`vpn_detection_log.csv`**: Detailed packet-level logs

### Key Metrics:

| Metric | Description |
|--------|-------------|
| `packetsSent` | Total packets sent by VPN client |
| `packetsReceived` | Packets processed by VPN detector |
| `packetsBlocked` | VPN packets blocked by firewall |
| `packetsForwarded` | Legitimate packets forwarded |
| `blockingRate` | Percentage of packets blocked |

## 📁 Project Structure

```
VPNBlocking/
├── README.md                    # This file
├── LICENSE                      # Project license
├── omnetpp.ini                  # Simulation configuration
├── package.ned                  # NED package declaration
├── Makefile                     # Build configuration
│
├── *.ned                        # Network description files
│   ├── VPNBlockNetwork.ned     # Main network topology
│   ├── FirewallRouter.ned      # Custom router with VPN detector
│   ├── VPNDetector.ned         # VPN detection module
│   └── VPNTrafficApp.ned       # VPN traffic generator
│
├── *.cc / *.h                   # C++ source files
│   ├── VPNDetector.cc/h        # VPN detection logic
│   └── VPNTrafficApp.cc/h      # VPN traffic generation
│
├── analysis.anf                 # Analysis configuration
├── analyze_results.py           # Python analysis script
├── vpn_detection_log.csv        # Packet log file
│
├── results/                     # Simulation results
│   ├── *.sca                   # Scalar results
│   ├── *.vec                   # Vector results
│   └── *.vci                   # Vector index files
│
└── out/                         # Build output directory
    └── gcc-debug/              # Compiled object files
```

## 🔬 Implementation Details

### VPN Detection Mechanisms:

1. **Protocol-based Detection**:
   - Checks IP protocol field for ESP (protocol 50)
   - Identifies IPsec tunnel mode traffic

2. **Port-based Detection**:
   - OpenVPN: UDP port 1194
   - PPTP: TCP port 1723
   - Custom port ranges configurable

3. **Statistical Analysis**:
   - Packet size distribution
   - Traffic pattern recognition
   - Threshold-based classification

### Module Descriptions:

- **VPNTrafficApp**: Generates UDP traffic simulating VPN connections with IPsec encapsulation
- **VPNDetector**: Analyzes incoming packets for VPN signatures and makes blocking decisions
- **FirewallRouter**: Extended INET Router with integrated VPN detection capability

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

### Development Setup:

```bash
# Clone the repository
git clone https://github.com/Ashsifat1511/VPNBlocking.git
cd VPNBlocking

# Create development branch
git checkout -b dev

# Make changes and test
make clean
make MODE=debug
./VPNBlocking_dbg.exe -u Cmdenv
```

## 📝 License

This project is licensed under the Academic Public License - see the [LICENSE](LICENSE) file for details.

**Note**: This project is for educational and research purposes only. Not for commercial use.

## 👥 Authors

- **Md Ashrarul Haque Sifat**  - [Ashsifat1511](https://github.com/Ashsifat1511)

## 🙏 Acknowledgments

- OMNeT++ Discrete Event Simulator team
- INET Framework contributors
- Network security research community

## 📧 Contact

For questions or support, please open an issue on GitHub or contact:
- Email: sifatashrarul@gmail.com
- GitHub: [@Ashsifat1511](https://github.com/Ashsifat1511)

## 📚 References

1. [OMNeT++ Documentation](https://omnetpp.org/documentation)
2. [INET Framework Documentation](https://inet.omnetpp.org/docs)
3. VPN Protocol Specifications (RFC 4301 - IPsec, RFC 2637 - PPTP)

---

**⭐ Star this repository if you find it helpful!**
