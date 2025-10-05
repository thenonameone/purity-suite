#!/bin/bash

# Pure Data - Professional Data Recovery & Digital Forensics Suite
# Comprehensive toolkit for mobile devices, hard drives, and digital forensics
# 
# LEGAL NOTICE: This tool is intended for use only on devices you own or 
# have explicit legal authorization to access.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m'

# Tool paths (allow override via PURE_DATA_DIR)
RECOVERY_DIR="${PURE_DATA_DIR:-$HOME/data-recovery}"
TOOLS_DIR="$RECOVERY_DIR/tools"
RECOVERY_TOOLKIT="$TOOLS_DIR/recovery-toolkit.sh"
DEBUG_ENABLER="$TOOLS_DIR/android-debug-enabler.sh"
BOOTLOADER_TOOLS="$TOOLS_DIR/bootloader-recovery-tools.py"

# Clear screen and show header
show_header() {
    clear
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${WHITE}                        Pure Data                              ${CYAN}║${NC}"
    echo -e "${CYAN}║${WHITE}         Professional Data Recovery & Digital Forensics        ${CYAN}║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo -e "${YELLOW}⚖️  LEGAL NOTICE: Only use on devices you own or have authorization to access${NC}"
    echo ""
}

# Show main menu
show_main_menu() {
    show_header
    echo -e "${WHITE}═══ MAIN MENU ═══${NC}"
    echo ""
    echo -e "${GREEN}📱 MOBILE DEVICE FORENSICS:${NC}"
    echo -e "  ${CYAN}1)${NC} Check Connected Devices Status"
    echo -e "  ${CYAN}2)${NC} Auto-Enable USB Debugging (Try All Methods)"
    echo -e "  ${CYAN}3)${NC} Manual Debug Method Selection"
    echo -e "  ${CYAN}4)${NC} Device Information Gathering"
    echo ""
    echo -e "${GREEN}🔓 BOOTLOADER & RECOVERY:${NC}"
    echo -e "  ${CYAN}5)${NC} Bootloader Operations"
    echo -e "  ${CYAN}6)${NC} Custom Recovery Operations"
    echo -e "  ${CYAN}7)${NC} Create Magisk Debug Module"
    echo ""
    echo -e "${GREEN}💾 DATA RECOVERY:${NC}"
    echo -e "  ${CYAN}8)${NC} Android Data Extraction"
    echo -e "  ${CYAN}9)${NC} iOS Device Recovery"
    echo -e "  ${CYAN}10)${NC} Hard Drive Recovery Tools"
    echo -e "  ${CYAN}11)${NC} Quick Recovery Workflow"
    echo ""
    echo -e "${GREEN}📊 REPORTING & ANALYSIS:${NC}"
    echo -e "  ${CYAN}12)${NC} Generate Device Report"
    echo -e "  ${CYAN}13)${NC} Generate Case Report"
    echo -e "  ${CYAN}14)${NC} View Recovery Logs"
    echo ""
    echo -e "${GREEN}📚 DOCUMENTATION & HELP:${NC}"
    echo -e "  ${CYAN}15)${NC} Legal & Ethical Guidelines"
    echo -e "  ${CYAN}16)${NC} Hardware Forensic Methods"
    echo -e "  ${CYAN}17)${NC} Quick Reference Guide"
    echo -e "  ${CYAN}18)${NC} Tool Help & Usage"
    echo ""
    echo -e "${GREEN}⚙️  SYSTEM & UTILITIES:${NC}"
    echo -e "  ${CYAN}19)${NC} System Status Check"
    echo -e "  ${CYAN}20)${NC} Update Tool Permissions"
    echo -e "  ${CYAN}21)${NC} Workspace Management"
    echo ""
    echo -e "${RED}0) Exit${NC}"
    echo ""
    echo -e "${WHITE}═══════════════════════════════════════════════════════════════${NC}"
}

# Pause function
pause() {
    echo ""
    read -p "Press Enter to continue..."
}

