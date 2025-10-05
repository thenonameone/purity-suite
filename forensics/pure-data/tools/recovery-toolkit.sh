#!/bin/bash

# Pure Data - Data Recovery Toolkit
# Comprehensive script for hard drive and mobile device data recovery
# Part of the Pure Data Professional Forensic Suite

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directories (allow override via PURE_DATA_DIR)
RECOVERY_DIR="${PURE_DATA_DIR:-$HOME/data-recovery}"
DISK_IMAGES_DIR="$RECOVERY_DIR/disk-images"
RECOVERED_DATA_DIR="$RECOVERY_DIR/recovered-data"
MOBILE_DATA_DIR="$RECOVERY_DIR/mobile-data"
LOGS_DIR="$RECOVERY_DIR/logs"
CASES_DIR="$RECOVERY_DIR/cases"

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOGS_DIR/recovery-$(date +%Y%m%d).log"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOGS_DIR/recovery-$(date +%Y%m%d).log"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOGS_DIR/recovery-$(date +%Y%m%d).log"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOGS_DIR/recovery-$(date +%Y%m%d).log"
}

# Check if running as root for certain operations
check_root() {
    if [[ $EUID -eq 0 ]]; then
        warn "Running as root. Be careful with disk operations."
    fi
}

# List connected storage devices
list_devices() {
    log "Scanning for storage devices..."
    echo -e "\n${BLUE}=== Block Devices ===${NC}"
    lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,LABEL,UUID
    
    echo -e "\n${BLUE}=== Disk Information ===${NC}"
    sudo fdisk -l | grep "Disk /"
    
    echo -e "\n${BLUE}=== USB Devices ===${NC}"
    lsusb | grep -E "(storage|disk|drive)"
}

# Create disk image using ddrescue
create_disk_image() {
    local source_device="$1"
    local case_name="$2"
    
    if [[ -z "$source_device" ]] || [[ -z "$case_name" ]]; then
        error "Usage: create_disk_image <source_device> <case_name>"
        return 1
    fi
    
    local output_image="$DISK_IMAGES_DIR/${case_name}_$(date +%Y%m%d_%H%M%S).dd"
    local log_file="$LOGS_DIR/${case_name}_ddrescue.log"
    
    log "Creating disk image of $source_device..."
    log "Output: $output_image"
    
    # Create case directory
    mkdir -p "$CASES_DIR/$case_name"
    
    # Run ddrescue with detailed logging
    sudo ddrescue -d -r3 -v "$source_device" "$output_image" "$log_file"
    
    # Calculate checksums
    log "Calculating checksums..."
    md5sum "$output_image" > "$output_image.md5"
    sha256sum "$output_image" > "$output_image.sha256"
    
    log "Disk image created successfully: $output_image"
    log "MD5: $(cat "$output_image.md5")"
    log "SHA256: $(cat "$output_image.sha256")"
}

# Run TestDisk for partition recovery
run_testdisk() {
    local target="$1"
    
    if [[ -z "$target" ]]; then
        error "Usage: run_testdisk <device_or_image>"
        return 1
    fi
    
    log "Starting TestDisk on $target..."
    sudo testdisk "$target"
}

# Run PhotoRec for file recovery
run_photorec() {
    local source="$1"
    local case_name="$2"
    
    if [[ -z "$source" ]] || [[ -z "$case_name" ]]; then
        error "Usage: run_photorec <source_device_or_image> <case_name>"
        return 1
    fi
    
    local output_dir="$RECOVERED_DATA_DIR/$case_name/photorec_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$output_dir"
    
    log "Starting PhotoRec recovery from $source to $output_dir..."
    sudo photorec /d "$output_dir" "$source"
}

# Run Scalpel for file carving
run_scalpel() {
    local source="$1"
    local case_name="$2"
    
    if [[ -z "$source" ]] || [[ -z "$case_name" ]]; then
        error "Usage: run_scalpel <source_device_or_image> <case_name>"
        return 1
    fi
    
    local output_dir="$RECOVERED_DATA_DIR/$case_name/scalpel_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$output_dir"
    
    log "Starting Scalpel file carving from $source to $output_dir..."
    sudo scalpel -o "$output_dir" "$source"
}

# Run Foremost for file recovery
run_foremost() {
    local source="$1"
    local case_name="$2"
    
    if [[ -z "$source" ]] || [[ -z "$case_name" ]]; then
        error "Usage: run_foremost <source_device_or_image> <case_name>"
        return 1
    fi
    
    local output_dir="$RECOVERED_DATA_DIR/$case_name/foremost_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$output_dir"
    
    log "Starting Foremost recovery from $source to $output_dir..."
    sudo foremost -i "$source" -o "$output_dir"
}

# Mobile device functions
list_android_devices() {
    log "Scanning for Android devices..."
    adb devices -l
}

list_ios_devices() {
    log "Scanning for iOS devices..."
    idevice_id -l
    if [[ $? -eq 0 ]]; then
        for device in $(idevice_id -l); do
            echo "Device: $device"
            ideviceinfo -u "$device" | grep -E "(DeviceName|ProductType|ProductVersion)"
        done
    fi
}

