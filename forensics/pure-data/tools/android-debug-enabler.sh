#!/bin/bash

# Pure Data - Android USB Debugging Enabler
# Multiple methods for enabling USB debugging for authorized device recovery
# Part of the Pure Data Professional Forensic Suite
# 
# LEGAL NOTICE: This script is intended for use only on devices you own or 
# have explicit legal authorization to access. Unauthorized access to devices
# is illegal in most jurisdictions.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Logging (allow override via PURE_DATA_DIR)
RECOVERY_DIR="${PURE_DATA_DIR:-$HOME/data-recovery}"
LOGS_DIR="$RECOVERY_DIR/logs"

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOGS_DIR/android-debug-$(date +%Y%m%d).log"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOGS_DIR/android-debug-$(date +%Y%m%d).log"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOGS_DIR/android-debug-$(date +%Y%m%d).log"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOGS_DIR/android-debug-$(date +%Y%m%d).log"
}

success() {
    echo -e "${CYAN}[SUCCESS]${NC} $1" | tee -a "$LOGS_DIR/android-debug-$(date +%Y%m%d).log"
}

# Legal disclaimer
show_disclaimer() {
    echo -e "${RED}LEGAL DISCLAIMER:${NC}"
    echo "This tool is intended for use only on:"
    echo "1. Devices you own"
    echo "2. Devices you have explicit legal authorization to access"
    echo "3. Forensic investigations with proper legal authority"
    echo ""
    echo "Unauthorized access to devices may be illegal in your jurisdiction."
    echo "Use this tool responsibly and in compliance with applicable laws."
    echo ""
    read -p "Do you have legal authorization to access this device? (yes/no): " auth
    if [[ "$auth" != "yes" ]]; then
        error "Legal authorization required. Exiting."
        exit 1
    fi
}

# Check device connection
check_device_connection() {
    info "Checking device connection..."
    
    # Check ADB connection
    local adb_devices=$(adb devices 2>/dev/null | grep -v "List of devices" | grep -v "^$" | wc -l)
    
    # Check fastboot connection
    local fastboot_devices=$(fastboot devices 2>/dev/null | wc -l)
    
    if [[ $adb_devices -gt 0 ]]; then
        success "Device connected via ADB"
        return 0
    elif [[ $fastboot_devices -gt 0 ]]; then
        success "Device connected via Fastboot"
        return 1
    else
        warn "No device detected. Make sure device is connected."
        return 2
    fi
}

# Method 1: Try to enable via ADB if already partially accessible
enable_via_adb() {
    log "Attempting to enable USB debugging via ADB..."
    
    # Check if we already have ADB access
    if adb devices | grep -q "device"; then
        info "ADB already enabled and authorized"
        return 0
    fi
    
    # Check if device is connected but unauthorized
    if adb devices | grep -q "unauthorized"; then
        warn "Device connected but unauthorized. User must accept debugging prompt on device."
        echo "Please accept the USB debugging authorization prompt on your device."
        echo "If you don't see a prompt, check the notification panel."
        
        # Wait for authorization
        local timeout=60
        while [[ $timeout -gt 0 ]]; do
            if adb devices | grep -q "device"; then
                success "USB debugging authorized!"
                return 0
            fi
            echo -n "."
            sleep 1
            ((timeout--))
        done
        
        error "Timeout waiting for USB debugging authorization"
        return 1
    fi
    
    # Try to enable debugging programmatically (requires root or system access)
    if adb shell "su -c 'setprop persist.sys.usb.config adb'" 2>/dev/null; then
        success "USB debugging enabled via root"
        adb kill-server
        adb start-server
        sleep 2
        return 0
    fi
    
    error "Could not enable USB debugging via ADB"
    return 1
}