# Legal disclaimer function
show_legal_disclaimer() {
    echo -e "${RED}⚖️  LEGAL DISCLAIMER:${NC}"
    echo "This tool is intended for use only on:"
    echo "• Devices you personally own"
    echo "• Devices you have explicit legal authorization to access"
    echo "• Authorized forensic investigations with proper legal authority"
    echo "• Corporate devices with management authorization"
    echo "• Academic research with appropriate approvals"
    echo ""
    echo -e "${YELLOW}Unauthorized access to devices is illegal in most jurisdictions.${NC}"
    echo ""
    read -p "Do you have legal authorization to proceed? (yes/no): " auth
    if [[ "$auth" != "yes" ]]; then
        echo -e "${RED}Legal authorization required. Returning to menu.${NC}"
        pause
        return 1
    fi
    return 0
}

# Check connected devices status
check_device_status() {
    show_header
    echo -e "${WHITE}═══ DEVICE STATUS CHECK ═══${NC}"
    echo ""
    
    echo -e "${CYAN}📱 Android Devices (ADB):${NC}"
    adb devices -l 2>/dev/null | grep -v "List of devices" || echo "No ADB devices found"
    echo ""
    
    echo -e "${CYAN}🔧 Fastboot Devices:${NC}"
    fastboot devices 2>/dev/null || echo "No fastboot devices found"
    echo ""
    
    echo -e "${CYAN}🍎 iOS Devices:${NC}"
    if command -v idevice_id &> /dev/null; then
        idevice_id -l 2>/dev/null || echo "No iOS devices found"
    else
        echo "iOS tools not available"
    fi
    echo ""
    
    echo -e "${CYAN}💾 Storage Devices:${NC}"
    lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,LABEL | head -10
    
    pause
}

# Auto-enable USB debugging
auto_enable_debugging() {
    show_header
    echo -e "${WHITE}═══ AUTO-ENABLE USB DEBUGGING ═══${NC}"
    echo ""
    
    if ! show_legal_disclaimer; then
        return
    fi
    
    echo -e "${GREEN}Starting automated USB debugging enabler...${NC}"
    echo ""
    "$DEBUG_ENABLER" auto
    pause
}

# Manual debug method selection
manual_debug_methods() {
    while true; do
        show_header
        echo -e "${WHITE}═══ MANUAL DEBUG METHODS ═══${NC}"
        echo ""
        echo -e "${CYAN}1)${NC} ADB Method (if partially enabled)"
        echo -e "${CYAN}2)${NC} Root Method (requires root access)"
        echo -e "${CYAN}3)${NC} Fastboot Method (requires unlocked bootloader)"
        echo -e "${CYAN}4)${NC} Recovery Method (requires custom recovery)"
        echo -e "${CYAN}5)${NC} Show Exploit Methods (older devices)"
        echo -e "${CYAN}6)${NC} Show Physical Access Methods"
        echo -e "${CYAN}7)${NC} Check Debugging Persistence"
        echo -e "${CYAN}8)${NC} Interactive Debug Menu"
        echo ""
        echo -e "${RED}0) Back to Main Menu${NC}"
        echo ""
        
        read -p "Select option (0-8): " choice
        
        case $choice in
            1)
                if show_legal_disclaimer; then
                    "$DEBUG_ENABLER" adb
                    pause
                fi
                ;;
            2)
                if show_legal_disclaimer; then
                    "$DEBUG_ENABLER" root
                    pause
                fi
                ;;
            3)
                if show_legal_disclaimer; then
                    "$DEBUG_ENABLER" fastboot
                    pause
                fi
                ;;
            4)
                if show_legal_disclaimer; then
                    "$DEBUG_ENABLER" recovery
                    pause
                fi
                ;;
            5)
                if show_legal_disclaimer; then
                    "$DEBUG_ENABLER" exploits
                    pause
                fi
                ;;
            6)
                "$DEBUG_ENABLER" physical
                pause
                ;;
            7)
                "$DEBUG_ENABLER" persistence
                pause
                ;;
            8)
                "$DEBUG_ENABLER" menu
                ;;
            0)
                return
                ;;
            *)
                echo -e "${RED}Invalid option. Please select 0-8.${NC}"
                sleep 1
                ;;
        esac
    done
}