# Android data extraction
extract_android_data() {
    local case_name="$1"
    
    if [[ -z "$case_name" ]]; then
        error "Usage: extract_android_data <case_name>"
        return 1
    fi
    
    local output_dir="$MOBILE_DATA_DIR/$case_name/android_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$output_dir"
    
    log "Extracting Android data to $output_dir..."
    
    # Check if device is rooted and accessible
    adb shell "su -c 'ls /data'" 2>/dev/null
    if [[ $? -eq 0 ]]; then
        log "Root access detected. Performing full extraction..."
        adb pull /data/data "$output_dir/app_data/"
        adb pull /sdcard "$output_dir/sdcard/"
    else
        warn "No root access. Limited extraction..."
        adb pull /sdcard "$output_dir/sdcard/"
    fi
    
    # Get device information
    adb shell getprop > "$output_dir/device_properties.txt"
    adb shell dumpsys > "$output_dir/system_dump.txt"
    
    log "Android extraction completed: $output_dir"
}

# iOS data extraction
extract_ios_data() {
    local case_name="$1"
    local device_id="$2"
    
    if [[ -z "$case_name" ]]; then
        error "Usage: extract_ios_data <case_name> [device_id]"
        return 1
    fi
    
    local output_dir="$MOBILE_DATA_DIR/$case_name/ios_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$output_dir"
    
    log "Extracting iOS data to $output_dir..."
    
    # Device information
    if [[ -n "$device_id" ]]; then
        ideviceinfo -u "$device_id" > "$output_dir/device_info.txt"
    else
        ideviceinfo > "$output_dir/device_info.txt"
    fi
    
    # Try to backup (requires device to be unlocked and trusted)
    warn "Make sure device is unlocked and trusted before backup..."
    if [[ -n "$device_id" ]]; then
        idevicebackup2 -u "$device_id" backup "$output_dir/backup"
    else
        idevicebackup2 backup "$output_dir/backup"
    fi
    
    log "iOS extraction completed: $output_dir"
}

# Quick recovery workflow
quick_recovery() {
    local device="$1"
    local case_name="$2"
    
    if [[ -z "$device" ]] || [[ -z "$case_name" ]]; then
        error "Usage: quick_recovery <device> <case_name>"
        return 1
    fi
    
    log "Starting quick recovery workflow for $device (case: $case_name)..."
    
    # Create disk image
    create_disk_image "$device" "$case_name"
    
    # Get the created image path
    local image_path=$(find "$DISK_IMAGES_DIR" -name "${case_name}_*.dd" | tail -1)
    
    # Run PhotoRec for file recovery
    run_photorec "$image_path" "$case_name"
    
    log "Quick recovery completed for case: $case_name"
}

# Generate recovery report
generate_report() {
    local case_name="$1"
    
    if [[ -z "$case_name" ]]; then
        error "Usage: generate_report <case_name>"
        return 1
    fi
    
    local report_file="$CASES_DIR/$case_name/recovery_report_$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "Data Recovery Report"
        echo "==================="
        echo "Case Name: $case_name"
        echo "Date: $(date)"
        echo "Operator: $(whoami)"
        echo ""
        
        echo "Disk Images:"
        find "$DISK_IMAGES_DIR" -name "*$case_name*" -type f
        echo ""
        
        echo "Recovered Data:"
        find "$RECOVERED_DATA_DIR/$case_name" -type d 2>/dev/null || echo "None"
        echo ""
        
        echo "Mobile Data:"
        find "$MOBILE_DATA_DIR/$case_name" -type d 2>/dev/null || echo "None"
        echo ""
        
        echo "Logs:"
        find "$LOGS_DIR" -name "*$case_name*" -o -name "recovery-$(date +%Y%m%d).log"
    } > "$report_file"
    
    log "Report generated: $report_file"
}

# Show help
show_help() {
    cat << EOF
Data Recovery Toolkit

USAGE:
    $0 <command> [arguments]

COMMANDS:
    list-devices              - List all storage devices
    create-image <device> <case>  - Create disk image using ddrescue
    testdisk <target>         - Run TestDisk for partition recovery
    photorec <source> <case>  - Run PhotoRec for file recovery
    scalpel <source> <case>   - Run Scalpel for file carving
    foremost <source> <case>  - Run Foremost for file recovery
    
    list-android              - List connected Android devices
    list-ios                  - List connected iOS devices
    extract-android <case>    - Extract Android device data
    extract-ios <case> [id]   - Extract iOS device data
    
    quick-recovery <device> <case> - Run complete recovery workflow
    generate-report <case>    - Generate recovery report
    
    help                      - Show this help

EXAMPLES:
    $0 list-devices
    $0 create-image /dev/sdb1 "evidence-001"
    $0 photorec /dev/sdb1 "evidence-001"
    $0 quick-recovery /dev/sdb "laptop-recovery"
    $0 extract-android "phone-case-001"

EOF
}

# Main execution
main() {
    check_root
    
    case "${1:-help}" in
        list-devices)
            list_devices
            ;;
        create-image)
            create_disk_image "$2" "$3"
            ;;
        testdisk)
            run_testdisk "$2"
            ;;
        photorec)
            run_photorec "$2" "$3"
            ;;
        scalpel)
            run_scalpel "$2" "$3"
            ;;
        foremost)
            run_foremost "$2" "$3"
            ;;
        list-android)
            list_android_devices
            ;;
        list-ios)
            list_ios_devices
            ;;
        extract-android)
            extract_android_data "$2"
            ;;
        extract-ios)
            extract_ios_data "$2" "$3"
            ;;
        quick-recovery)
            quick_recovery "$2" "$3"
            ;;
        generate-report)
            generate_report "$2"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"