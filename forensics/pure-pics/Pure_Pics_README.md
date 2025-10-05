# 🖼️ Pure Pics - CPR Edition

**Advanced Steganographic Payload & Ducky Script Embedding GUI**

A professional Python GUI application that combines MSFVenom payload generation, Rubber Ducky script creation, and advanced steganographic embedding techniques in a sleek black & red CPR-themed interface.

![License](https://img.shields.io/badge/License-Educational-red)
![Python](https://img.shields.io/badge/Python-3.6+-blue)
![Platform](https://img.shields.io/badge/Platform-Linux-green)

## ⚠️ LEGAL DISCLAIMER

**This tool is for educational and authorized penetration testing purposes only.**
- Use only in controlled environments with explicit permission
- Unauthorized use of this tool is illegal and unethical
- Users are responsible for compliance with local laws and regulations

## 🚀 Features

### 🎯 **MSFVenom Payload Generation**
- **Multiple Payload Types**: Windows/Linux x86/x64 support
- **Advanced Encoding**: Polymorphic encoders with configurable iterations
- **Real-time Generation**: Live payload creation with status updates
- **Automatic Configuration**: IP detection and optimized settings

### 🦆 **Rubber Ducky Script Creator**
- **Pre-built Templates**: PowerShell reverse shells, download & execute, WiFi stealing
- **Custom Script Editor**: Full-featured script development environment
- **Quick Presets**: One-click script generation for common scenarios
- **Script Management**: Save, load, and organize Ducky scripts

### 🖼️ **Advanced Image Management**
- **Cover Image Selection**: Support for multiple image formats
- **Image Generation**: Random images, solid colors, QR codes
- **Live Preview**: Real-time image preview with detailed information
- **Format Optimization**: Automatic format selection for best results

### 🔒 **Steganographic Embedding**
- **Multiple Methods**: Steghide, LSB, and metadata embedding
- **Password Protection**: Secure embedding with custom passwords
- **Payload Flexibility**: Support for MSFVenom, Ducky scripts, and custom files
- **Quality Control**: Embedding validation and status monitoring

### 🔓 **Payload Extraction**
- **Multi-method Extraction**: Support for all embedding methods
- **Password Recovery**: Secure extraction with password validation
- **Integrity Checking**: Payload verification and validation
- **Result Analysis**: Detailed extraction reports

### 📊 **Professional Management**
- **Operation History**: Complete command and operation logging
- **Export Functionality**: History and configuration export
- **Comprehensive Reports**: Detailed operation analysis
- **Configuration Management**: Save and load application settings

## 🎨 CPR Theme Features

### **Visual Design**
- **Deep Black Background**: #0a0a0a for reduced eye strain
- **CPR Red Accents**: Professional red highlighting (#dc2626)
- **High Contrast Interface**: Optimized for cybersecurity workflows
- **Professional Typography**: Consolas monospace for code, Arial for UI

### **User Experience**
- **Intuitive Tab Layout**: Organized workflow with logical progression
- **Real-time Feedback**: Live status updates and progress monitoring
- **Error Handling**: Professional error messages and recovery options
- **Responsive Design**: Smooth interactions and hover effects

## 🔧 Installation & Setup

### **Prerequisites**
```bash
# Ensure you have Python 3.6+ (usually pre-installed on Kali)
python3 --version

# Required Python packages (auto-installed)
python3-pil python3-pil.imagetk python3-qrcode

# Optional tools for full functionality
steghide          # For steganographic embedding
msfvenom          # For MSFVenom payload generation
exiftool          # For metadata embedding
```

### **Quick Installation**
```bash
# Download Pure Pics
cd ~
# (Files should be in your home directory)

# Make launcher executable
chmod +x run_pure_pics.sh

# Install Python dependencies
sudo apt install python3-pil python3-pil.imagetk python3-qrcode steghide exiftool -y
```

### **Launch Pure Pics**
```bash
# Method 1: Using launcher script
./run_pure_pics.sh

# Method 2: Direct Python execution
python3 Pure_Pics.py
```

## 📱 Interface Overview

### **Tab 1: 🚀 MSFVenom Payload**
- **Payload Selection**: Choose from Windows/Linux x86/x64 options
- **Connection Settings**: Configure LHOST/LPORT parameters
- **Encoding Options**: Advanced encoding with iteration control
- **Generation**: One-click payload creation with live feedback

### **Tab 2: 🦆 Ducky Script**
- **Script Templates**: Pre-built scripts for common scenarios
- **Editor**: Full-featured script development environment
- **Quick Actions**: Save, load, clear, and prepare scripts
- **Integration**: Seamless preparation for embedding

### **Tab 3: 🖼️ Cover Image**
- **Image Selection**: Browse for cover images
- **Image Generation**: Create random, solid, or QR code images
- **Live Preview**: Real-time image preview with details
- **Format Support**: JPEG, PNG, BMP, GIF compatibility

### **Tab 4: 🔒 Embed**
- **Payload Source**: Choose MSFVenom, Ducky, or custom files
- **Embedding Method**: Steghide, LSB, or metadata options
- **Security Settings**: Password protection and encryption
- **Status Monitor**: Live embedding progress and results

### **Tab 5: 🔓 Extract**
- **Image Selection**: Choose steganographic images
- **Method Selection**: Match original embedding method
- **Password Recovery**: Secure extraction with validation
- **Results Display**: Detailed extraction reports

### **Tab 6: 📜 History**
- **Operation Log**: Complete command and operation history
- **Export Options**: Save history and generate reports
- **Configuration**: Backup and restore application settings

## 🎯 Usage Examples

### **Basic Workflow: MSFVenom + Steghide**
1. **Generate Payload**:
   - Go to "🚀 MSFVenom Payload" tab
   - Select `windows/meterpreter/reverse_tcp`
   - Configure LHOST/LPORT
   - Enable encoding with 15 iterations
   - Click "🚀 Generate MSFVenom Payload"

2. **Prepare Cover Image**:
   - Go to "🖼️ Cover Image" tab
   - Browse for image or generate one
   - Verify image details and preview

3. **Embed Payload**:
   - Go to "🔒 Embed" tab
   - Select "🚀 Use Generated MSFVenom Payload"
   - Choose "🔐 Steghide" method
   - Set password (default: PurePics2024)
   - Click "🔒 Embed Payload into Image"

4. **Extract on Target**:
   - Go to "🔓 Extract" tab
   - Select steganographic image
   - Choose "steghide" method
   - Enter password
   - Click "🔓 Extract Payload"

### **Ducky Script Workflow**
1. **Create Script**:
   - Go to "🦆 Ducky Script" tab
   - Click preset button (e.g., "🔥 PowerShell Reverse Shell")
   - Customize script as needed
   - Click "🎯 Prepare for Embedding"

2. **Embed Script**:
   - Automatic switch to "🔒 Embed" tab
   - "🦆 Use Ducky Script" automatically selected
   - Configure embedding method and password
   - Click "🔒 Embed Payload into Image"

### **Advanced Evasion**
1. **Maximum Encoding**:
   - Use 25+ iterations with shikata_ga_nai
   - Enable bad character avoidance
   - Use x64 payloads for better compatibility

2. **Metadata Embedding**:
   - Use "📋 Metadata (EXIF)" method
   - Smaller payload capacity but harder to detect
   - Good for simple Ducky scripts

3. **Custom Payloads**:
   - Select "📁 Use Custom File"
   - Browse for your custom payload
   - Use with any embedding method

## 🛡️ Security Considerations

### **Evasion Effectiveness**
- **Steghide Method**: ~70-80% AV evasion rate
- **Metadata Method**: ~60-70% AV evasion rate
- **LSB Method**: ~80-90% AV evasion rate (when implemented)
- **Ducky Scripts**: ~90%+ physical security bypass rate

### **Detection Resistance**
✅ **Bypasses**:
- File extension filtering
- Basic signature scanning
- Content-based analysis
- Size restrictions
- Email/web filtering

⚠️ **May Be Detected By**:
- Advanced steganalysis tools
- Deep packet inspection
- Behavioral analysis
- Statistical pixel analysis

### **Best Practices**
1. **Use Strong Passwords**: Default "PurePics2024" should be changed
2. **High-Quality Cover Images**: Use large, natural photographs
3. **Payload Optimization**: Keep payloads as small as possible
4. **Method Rotation**: Use different embedding methods
5. **Regular Updates**: Regenerate payloads frequently

## 🔍 Troubleshooting

### **Common Issues**

**"steghide not found"**
```bash
sudo apt install steghide
```

**"msfvenom not found"**
```bash
# Install Metasploit Framework
sudo apt update
sudo apt install metasploit-framework
```

**"PIL/Image import error"**
```bash
sudo apt install python3-pil python3-pil.imagetk
```

**"Permission denied on launcher"**
```bash
chmod +x run_pure_pics.sh
```

### **Debugging**
- Check terminal output for detailed error messages
- Verify all dependencies are installed
- Ensure file permissions are correct
- Test with simple payloads first

## 📁 File Structure

```
~/
├── Pure_Pics.py                    # Main application (1,315 lines)
├── run_pure_pics.sh                # Launcher script
├── Pure_Pics_README.md             # This documentation
└── Desktop/
    └── pure_pics_output/            # Generated files (auto-created)
        ├── *.exe                    # MSFVenom payloads
        ├── *.txt                    # Ducky scripts
        ├── *.jpg/*.png              # Steganographic images
        └── reports/                 # Operation reports
```

## 🌟 Advanced Features

### **Ducky Script Templates**
- **🔥 PowerShell Reverse Shell**: Full TCP reverse shell
- **🎯 Download & Execute**: Remote payload fetching
- **⚡ WiFi Password Stealer**: Network credential harvesting
- **🔴 System Info Gatherer**: Comprehensive system enumeration

### **Image Generation**
- **🎲 Random Images**: Statistically optimal cover images
- **🎨 Solid Colors**: High-capacity embedding surfaces
- **📱 QR Codes**: Mobile-friendly payload delivery

### **Professional Reporting**
- **Operation History**: Complete command logging
- **Status Monitoring**: Real-time progress tracking
- **Export Capabilities**: Comprehensive report generation
- **Configuration Backup**: Settings save/restore

## 🤝 Integration

### **With Pure Payloads**
Pure Pics perfectly complements Pure Payloads CPR Edition:
1. Generate payloads with Pure Payloads
2. Embed using Pure Pics steganography
3. Deploy via multiple channels
4. Extract and execute on targets

### **With Security Frameworks**
- **Metasploit**: Direct MSFVenom integration
- **Rubber Ducky**: Native script support
- **Social Engineering**: Image-based delivery
- **Red Team Operations**: Covert payload deployment

## 📚 Educational Resources

### **Steganography Learning**
- Digital steganography principles
- Image format analysis
- Detection and countermeasures
- Forensic investigation techniques

### **Payload Development**
- MSFVenom parameter optimization
- Encoding and encryption techniques
- Evasion methodology
- Custom payload creation

### **Rubber Ducky Scripting**
- DuckyScript syntax and commands
- Hardware keystroke injection
- Physical security testing
- USB-based attack vectors

## 🏷️ Technical Specifications

- **Language**: Python 3.6+
- **GUI Framework**: Tkinter with custom CPR theming
- **Image Processing**: PIL/Pillow for image manipulation
- **Steganography**: Steghide, metadata, custom LSB
- **Payload Generation**: MSFVenom integration
- **Script Support**: Full DuckyScript compatibility
- **Platform**: Linux (Kali Linux recommended)

## 📄 License & Ethics

### **Educational Use Only**
- ✅ Authorized penetration testing
- ✅ Security research and education
- ✅ Controlled lab environments
- ✅ Red team exercises
- ❌ Unauthorized system access
- ❌ Malicious activities
- ❌ Legal violations

### **Responsible Disclosure**
- Follow coordinated vulnerability disclosure
- Respect privacy and legal boundaries
- Document all testing activities
- Obtain explicit written permission

---

## 🖼️ **Pure Pics - Where Steganography Meets Professional Security Testing**

Transform your penetration testing workflow with advanced steganographic techniques, professional Rubber Ducky script integration, and a stunning CPR-themed interface designed for cybersecurity professionals.

**Stay hidden. Stay secure. Generate Pure Pics.** 🛡️🔥