# Device information gathering
device_info_gathering() {
    show_header
    echo -e "${WHITE}═══ DEVICE INFORMATION GATHERING ═══${NC}"
    echo ""
    
    echo -e "${CYAN}1)${NC} Android Device Information"
    echo -e "${CYAN}2)${NC} Bootloader Information" 
    echo -e "${CYAN}3)${NC} Complete Device Report"
    echo -e "${CYAN}4)${NC} iOS Device Information"
    echo ""
    read -p "Select option (1-4): " choice
    
    case $choice in
        1)
            "$DEBUG_ENABLER" info
            ;;
        2)
            python3 "$BOOTLOADER_TOOLS" bootloader-info
            ;;
        3)
            python3 "$BOOTLOADER_TOOLS" device-report
            ;;
        4)
            if command -v ideviceinfo &> /dev/null; then
                ideviceinfo
            else
                echo -e "${RED}iOS tools not installed${NC}"
            fi
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            ;;
    esac
    pause
}

# Bootloader operations
bootloader_operations() {
    while true; do
        show_header
        echo -e "${WHITE}═══ BOOTLOADER OPERATIONS ═══${NC}"
        echo ""
        echo -e "${YELLOW}⚠️  WARNING: These operations can wipe device data!${NC}"
        echo ""
        echo -e "${CYAN}1)${NC} Check Fastboot Connection"
        echo -e "${CYAN}2)${NC} Get Bootloader Information"
        echo -e "${CYAN}3)${NC} Unlock Bootloader (DANGEROUS)"
        echo -e "${CYAN}4)${NC} Boot Recovery Image"
        echo -e "${CYAN}5)${NC} Show FRP Bypass Methods"
        echo ""
        echo -e "${RED}0) Back to Main Menu${NC}"
        echo ""
        
        read -p "Select option (0-5): " choice
        
        case $choice in
            1)
                python3 "$BOOTLOADER_TOOLS" check-fastboot
                ;;
            2)
                python3 "$BOOTLOADER_TOOLS" bootloader-info
                ;;
            3)
                if show_legal_disclaimer; then
                    python3 "$BOOTLOADER_TOOLS" unlock-bootloader
                fi
                ;;
            4)
                if show_legal_disclaimer; then
                    echo "Enter path to recovery image (or press Enter for auto-detect):"
                    read recovery_path
                    if [[ -z "$recovery_path" ]]; then
                        python3 "$BOOTLOADER_TOOLS" boot-recovery
                    else
                        python3 "$BOOTLOADER_TOOLS" boot-recovery "$recovery_path"
                    fi
                fi
                ;;
            5)
                python3 "$BOOTLOADER_TOOLS" frp-bypass
                ;;
            0)
                return
                ;;
            *)
                echo -e "${RED}Invalid option. Please select 0-5.${NC}"
                sleep 1
                continue
                ;;
        esac
        pause
    done
}

# Recovery operations
recovery_operations() {
    while true; do
        show_header
        echo -e "${WHITE}═══ CUSTOM RECOVERY OPERATIONS ═══${NC}"
        echo ""
        echo -e "${CYAN}1)${NC} Check Recovery Connection"
        echo -e "${CYAN}2)${NC} Enable Debugging via Recovery"
        echo -e "${CYAN}3)${NC} Mount System Partition"
        echo -e "${CYAN}4)${NC} Recovery Command Shell"
        echo ""
        echo -e "${RED}0) Back to Main Menu${NC}"
        echo ""
        
        read -p "Select option (0-4): " choice
        
        case $choice in
            1)
                python3 "$BOOTLOADER_TOOLS" check-recovery
                ;;
            2)
                if show_legal_disclaimer; then
                    python3 "$BOOTLOADER_TOOLS" enable-debug-recovery
                fi
                ;;
            3)
                echo "Attempting to mount system partition..."
                adb shell "mount /system" 2>/dev/null || adb shell "mount -o rw /system" || echo "Mount failed"
                ;;
            4)
                echo "Opening ADB shell to recovery..."
                adb shell
                ;;
            0)
                return
                ;;
            *)
                echo -e "${RED}Invalid option. Please select 0-4.${NC}"
                sleep 1
                continue
                ;;
        esac
        pause
    done
}

