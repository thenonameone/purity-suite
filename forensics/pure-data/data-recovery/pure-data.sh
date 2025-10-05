#!/bin/bash

# Pure Data - Professional Data Recovery & Digital Forensics Suite
# Main launcher script for the comprehensive forensic toolkit

# Colors for branding
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ASCII Art Logo
show_logo() {
    clear
    echo -e "${CYAN}"
    cat << "EOF"
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║    ██████╗ ██╗   ██╗██████╗ ███████╗    ██████╗  █████╗ ████████╗ █████╗ ║
    ║    ██╔══██╗██║   ██║██╔══██╗██╔════╝    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗║
    ║    ██████╔╝██║   ██║██████╔╝█████╗      ██║  ██║███████║   ██║   ███████║║
    ║    ██╔═══╝ ██║   ██║██╔══██╗██╔══╝      ██║  ██║██╔══██║   ██║   ██╔══██║║
    ║    ██║     ╚██████╔╝██║  ██║███████╗    ██████╔╝██║  ██║   ██║   ██║  ██║║
    ║    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝║
    ║                                                                          ║
    ║              Professional Data Recovery & Digital Forensics              ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    echo ""
    echo -e "${WHITE}🔍 Comprehensive toolkit for digital forensics and data recovery${NC}"
    echo -e "${BLUE}📱 Mobile devices • 💾 Hard drives • 🔐 Encrypted systems • 🛡️ Professional forensics${NC}"
    echo ""
    echo -e "${YELLOW}⚖️  LEGAL NOTICE: Only use on devices you own or have legal authorization to access${NC}"
    echo ""
    echo -e "${GREEN}Press Enter to continue to Pure Data main menu...${NC}"
    read
}

# Version information
show_version() {
    echo -e "${CYAN}Pure Data v1.0 - Professional Data Recovery & Digital Forensics Suite${NC}"
    echo -e "${WHITE}Comprehensive toolkit for mobile devices, hard drives, and digital forensics${NC}"
    echo ""
    echo -e "${BLUE}Components:${NC}"
    echo "• Mobile Device Forensics (Android/iOS)"
    echo "• Hard Drive & Storage Recovery"
    echo "• USB Debugging Bypass Tools"
    echo "• Bootloader & Recovery Operations"  
    echo "• Professional Reporting & Documentation"
    echo "• Hardware-Level Forensic Methods"
    echo ""
    echo -e "${GREEN}Created for professional forensic investigators and data recovery specialists${NC}"
    echo ""
}

# System requirements check
check_requirements() {
    echo -e "${CYAN}Checking system requirements...${NC}"
    echo ""
    
    requirements_met=true
    
    # Check for required tools
    tools=("adb" "fastboot" "python3" "testdisk" "photorec")
    for tool in "${tools[@]}"; do
        if command -v "$tool" &> /dev/null; then
            echo -e "✅ $tool - Available"
        else
            echo -e "❌ $tool - Missing"
            requirements_met=false
        fi
    done
    
    echo ""
    
    # Check directory structure
    if [[ -d "$HOME/data-recovery" ]]; then
        echo -e "✅ Pure Data workspace - Available"
        
        # Check for main tools
        if [[ -x "$HOME/data-recovery/tools/android-master-menu.sh" ]]; then
            echo -e "✅ Pure Data main interface - Available"
        else
            echo -e "❌ Pure Data main interface - Missing or not executable"
            requirements_met=false
        fi
    else
        echo -e "❌ Pure Data workspace - Missing"
        requirements_met=false
    fi
    
    echo ""
    
    if [[ "$requirements_met" == true ]]; then
        echo -e "${GREEN}✅ All requirements met. Pure Data is ready to use!${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Some requirements are missing. Pure Data may not function properly.${NC}"
        echo -e "${BLUE}Consider running system status check from the main menu for more details.${NC}"
        return 1
    fi
}

# Show help
show_help() {
    echo -e "${CYAN}Pure Data - Usage Help${NC}"
    echo ""
    echo -e "${WHITE}USAGE:${NC}"
    echo "  $0 [OPTION]"
    echo ""
    echo -e "${WHITE}OPTIONS:${NC}"
    echo "  -h, --help      Show this help message"
    echo "  -v, --version   Show version information"
    echo "  -c, --check     Check system requirements"
    echo "  -q, --quick     Launch directly without splash screen"
    echo "  --logo          Show Pure Data logo"
    echo ""
    echo -e "${WHITE}EXAMPLES:${NC}"
    echo "  $0              Launch Pure Data with splash screen"
    echo "  $0 --quick      Launch directly to main menu"
    echo "  $0 --check      Check if system is ready for Pure Data"
    echo ""
    echo -e "${WHITE}ALIASES:${NC}"
    echo "  puredata        Main launcher (after adding to PATH or alias)"
    echo "  pure-data       Alternative launcher"
    echo ""
}

# Launch main interface
launch_pure_data() {
    # Check if main menu exists
    if [[ ! -f "$HOME/data-recovery/tools/android-master-menu.sh" ]]; then
        echo -e "${RED}❌ Pure Data main interface not found.${NC}"
        echo "Please ensure Pure Data is properly installed."
        exit 1
    fi
    
    # Make sure it's executable
    chmod +x "$HOME/data-recovery/tools/android-master-menu.sh" 2>/dev/null
    
    # Launch the main menu
    exec "$HOME/data-recovery/tools/android-master-menu.sh"
}

# Main function
main() {
    case "${1:-default}" in
        -h|--help)
            show_help
            ;;
        -v|--version)
            show_version
            ;;
        -c|--check)
            check_requirements
            ;;
        -q|--quick)
            launch_pure_data
            ;;
        --logo)
            show_logo
            ;;
        default)
            show_logo
            launch_pure_data
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information."
            exit 1
            ;;
    esac
}

# Run main function
main "$@"