# Method 2: Enable via fastboot/bootloader
enable_via_fastboot() {
    log "Attempting to enable USB debugging via fastboot..."
    
    if ! fastboot devices | grep -q "fastboot"; then
        error "Device not in fastboot mode. Please:"
        echo "1. Power off device"
        echo "2. Hold Volume Down + Power to enter fastboot mode"
        echo "3. Connect USB cable"
        return 1
    fi
    
    info "Device detected in fastboot mode"
    
    # Check if bootloader is unlocked
    local bootloader_status=$(fastboot getvar unlocked 2>&1 | grep "unlocked" | cut -d' ' -f2)
    
    if [[ "$bootloader_status" == "yes" ]]; then
        success "Bootloader is unlocked"
        
        # Try to boot into a custom recovery or enable debugging
        warn "This method requires a custom recovery image."
        echo "Would you like to:"
        echo "1. Boot temporary recovery (if available)"
        echo "2. Flash custom recovery"
        echo "3. Skip fastboot method"
        read -p "Choice (1-3): " choice
        
        case $choice in
            1)
                if [[ -f "/tmp/recovery.img" ]]; then
                    fastboot boot /tmp/recovery.img
                    info "Booted temporary recovery. Check device screen."
                else
                    error "No recovery image found at /tmp/recovery.img"
                fi
                ;;
            2)
                warn "Flashing custom recovery requires specific recovery image for your device"
                echo "This is beyond the scope of this script."
                ;;
            3)
                info "Skipping fastboot method"
                ;;
        esac
    else
        error "Bootloader is locked. Cannot use fastboot method without unlocking."
        return 1
    fi
}

# Method 3: Hardware-based methods
enable_via_hardware() {
    log "Hardware-based debugging methods..."
    
    echo -e "${CYAN}Hardware Methods Available:${NC}"
    echo "1. Test Points (Advanced - requires hardware knowledge)"
    echo "2. UART/Serial Connection"
    echo "3. JTAG Interface"
    echo "4. eMMC Direct Access"
    echo ""
    
    warn "Hardware methods require:"
    echo "- Advanced electronics knowledge"
    echo "- Specialized equipment"
    echo "- Risk of device damage"
    echo "- Professional forensic training"
    echo ""
    
    info "For professional hardware-based recovery, consider:"
    echo "- Cellebrite UFED"
    echo "- Oxygen Detective Suite"
    echo "- MSAB XRY"
    echo "- Chip-off forensic services"
}

# Method 4: Root-based methods
enable_via_root() {
    log "Attempting root-based USB debugging enabler..."
    
    # Check if device is rooted
    if adb shell "su -c 'id'" 2>/dev/null | grep -q "uid=0"; then
        success "Device appears to be rooted"
        
        # Enable USB debugging via root
        adb shell "su -c 'setprop persist.sys.usb.config adb'"
        adb shell "su -c 'setprop ro.adb.secure 0'"
        adb shell "su -c 'setprop ro.debuggable 1'"
        
        # Modify build.prop for persistent debugging
        adb shell "su -c 'mount -o remount,rw /system'"
        adb shell "su -c 'echo \"persist.sys.usb.config=adb\" >> /system/build.prop'"
        adb shell "su -c 'echo \"ro.adb.secure=0\" >> /system/build.prop'"
        adb shell "su -c 'echo \"ro.debuggable=1\" >> /system/build.prop'"
        
        # Restart ADB daemon
        adb shell "su -c 'stop adbd && start adbd'"
        
        success "USB debugging enabled via root access"
        return 0
    else
        error "Device is not rooted or root access denied"
        return 1
    fi
}

# Method 5: Custom recovery methods
enable_via_recovery() {
    log "Recovery mode methods..."
    
    echo "To enable USB debugging via custom recovery:"
    echo "1. Boot device into recovery mode (usually Volume Up + Power)"
    echo "2. Use custom recovery (TWRP, CWM, etc.) if installed"
    echo "3. Access file system and modify build.prop"
    echo ""
    
    if adb devices | grep -q "recovery"; then
        success "Device detected in recovery mode"
        
        # Try to modify build.prop via recovery
        info "Attempting to enable debugging via recovery..."
        
        adb shell "mount /system"
        if adb shell "echo 'persist.sys.usb.config=adb' >> /system/build.prop" 2>/dev/null; then
            success "Added debugging config to build.prop"
            adb shell "reboot"
            info "Device rebooting. USB debugging should be enabled."
            return 0
        else
            error "Could not modify build.prop via recovery"
            return 1
        fi
    else
        warn "Device not in recovery mode"
        return 1
    fi
}

