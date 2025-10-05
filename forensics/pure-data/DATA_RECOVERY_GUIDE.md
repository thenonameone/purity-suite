# Data Recovery Toolkit Guide

## Overview

This toolkit provides comprehensive data recovery capabilities for both hard drives and mobile devices. All tools are pre-installed on your Kali Linux system.

## Directory Structure

```
~/data-recovery/
├── disk-images/     # Disk images created with ddrescue
├── recovered-data/  # Files recovered by various tools
├── mobile-data/     # Mobile device extractions
├── logs/            # Operation logs
├── cases/           # Case-specific information and reports
└── tools/           # Recovery scripts and utilities
```

## Installed Tools

### Hard Drive Recovery Tools
- **TestDisk** - Partition recovery and repair
- **PhotoRec** - File recovery by signature analysis
- **ddrescue** - Creates bit-by-bit disk images
- **Foremost** - File carving utility  
- **Scalpel** - Advanced file carving
- **Autopsy** - Digital forensics platform

### Mobile Device Tools
- **ADB** - Android Debug Bridge for Android devices
- **libimobiledevice** - iOS device communication tools
- **ideviceinfo** - iOS device information
- **idevicebackup2** - iOS backup creation

## Quick Start Guide

### 1. List Connected Devices
```bash
~/data-recovery/tools/recovery-toolkit.sh list-devices
```

### 2. Create Disk Image (CRITICAL FIRST STEP)
```bash
# Always create an image first to avoid further damage
~/data-recovery/tools/recovery-toolkit.sh create-image /dev/sdb "my-case-name"
```

### 3. Run File Recovery
```bash
# Use the disk image, not the original device
~/data-recovery/tools/recovery-toolkit.sh photorec /home/xx/data-recovery/disk-images/my-case-name_*.dd "my-case-name"
```

### 4. Complete Recovery Workflow
```bash
# This creates image + runs PhotoRec automatically
~/data-recovery/tools/recovery-toolkit.sh quick-recovery /dev/sdb "my-case-name"
```

## Hard Drive Recovery Procedures

### Step 1: Assessment and Imaging

**IMPORTANT: Always create a disk image first to prevent further damage!**

1. **Identify the target device:**
   ```bash
   sudo fdisk -l
   lsblk
   ```

2. **Create a bit-by-bit disk image:**
   ```bash
   ~/data-recovery/tools/recovery-toolkit.sh create-image /dev/sdb "case-name"
   ```

### Step 2: File System Analysis

1. **Check partition table:**
   ```bash
   ~/data-recovery/tools/recovery-toolkit.sh testdisk /path/to/image.dd
   ```

2. **Recover deleted partitions:**
   - Use TestDisk's interactive interface
   - Write recovered partition table if found

### Step 3: File Recovery

1. **PhotoRec (Signature-based recovery):**
   ```bash
   ~/data-recovery/tools/recovery-toolkit.sh photorec /path/to/image.dd "case-name"
   ```

2. **Scalpel (Advanced file carving):**
   ```bash
   ~/data-recovery/tools/recovery-toolkit.sh scalpel /path/to/image.dd "case-name"
   ```

3. **Foremost (File type recovery):**
   ```bash
   ~/data-recovery/tools/recovery-toolkit.sh foremost /path/to/image.dd "case-name"
   ```

### Step 4: Manual Tools

1. **Direct tool usage:**
   ```bash
   # TestDisk
   sudo testdisk /dev/sdb
   
   # PhotoRec
   sudo photorec /dev/sdb
   
   # ddrescue (manual)
   sudo ddrescue -d -r3 -v /dev/sdb ~/recovery/image.dd ~/recovery/rescue.log
   ```

## Mobile Device Recovery

### Android Devices

1. **Enable Developer Options & USB Debugging:**
   - Settings → About Phone → Tap Build Number 7 times
   - Settings → Developer Options → Enable USB Debugging

2. **List connected devices:**
   ```bash
   ~/data-recovery/tools/recovery-toolkit.sh list-android
   ```

3. **Extract data:**
   ```bash
   ~/data-recovery/tools/recovery-toolkit.sh extract-android "phone-case-name"
   ```

4. **Manual ADB commands:**
   ```bash
   # Check device connection
   adb devices
   
   # Pull specific data
   adb pull /sdcard ~/recovery/android-data/
   
   # Get device info
   adb shell getprop
   ```

### iOS Devices

1. **Trust the computer on iOS device**
2. **List connected devices:**
   ```bash
   ~/data-recovery/tools/recovery-toolkit.sh list-ios
   ```

3. **Extract data:**
   ```bash
   ~/data-recovery/tools/recovery-toolkit.sh extract-ios "iphone-case-name"
   ```

4. **Manual iOS commands:**
   ```bash
   # List devices
   idevice_id -l
   
   # Get device info
   ideviceinfo
   
   # Create backup
   idevicebackup2 backup ~/recovery/ios-backup/
   ```

## Recovery Strategies by Damage Type

### Logical Damage (File System Corruption)
1. Use TestDisk to repair partition table
2. Run PhotoRec for deleted files
3. Check file system with fsck (Linux) or chkdsk (Windows)