# Create Magisk module
create_magisk_module() {
    show_header
    echo -e "${WHITE}═══ CREATE MAGISK DEBUG MODULE ═══${NC}"
    echo ""
    
    if show_legal_disclaimer; then
        python3 "$BOOTLOADER_TOOLS" create-magisk-module
    fi
    pause
}

# Android data extraction
android_data_extraction() {
    show_header
    echo -e "${WHITE}═══ ANDROID DATA EXTRACTION ═══${NC}"
    echo ""
    
    if ! show_legal_disclaimer; then
        return
    fi
    
    read -p "Enter case name: " case_name
    if [[ -z "$case_name" ]]; then
        echo -e "${RED}Case name required${NC}"
        pause
        return
    fi
    
    echo -e "${GREEN}Starting Android data extraction for case: $case_name${NC}"
    "$RECOVERY_TOOLKIT" extract-android "$case_name"
    pause
}

# iOS device recovery
ios_device_recovery() {
    show_header
    echo -e "${WHITE}═══ iOS DEVICE RECOVERY ═══${NC}"
    echo ""
    
    if ! show_legal_disclaimer; then
        return
    fi
    
    read -p "Enter case name: " case_name
    if [[ -z "$case_name" ]]; then
        echo -e "${RED}Case name required${NC}"
        pause
        return
    fi
    
    echo -e "${GREEN}Starting iOS data extraction for case: $case_name${NC}"
    "$RECOVERY_TOOLKIT" extract-ios "$case_name"
    pause
}

# Hard drive recovery tools
hard_drive_recovery() {
    while true; do
        show_header
        echo -e "${WHITE}═══ HARD DRIVE RECOVERY TOOLS ═══${NC}"
        echo ""
        echo -e "${CYAN}1)${NC} List Storage Devices"
        echo -e "${CYAN}2)${NC} Create Disk Image"
        echo -e "${CYAN}3)${NC} Run TestDisk (Partition Recovery)"
        echo -e "${CYAN}4)${NC} Run PhotoRec (File Recovery)"
        echo -e "${CYAN}5)${NC} Run Scalpel (File Carving)"
        echo -e "${CYAN}6)${NC} Run Foremost (File Recovery)"
        echo ""
        echo -e "${RED}0) Back to Main Menu${NC}"
        echo ""
        
        read -p "Select option (0-6): " choice
        
        case $choice in
            1)
                "$RECOVERY_TOOLKIT" list-devices
                ;;
            2)
                read -p "Enter source device (e.g., /dev/sdb): " device
                read -p "Enter case name: " case_name
                if [[ -n "$device" && -n "$case_name" ]]; then
                    "$RECOVERY_TOOLKIT" create-image "$device" "$case_name"
                else
                    echo -e "${RED}Device and case name required${NC}"
                fi
                ;;
            3)
                read -p "Enter target device/image: " target
                if [[ -n "$target" ]]; then
                    "$RECOVERY_TOOLKIT" testdisk "$target"
                else
                    echo -e "${RED}Target required${NC}"
                fi
                ;;
            4)
                read -p "Enter source device/image: " source
                read -p "Enter case name: " case_name
                if [[ -n "$source" && -n "$case_name" ]]; then
                    "$RECOVERY_TOOLKIT" photorec "$source" "$case_name"
                else
                    echo -e "${RED}Source and case name required${NC}"
                fi
                ;;
            5)
                read -p "Enter source device/image: " source
                read -p "Enter case name: " case_name
                if [[ -n "$source" && -n "$case_name" ]]; then
                    "$RECOVERY_TOOLKIT" scalpel "$source" "$case_name"
                else
                    echo -e "${RED}Source and case name required${NC}"
                fi
                ;;
            6)
                read -p "Enter source device/image: " source
                read -p "Enter case name: " case_name
                if [[ -n "$source" && -n "$case_name" ]]; then
                    "$RECOVERY_TOOLKIT" foremost "$source" "$case_name"
                else
                    echo -e "${RED}Source and case name required${NC}"
                fi
                ;;
            0)
                return
                ;;
            *)
                echo -e "${RED}Invalid option. Please select 0-6.${NC}"
                sleep 1
                continue
                ;;
        esac
        pause
    done
}