# Method 6: Exploit-based methods (for older devices)
enable_via_exploits() {
    log "Checking for known exploits..."
    
    # Get device info
    local device_info
    if device_info=$(adb shell getprop ro.build.version.release 2>/dev/null); then
        local android_version=$(echo "$device_info" | tr -d '\r\n')
        info "Android version: $android_version"
        
        # Check for known vulnerabilities based on Android version
        case "$android_version" in
            "4.0"*|"4.1"*|"4.2"*|"4.3"*|"4.4"*)
                info "Old Android version detected. Potential exploits available:"
                echo "- Towelroot (Android 4.4.2 and below)"
                echo "- KingRoot (Various versions)"
                echo "- Framaroot (Android 4.3 and below)"
                ;;
            "5.0"*|"5.1"*)
                info "Android 5.x detected. Limited exploits:"
                echo "- KingRoot (some versions)"
                echo "- PingPong (5.0-5.1)"
                ;;
            "6.0"*|"7.0"*|"7.1"*)
                warn "Android 6.x-7.x detected. Very limited exploits available."
                ;;
            *)
                warn "Modern Android version. Exploits very unlikely to work."
                ;;
        esac
    else
        warn "Could not determine Android version"
    fi
    
    warn "Exploit methods are unreliable and may damage the device."
    warn "Only use on devices you own and can afford to lose."
}

# Method 7: Social engineering / Physical access
physical_access_methods() {
    log "Physical access methods..."
    
    echo -e "${CYAN}Physical Access Methods:${NC}"
    echo "1. Screen unlock patterns/PINs:"
    echo "   - Check for smudge patterns on screen"
    echo "   - Try common PINs (1234, 0000, 1111, etc.)"
    echo "   - Birth dates, phone numbers"
    echo ""
    echo "2. Smart Lock bypass:"
    echo "   - Trusted devices (smartwatches, etc.)"
    echo "   - Trusted locations (if GPS enabled)"
    echo "   - Voice unlock (if enabled)"
    echo ""
    echo "3. Emergency bypass:"
    echo "   - Emergency call vulnerabilities (older versions)"
    echo "   - Camera/notification panel access"
    echo ""
    echo "4. Developer options via accessibility:"
    echo "   - If accessibility services are enabled"
    echo "   - Voice assistant commands"
    echo ""
    
    warn "These methods should only be used on devices you own or have authorization to access."
}

# Method 8: USB debugging persistence checker
check_debug_persistence() {
    log "Checking USB debugging persistence..."
    
    if adb devices | grep -q "device"; then
        # Check current debugging status
        local debug_status=$(adb shell getprop persist.sys.usb.config 2>/dev/null)
        local secure_status=$(adb shell getprop ro.adb.secure 2>/dev/null)
        
        info "Current USB config: $debug_status"
        info "ADB secure mode: $secure_status"
        
        # Check if debugging will persist after reboot
        if echo "$debug_status" | grep -q "adb"; then
            success "USB debugging is configured to persist"
        else
            warn "USB debugging may not persist after reboot"
        fi
        
        # Try to make debugging persistent
        if adb shell "su -c 'setprop persist.sys.usb.config adb'" 2>/dev/null; then
            success "Made USB debugging persistent"
        else
            warn "Could not make debugging persistent (requires root)"
        fi
    else
        error "No device connected for persistence check"
        return 1
    fi
}

# Automated debugging enabler
auto_enable_debugging() {
    log "Starting automated USB debugging enabler..."
    
    show_disclaimer
    
    local connection_status
    check_device_connection
    connection_status=$?
    
    case $connection_status in
        0)
            info "Device connected via ADB - trying ADB methods"
            if enable_via_adb; then
                return 0
            fi
            if enable_via_root; then
                return 0
            fi
            ;;
        1)
            info "Device connected via Fastboot - trying fastboot methods"
            if enable_via_fastboot; then
                return 0
            fi
            ;;
        2)
            warn "No device detected - showing manual methods"
            ;;
    esac
    
    # Try recovery methods
    enable_via_recovery
    
    # Show other options
    echo -e "\n${CYAN}Other Methods:${NC}"
    echo "1. Hardware-based methods"
    echo "2. Exploit-based methods (older devices)"
    echo "3. Physical access methods"
    echo "4. Check debugging persistence"
    echo ""
    read -p "Try additional method? (1-4 or 'n' to exit): " method
    
    case $method in
        1) enable_via_hardware ;;
        2) enable_via_exploits ;;
        3) physical_access_methods ;;
        4) check_debug_persistence ;;
        *) info "Exiting..." ;;
    esac
}

