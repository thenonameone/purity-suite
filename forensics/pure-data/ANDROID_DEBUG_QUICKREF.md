# Android USB Debugging Quick Reference

## 🚀 Quick Start Commands

After restarting your shell or running `source ~/.zshrc`:

### Basic Recovery Tools
```bash
recovery help                    # Main data recovery toolkit
recovery list-devices           # Show connected storage devices
recovery list-android           # Show connected Android devices
recovery extract-android "case" # Extract Android device data
```

### Android Debugging Tools
```bash
android-debug                   # Interactive debugging enabler menu
android-debug auto             # Try all methods automatically
android-debug help             # Show detailed help
```

### Bootloader & Recovery Tools  
```bash
bootloader-tools                      # Show available commands
bootloader-tools check-fastboot       # Check fastboot connection
bootloader-tools bootloader-info      # Get bootloader information
bootloader-tools device-report        # Generate device report
```

## 📋 Method Success Matrix

| Device State | ADB Method | Root Method | Fastboot | Recovery | Hardware |
|--------------|------------|-------------|----------|----------|----------|
| **Screen Unlocked** | ✅ High | ⚠️ If Rooted | ❌ No | ❌ No | ✅ Yes |
| **Screen Locked** | ❌ No | ❌ No | ⚠️ If Unlocked | ⚠️ If Custom | ✅ Yes |
| **Bootloader Unlocked** | ❌ No | ❌ No | ✅ High | ✅ High | ✅ Yes |
| **Bootloader Locked** | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes |

## 🔧 Method Selection Guide

### 1. Device is ON and Accessible
```bash
# Try basic ADB first
adb devices
android-debug adb

# If rooted
android-debug root
```

### 2. Device is ON but Locked
```bash
# Try physical access methods
android-debug physical

# Boot into fastboot mode:
# Power + Volume Down (most devices)
bootloader-tools check-fastboot
```

### 3. Device in Fastboot Mode
```bash
bootloader-tools bootloader-info
bootloader-tools unlock-bootloader  # DANGEROUS: Wipes data!
```

### 4. Custom Recovery Available
```bash
# Boot into recovery: Power + Volume Up
bootloader-tools check-recovery
bootloader-tools enable-debug-recovery
```

## ⚖️ Legal Checklist

**Before using ANY method, verify:**
- [ ] You own the device OR have explicit legal authorization
- [ ] You understand the risks and limitations
- [ ] You have read the legal guidelines in `LEGAL_ETHICAL_GUIDELINES.md`
- [ ] You have proper forensic documentation procedures
- [ ] You are complying with local laws and regulations

## 🛠️ Common Workflows

### Personal Device Recovery
```bash
# 1. Try to get ADB access
android-debug auto

# 2. If successful, extract data
recovery extract-android "my-device-recovery"

# 3. Generate report
recovery generate-report "my-device-recovery"
```

### Forensic Investigation
```bash
# 1. Document device state
bootloader-tools device-report

# 2. Try least invasive methods first
android-debug adb

# 3. Escalate to hardware methods if necessary
# (Requires specialized equipment and training)
```

### Corporate Device Management
```bash
# 1. Verify authorization and policies
# 2. Enable debugging via appropriate method
android-debug root  # If devices are rooted

# 3. Extract corporate data
recovery extract-android "corporate-device-001"
```

## 🔍 Troubleshooting

### Device Not Detected
```bash
# Check USB connection and drivers
lsusb
adb devices
fastboot devices

# Restart ADB server
adb kill-server
adb start-server

# Check USB debugging status
adb shell getprop ro.adb.secure
```

### Permission Errors
```bash
# Fix recovery directory permissions
sudo chown -R $USER:$USER ~/data-recovery/

# Add user to plugdev group (if needed)
sudo usermod -a -G plugdev $USER
```

### Bootloader Issues
```bash
# Check bootloader status
fastboot getvar unlocked
fastboot getvar secure

# Try different unlock commands
fastboot oem unlock
fastboot flashing unlock
```

## 📊 Success Rates by Android Version

| Android Version | Software Methods | Hardware Methods |
|-----------------|------------------|------------------|
| **Android 4.x** | 🟢 High (70-90%) | 🟢 High (90%+) |
| **Android 5-6** | 🟡 Medium (40-70%) | 🟢 High (85%+) |
| **Android 7-8** | 🟡 Low (20-40%) | 🟡 Medium (70%+) |
| **Android 9+** | 🔴 Very Low (5-20%) | 🟡 Medium (60%+) |

## 🎯 Tool Effectiveness

### Software-Based Methods
- **ADB Method**: Works only if debugging already partially enabled
- **Root Method**: Highly effective but requires prior root access
- **Fastboot Method**: Good for unlocked bootloaders
- **Recovery Method**: Effective with custom recovery installed
- **Exploit Methods**: Limited to older Android versions

### Hardware-Based Methods
- **UART Access**: High success rate, requires soldering skills
- **JTAG Access**: Professional level, expensive equipment
- **Chip-off**: Last resort, destructive, 90%+ success rate
- **ISP Programming**: Direct flash access, very high success

## 🚨 Risk Levels

| Method | Data Loss Risk | Device Damage Risk | Legal Risk |
|--------|----------------|-------------------|------------|
| **ADB** | 🟢 None | 🟢 None | 🟢 Low |
| **Root** | 🟡 Low | 🟡 Low | 🟡 Medium |
| **Fastboot** | 🔴 High | 🟡 Low | 🟡 Medium |
| **Recovery** | 🟡 Medium | 🟡 Low | 🟡 Medium |
| **Hardware** | 🟡 Medium | 🔴 High | 🔴 High |

## 📚 Additional Resources

### Documentation Files
- `DATA_RECOVERY_GUIDE.md` - Complete recovery procedures
- `LEGAL_ETHICAL_GUIDELINES.md` - Legal and ethical considerations  
- `HARDWARE_FORENSIC_METHODS.md` - Professional hardware techniques

### Tool Locations
- Main toolkit: `~/data-recovery/tools/recovery-toolkit.sh`
- Debug enabler: `~/data-recovery/tools/android-debug-enabler.sh`
- Bootloader tools: `~/data-recovery/tools/bootloader-recovery-tools.py`

### Professional Training
- **SANS FOR585** - Smartphone Forensic Analysis
- **Cellebrite Certified** - Mobile forensics certification
- **CHFI** - Computer Hacking Forensic Investigator
- **Local workshops** - Electronics and soldering training

## ⚡ Emergency Procedures

### If Device Becomes Unresponsive
1. **Disconnect USB cable immediately**
2. **Power off device** (hold power button 10+ seconds)
3. **Document what happened** in detail
4. **Try recovery mode** (Power + Volume combinations)
5. **Contact professional service** if critical data

### If Legal Issues Arise
1. **Stop all activities immediately**
2. **Preserve all documentation**
3. **Contact legal counsel**  
4. **Cooperate with investigations**
5. **Review procedures and training**

---

## 🎯 Remember

**Always start with the least invasive method and escalate only if necessary.**

The tools provided give you multiple approaches for legitimate Android device debugging and data recovery. Success rates depend heavily on device model, Android version, and security patches.

For mission-critical or high-value data recovery, consider professional forensic services with proper certifications and legal procedures.