# Quick recovery workflow
quick_recovery_workflow() {
    show_header
    echo -e "${WHITE}═══ QUICK RECOVERY WORKFLOW ═══${NC}"
    echo ""
    
    echo -e "${CYAN}1)${NC} Android Device Quick Recovery"
    echo -e "${CYAN}2)${NC} Hard Drive Quick Recovery"
    echo ""
    read -p "Select option (1-2): " choice
    
    case $choice in
        1)
            if show_legal_disclaimer; then
                read -p "Enter case name: " case_name
                if [[ -n "$case_name" ]]; then
                    echo "Starting Android quick recovery..."
                    "$DEBUG_ENABLER" auto
                    if adb devices | grep -q "device"; then
                        "$RECOVERY_TOOLKIT" extract-android "$case_name"
                    fi
                fi
            fi
            ;;
        2)
            read -p "Enter source device (e.g., /dev/sdb): " device
            read -p "Enter case name: " case_name
            if [[ -n "$device" && -n "$case_name" ]]; then
                "$RECOVERY_TOOLKIT" quick-recovery "$device" "$case_name"
            else
                echo -e "${RED}Device and case name required${NC}"
            fi
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            ;;
    esac
    pause
}

# Generate device report
generate_device_report() {
    show_header
    echo -e "${WHITE}═══ GENERATE DEVICE REPORT ═══${NC}"
    echo ""
    
    echo -e "${CYAN}Generating comprehensive device report...${NC}"
    python3 "$BOOTLOADER_TOOLS" device-report
    pause
}

# Generate case report
generate_case_report() {
    show_header
    echo -e "${WHITE}═══ GENERATE CASE REPORT ═══${NC}"
    echo ""
    
    read -p "Enter case name: " case_name
    if [[ -n "$case_name" ]]; then
        "$RECOVERY_TOOLKIT" generate-report "$case_name"
    else
        echo -e "${RED}Case name required${NC}"
    fi
    pause
}

# View recovery logs
view_recovery_logs() {
    show_header
    echo -e "${WHITE}═══ RECOVERY LOGS ═══${NC}"
    echo ""
    
    echo -e "${CYAN}Available log files:${NC}"
    ls -la "$RECOVERY_DIR/logs/" 2>/dev/null | head -20
    echo ""
    
    read -p "Enter log filename to view (or press Enter to see latest): " logfile
    
    if [[ -z "$logfile" ]]; then
        # Show latest log
        latest_log=$(ls -t "$RECOVERY_DIR/logs/"*.log 2>/dev/null | head -1)
        if [[ -n "$latest_log" ]]; then
            echo -e "${GREEN}Latest log: $latest_log${NC}"
            tail -50 "$latest_log"
        else
            echo -e "${RED}No log files found${NC}"
        fi
    else
        if [[ -f "$RECOVERY_DIR/logs/$logfile" ]]; then
            less "$RECOVERY_DIR/logs/$logfile"
        else
            echo -e "${RED}Log file not found${NC}"
        fi
    fi
    pause
}