### Physical Damage (Bad Sectors)
1. Use ddrescue with multiple passes (-r3)
2. Focus on recovering readable sectors first
3. Use Scalpel for file carving from partial data

### Formatted Drive
1. Don't write anything to the drive
2. Use PhotoRec - ignores file system structure
3. Foremost can recover specific file types

### Water Damage (Mobile)
1. Power off device immediately
2. Dry thoroughly before attempting connection
3. Use specialized mobile recovery tools if device boots

## File Types Recoverable

### PhotoRec Supports:
- Images: JPG, PNG, GIF, TIFF, BMP, RAW formats
- Documents: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX
- Videos: MP4, AVI, MOV, MKV, WMV, FLV
- Audio: MP3, WAV, FLAC, AAC, OGG
- Archives: ZIP, RAR, 7Z, TAR, GZ
- And 400+ other file formats

### Scalpel Configuration:
Edit `/etc/scalpel/scalpel.conf` to customize file types and sizes.

## Best Practices

### Before Recovery
1. **Stop using the device immediately**
2. **Power down to prevent overwrites**
3. **Create bit-by-bit image first**
4. **Work from copies, never originals**
5. **Document everything**

### During Recovery
1. **Use write-blocking hardware when possible**
2. **Save to different drive than source**
3. **Monitor progress and logs**
4. **Multiple recovery attempts with different tools**

### After Recovery
1. **Verify recovered files**
2. **Generate case reports**
3. **Calculate and verify checksums**
4. **Organize by file type and date**

## Security Considerations

### Legal Compliance
- Ensure proper authorization before accessing devices
- Maintain chain of custody documentation
- Follow local laws regarding data access

### Technical Security
- Use encrypted storage for recovered data
- Secure wipe temporary files
- Maintain audit logs of all operations

## Troubleshooting

### Common Issues

1. **"Permission denied" errors:**
   ```bash
   sudo chown -R $USER:$USER ~/data-recovery/
   ```

2. **Device not recognized:**
   ```bash
   # Check USB connections
   lsusb
   
   # Restart services
   sudo systemctl restart usbmuxd
   ```

3. **Out of disk space:**
   ```bash
   # Check available space
   df -h
   
   # Clean old recovery data
   rm -rf ~/data-recovery/recovered-data/old-case/
   ```

4. **Mobile device connection issues:**
   ```bash
   # Android
   adb kill-server
   adb start-server
   
   # iOS  
   sudo systemctl restart usbmuxd
   ```

### Recovery Tips

1. **Low success rate?** Try multiple tools - each uses different algorithms
2. **Partial files?** Use file repair tools after recovery
3. **Can't mount image?** Try different loop devices or mounting options
4. **Slow recovery?** Check for bad sectors with badblocks

## Advanced Techniques

### Custom File Signatures
Create custom Scalpel configurations for proprietary file types:
```
# Custom file type in scalpel.conf
customfile  y  5000000  \\x43\\x55\\x53\\x54  \\x45\\x4e\\x44
```

### Network Recovery
For remote devices, use network forensics tools:
```bash
# Network packet capture
tcpdump -i any -w capture.pcap

# Analyze with Wireshark
wireshark capture.pcap
```

### Memory Analysis
For running systems:
```bash
# Create memory dump
sudo dd if=/dev/mem of=memory.dump bs=1024

# Analyze with Volatility
volatility -f memory.dump imageinfo
```

## Reporting

### Generate Reports
```bash
~/data-recovery/tools/recovery-toolkit.sh generate-report "case-name"
```

### Manual Documentation
Keep detailed logs including:
- Device information and condition
- Tools used and settings
- Files recovered and their condition  
- Chain of custody information
- Timeline of operations

## Emergency Procedures

### Hard Drive Making Noise
1. Power off immediately
2. Do not attempt DIY recovery
3. Contact professional data recovery service
4. Physical damage requires clean room environment

### Mobile Device Water Damage
1. Power off device
2. Remove battery if possible
3. Dry with rice/silica gel for 48+ hours
4. Attempt recovery only when completely dry

### Encrypted Devices
- Focus on metadata and unencrypted areas
- Document encryption methods discovered
- Consider legal methods for password recovery

## Professional Recovery Services

When to seek professional help:
- Physical drive damage (clicking, grinding sounds)
- Clean room required (opened drive case)
- Mission-critical data worth professional cost
- Legal requirements for certified procedures

---

## Tool Reference

### Recovery Toolkit Script Commands
```bash
# List all available commands
~/data-recovery/tools/recovery-toolkit.sh help

# Common workflows
list-devices              # Scan for storage devices
create-image             # Create disk image  
quick-recovery           # Complete recovery workflow
generate-report          # Create case report
```

### Direct Tool Usage
```bash
# TestDisk
testdisk /dev/sdb        # Interactive partition recovery

# PhotoRec  
photorec /dev/sdb        # Interactive file recovery

# ddrescue
ddrescue -d -r3 /dev/sdb image.dd rescue.log

# Foremost
foremost -i /dev/sdb -o output/

# Scalpel
scalpel -o output/ /dev/sdb
```

Remember: Always prioritize creating a disk image first to preserve evidence and prevent further data loss!