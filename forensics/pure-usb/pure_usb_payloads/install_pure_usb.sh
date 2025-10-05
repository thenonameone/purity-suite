#!/bin/bash

# Pure USB Installer Script
# =========================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
INSTALL_DIR="/opt/pure_usb"
DESKTOP_FILE="/usr/share/applications/pure_usb.desktop"
EXECUTABLE_LINK="/usr/local/bin/pure_usb"

echo -e "${BLUE}Pure USB Installer${NC}"
echo "=================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}This installer must be run as root.${NC}"
    echo "Please run: sudo $0"
    exit 1
fi

echo -e "${YELLOW}Installing Pure USB - Keylogger Payload Deployment Tool${NC}"
echo ""

# Check dependencies
echo "Checking dependencies..."

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check tkinter
python3 -c "import tkinter" 2>/dev/null || {
    echo -e "${RED}Python 3 tkinter is required but not installed.${NC}"
    echo "Install with: apt install python3-tk"
    exit 1
}

echo -e "${GREEN}✓ Dependencies satisfied${NC}"

# Create installation directory
echo "Creating installation directory..."
mkdir -p "$INSTALL_DIR"

# Copy files
echo "Copying application files..."
cp pure_usb.py "$INSTALL_DIR/"
cp *.exe "$INSTALL_DIR/" 2>/dev/null || true
cp *.py "$INSTALL_DIR/" 2>/dev/null || true
cp *.ps1 "$INSTALL_DIR/" 2>/dev/null || true
cp *.rc "$INSTALL_DIR/" 2>/dev/null || true
cp *.sh "$INSTALL_DIR/" 2>/dev/null || true
cp *.bat "$INSTALL_DIR/" 2>/dev/null || true
cp *.txt "$INSTALL_DIR/" 2>/dev/null || true
cp *.md "$INSTALL_DIR/" 2>/dev/null || true

# Set permissions
chmod +x "$INSTALL_DIR/pure_usb.py"
chmod +x "$INSTALL_DIR"/*.sh 2>/dev/null || true

# Create desktop entry
echo "Creating desktop entry..."
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Pure USB
Comment=Keylogger Payload Deployment Tool
Exec=python3 $INSTALL_DIR/pure_usb.py
Icon=drive-removable-media
Terminal=false
StartupNotify=true
Categories=System;Security;Network;
Keywords=pentest;payload;usb;keylogger;metasploit;
StartupWMClass=Pure USB
EOF

chmod 644 "$DESKTOP_FILE"

# Create executable symlink
echo "Creating executable symlink..."
cat > "$EXECUTABLE_LINK" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
python3 "$INSTALL_DIR/pure_usb.py" "\$@"
EOF

chmod +x "$EXECUTABLE_LINK"

# Create uninstaller
echo "Creating uninstaller..."
cat > "$INSTALL_DIR/uninstall.sh" << EOF
#!/bin/bash

echo "Uninstalling Pure USB..."

# Remove files
rm -rf "$INSTALL_DIR"
rm -f "$DESKTOP_FILE"
rm -f "$EXECUTABLE_LINK"

echo "Pure USB uninstalled successfully."
EOF

chmod +x "$INSTALL_DIR/uninstall.sh"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/
fi

echo ""
echo -e "${GREEN}Installation completed successfully!${NC}"
echo ""
echo "Pure USB has been installed to: $INSTALL_DIR"
echo ""
echo "You can now:"
echo "• Launch from Applications menu (System → Pure USB)"
echo "• Run from terminal: pure_usb"
echo "• Run directly: python3 $INSTALL_DIR/pure_usb.py"
echo ""
echo -e "${YELLOW}Usage Notes:${NC}"
echo "• Some USB operations may require sudo privileges"
echo "• Make sure Metasploit Framework is installed for handler functionality"
echo "• Only use on systems you own or have explicit permission to test"
echo ""
echo -e "${YELLOW}To uninstall:${NC}"
echo "sudo $INSTALL_DIR/uninstall.sh"
echo ""
echo -e "${RED}⚠️  LEGAL REMINDER: FOR AUTHORIZED TESTING ONLY${NC}"