# Show documentation
show_documentation() {
    while true; do
        show_header
        echo -e "${WHITE}═══ DOCUMENTATION & HELP ═══${NC}"
        echo ""
        echo -e "${CYAN}1)${NC} Legal & Ethical Guidelines"
        echo -e "${CYAN}2)${NC} Hardware Forensic Methods"
        echo -e "${CYAN}3)${NC} Quick Reference Guide"
        echo -e "${CYAN}4)${NC} Data Recovery Guide"
        echo -e "${CYAN}5)${NC} Tool Help & Usage"
        echo ""
        echo -e "${RED}0) Back to Main Menu${NC}"
        echo ""
        
        read -p "Select option (0-5): " choice
        
        case $choice in
            1)
                if command -v less &> /dev/null; then
                    less "$RECOVERY_DIR/LEGAL_ETHICAL_GUIDELINES.md"
                else
                    cat "$RECOVERY_DIR/LEGAL_ETHICAL_GUIDELINES.md"
                fi
                ;;
            2)
                if command -v less &> /dev/null; then
                    less "$RECOVERY_DIR/HARDWARE_FORENSIC_METHODS.md"
                else
                    cat "$RECOVERY_DIR/HARDWARE_FORENSIC_METHODS.md"
                fi
                ;;
            3)
                if command -v less &> /dev/null; then
                    less "$RECOVERY_DIR/ANDROID_DEBUG_QUICKREF.md"
                else
                    cat "$RECOVERY_DIR/ANDROID_DEBUG_QUICKREF.md"
                fi
                ;;
            4)
                if command -v less &> /dev/null; then
                    less "$RECOVERY_DIR/DATA_RECOVERY_GUIDE.md"
                else
                    cat "$RECOVERY_DIR/DATA_RECOVERY_GUIDE.md"
                fi
                ;;
            5)
                echo -e "${GREEN}Tool Help:${NC}"
                echo ""
                echo "Recovery Toolkit Help:"
                "$RECOVERY_TOOLKIT" help
                echo ""
                echo "Android Debug Enabler Help:"
                "$DEBUG_ENABLER" help
                echo ""
                echo "Bootloader Tools Help:"
                python3 "$BOOTLOADER_TOOLS"
                ;;
            0)
                return
                ;;
            *)
                echo -e "${RED}Invalid option. Please select 0-5.${NC}"
                sleep 1
                continue
                ;;
        esac
        pause
    done
}