# Device information gathering
gather_device_info() {
    log "Gathering device information..."
    
    local output_file="$RECOVERY_DIR/logs/device-info-$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "=== Android Device Information ==="
        echo "Timestamp: $(date)"
        echo "Operator: $(whoami)"
        echo ""
        
        if adb devices | grep -q "device"; then
            echo "=== Device Properties ==="
            adb shell getprop
            echo ""
            
            echo "=== Build Information ==="
            adb shell getprop ro.build.version.release
            adb shell getprop ro.build.version.sdk
            adb shell getprop ro.product.model
            adb shell getprop ro.product.manufacturer
            echo ""
            
            echo "=== USB Debugging Status ==="
            adb shell getprop persist.sys.usb.config
            adb shell getprop ro.adb.secure
            adb shell getprop ro.debuggable
            echo ""
            
            echo "=== Root Status ==="
            if adb shell "su -c 'id'" 2>/dev/null; then
                echo "Device appears to be rooted"
                adb shell "su -c 'id'"
            else
                echo "Device does not appear to be rooted"
            fi
        else
            echo "No ADB device connected"
        fi
        
        if fastboot devices | grep -q "fastboot"; then
            echo "=== Fastboot Information ==="
            fastboot getvar all 2>&1
        fi
        
    } | tee "$output_file"
    
    success "Device information saved to: $output_file"
}

# Main menu
show_menu() {
    echo -e "${CYAN}Android USB Debugging Enabler${NC}"
    echo "================================"
    echo "1. Auto-enable debugging (try all methods)"
    echo "2. Enable via ADB"
    echo "3. Enable via Fastboot/Bootloader"
    echo "4. Enable via Root"
    echo "5. Enable via Recovery"
    echo "6. Show hardware methods"
    echo "7. Show exploit methods"
    echo "8. Show physical access methods"
    echo "9. Check debugging persistence"
    echo "10. Gather device information"
    echo "11. Show help"
    echo "0. Exit"
    echo ""
}

show_help() {
    cat << EOF
Android USB Debugging Enabler Help

This tool provides multiple methods for enabling USB debugging on Android devices
for legitimate data recovery and forensic purposes.

PREREQUISITES:
- Device must be physically accessible
- Legal authorization to access the device
- ADB and Fastboot tools installed
- USB cable connection

METHODS AVAILABLE:
1. ADB Method - Works if debugging partially enabled
2. Fastboot Method - Requires unlocked bootloader
3. Root Method - Requires root access
4. Recovery Method - Requires custom recovery
5. Hardware Method - Advanced techniques requiring specialized equipment
6. Exploit Method - For older Android versions
7. Physical Access - Requires screen unlock

IMPORTANT NOTES:
- Always create a backup before attempting modifications
- Some methods may void warranty or damage device
- Success rates vary by device model and Android version
- Modern devices (Android 8+) are much harder to bypass

For professional forensic work, consider commercial tools like:
- Cellebrite UFED
- Oxygen Detective Suite
- MSAB XRY Mobile Forensics
EOF
}

# Main execution
main() {
    case "${1:-menu}" in
        auto)
            auto_enable_debugging
            ;;
        adb)
            show_disclaimer
            enable_via_adb
            ;;
        fastboot)
            show_disclaimer
            enable_via_fastboot
            ;;
        root)
            show_disclaimer
            enable_via_root
            ;;
        recovery)
            show_disclaimer
            enable_via_recovery
            ;;
        hardware)
            enable_via_hardware
            ;;
        exploits)
            show_disclaimer
            enable_via_exploits
            ;;
        physical)
            physical_access_methods
            ;;
        persistence)
            check_debug_persistence
            ;;
        info)
            gather_device_info
            ;;
        help|--help|-h)
            show_help
            ;;
        menu)
            while true; do
                show_menu
                read -p "Select option (0-11): " choice
                case $choice in
                    1) auto_enable_debugging ;;
                    2) show_disclaimer && enable_via_adb ;;
                    3) show_disclaimer && enable_via_fastboot ;;
                    4) show_disclaimer && enable_via_root ;;
                    5) show_disclaimer && enable_via_recovery ;;
                    6) enable_via_hardware ;;
                    7) show_disclaimer && enable_via_exploits ;;
                    8) physical_access_methods ;;
                    9) check_debug_persistence ;;
                    10) gather_device_info ;;
                    11) show_help ;;
                    0) exit 0 ;;
                    *) error "Invalid option" ;;
                esac
                echo ""
                read -p "Press Enter to continue..."
            done
            ;;
        *)
            error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"