# System status check
system_status_check() {
    show_header
    echo -e "${WHITE}═══ SYSTEM STATUS CHECK ═══${NC}"
    echo ""
    
    echo -e "${CYAN}Tool Availability:${NC}"
    tools=("adb" "fastboot" "testdisk" "photorec" "ddrescue" "foremost" "scalpel")
    for tool in "${tools[@]}"; do
        if command -v "$tool" &> /dev/null; then
            echo -e "  ✅ $tool - Available"
        else
            echo -e "  ❌ $tool - Not found"
        fi
    done
    
    echo ""
    echo -e "${CYAN}Directory Structure:${NC}"
    if [[ -d "$RECOVERY_DIR" ]]; then
        echo -e "  ✅ Recovery directory exists"
        du -sh "$RECOVERY_DIR"/* 2>/dev/null | head -10
    else
        echo -e "  ❌ Recovery directory missing"
    fi
    
    echo ""
    echo -e "${CYAN}Permissions:${NC}"
    if [[ -x "$RECOVERY_TOOLKIT" ]]; then
        echo -e "  ✅ Recovery toolkit executable"
    else
        echo -e "  ❌ Recovery toolkit not executable"
    fi
    
    pause
}

# Update tool permissions
update_tool_permissions() {
    show_header
    echo -e "${WHITE}═══ UPDATE TOOL PERMISSIONS ═══${NC}"
    echo ""
    
    echo -e "${GREEN}Updating tool permissions...${NC}"
    chmod +x "$RECOVERY_TOOLKIT" 2>/dev/null && echo "✅ Recovery toolkit"
    chmod +x "$DEBUG_ENABLER" 2>/dev/null && echo "✅ Debug enabler"
    chmod +x "$BOOTLOADER_TOOLS" 2>/dev/null && echo "✅ Bootloader tools"
    chmod +x "$TOOLS_DIR/android-master-menu.sh" 2>/dev/null && echo "✅ Master menu"
    
    echo ""
    echo -e "${GREEN}Fixing directory ownership...${NC}"
    sudo chown -R "$USER:$USER" "$RECOVERY_DIR" 2>/dev/null && echo "✅ Directory ownership fixed"
    
    pause
}

# Workspace management
workspace_management() {
    while true; do
        show_header
        echo -e "${WHITE}═══ WORKSPACE MANAGEMENT ═══${NC}"
        echo ""
        echo -e "${CYAN}1)${NC} Show Disk Usage"
        echo -e "${CYAN}2)${NC} Clean Old Logs"
        echo -e "${CYAN}3)${NC} Archive Case Data"
        echo -e "${CYAN}4)${NC} Backup Workspace"
        echo -e "${CYAN}5)${NC} Reset Workspace"
        echo ""
        echo -e "${RED}0) Back to Main Menu${NC}"
        echo ""
        
        read -p "Select option (0-5): " choice
        
        case $choice in
            1)
                echo -e "${CYAN}Disk Usage:${NC}"
                df -h
                echo ""
                echo -e "${CYAN}Recovery Directory Usage:${NC}"
                du -sh "$RECOVERY_DIR"/* 2>/dev/null
                ;;
            2)
                echo -e "${YELLOW}Cleaning logs older than 30 days...${NC}"
                find "$RECOVERY_DIR/logs" -name "*.log" -mtime +30 -delete 2>/dev/null || true
                echo "✅ Old logs cleaned"
                ;;
            3)
                read -p "Enter case name to archive: " case_name
                if [[ -n "$case_name" ]]; then
                    archive_name="case_${case_name}_$(date +%Y%m%d).tar.gz"
                    tar -czf "$HOME/$archive_name" -C "$RECOVERY_DIR" . 2>/dev/null || true
                    echo "✅ Case archived to: $HOME/$archive_name"
                fi
                ;;
            4)
                backup_name="recovery_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
                tar -czf "$HOME/$backup_name" -C "$HOME" data-recovery 2>/dev/null || true
                echo "✅ Workspace backed up to: $HOME/$backup_name"
                ;;
            5)
                echo -e "${RED}WARNING: This will reset the entire workspace!${NC}"
                read -p "Are you sure? (yes/no): " confirm
                if [[ "$confirm" == "yes" ]]; then
                    rm -rf "$RECOVERY_DIR/recovered-data"/* 2>/dev/null || true
                    rm -rf "$RECOVERY_DIR/mobile-data"/* 2>/dev/null || true
                    rm -rf "$RECOVERY_DIR/disk-images"/* 2>/dev/null || true
                    echo "✅ Workspace reset complete"
                fi
                ;;
            0)
                return
                ;;
            *)
                echo -e "${RED}Invalid option. Please select 0-5.${NC}"
                sleep 1
                continue
                ;;
        esac
        pause
    done
}

# Main program loop
main() {
    # Check if required tools exist
    if [[ ! -f "$RECOVERY_TOOLKIT" || ! -f "$DEBUG_ENABLER" || ! -f "$BOOTLOADER_TOOLS" ]]; then
        echo -e "${RED}Error: Required tools not found. Please ensure all tools are installed.${NC}"
        exit 1
    fi
    
    while true; do
        show_main_menu
        read -p "Select option (0-21): " choice
        
        case $choice in
            1) check_device_status ;;
            2) auto_enable_debugging ;;
            3) manual_debug_methods ;;
            4) device_info_gathering ;;
            5) bootloader_operations ;;
            6) recovery_operations ;;
            7) create_magisk_module ;;
            8) android_data_extraction ;;
            9) ios_device_recovery ;;
            10) hard_drive_recovery ;;
            11) quick_recovery_workflow ;;
            12) generate_device_report ;;
            13) generate_case_report ;;
            14) view_recovery_logs ;;
            15|16|17|18) show_documentation ;;
            19) system_status_check ;;
            20) update_tool_permissions ;;
            21) workspace_management ;;
            0) 
                echo -e "${GREEN}Thank you for using Pure Data - Professional Data Recovery Suite${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option. Please select 0-21.${NC}"
                sleep 1
                ;;
        esac
    done
}

# Run main program
main "$@"