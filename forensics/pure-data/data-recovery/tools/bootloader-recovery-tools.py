#!/usr/bin/env python3

"""
Pure Data - Android Bootloader and Recovery Tools
Advanced methods for enabling USB debugging through bootloader and recovery modes
Part of the Pure Data Professional Forensic Suite

LEGAL NOTICE: This tool is intended for use only on devices you own or 
have explicit legal authorization to access.
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime
from pathlib import Path

class AndroidBootloaderTools:
    def __init__(self):
        self.recovery_dir = Path.home() / "data-recovery"
        self.logs_dir = self.recovery_dir / "logs"
        self.tools_dir = self.recovery_dir / "tools"
        
        # Colors for output
        self.colors = {
            'RED': '\033[0;31m',
            'GREEN': '\033[0;32m',
            'YELLOW': '\033[1;33m',
            'BLUE': '\033[0;34m',
            'CYAN': '\033[0;36m',
            'NC': '\033[0m'
        }
    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color = self.colors.get(level, self.colors['NC'])
        print(f"{color}[{timestamp}] [{level}]{self.colors['NC']} {message}")
        
        # Log to file
        log_file = self.logs_dir / f"bootloader-tools-{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")
    
    def error(self, message):
        self.log(message, "RED")
    
    def success(self, message):
        self.log(message, "GREEN")
    
    def warn(self, message):
        self.log(message, "YELLOW")
    
    def info(self, message):
        self.log(message, "BLUE")
    
    def run_command(self, cmd, timeout=30):
        """Execute shell command with timeout"""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
    
    def check_fastboot_connection(self):
        """Check if device is connected via fastboot"""
        self.info("Checking fastboot connection...")
        code, stdout, stderr = self.run_command("fastboot devices")
        
        if code == 0 and stdout.strip():
            devices = [line for line in stdout.strip().split('\n') if line.strip()]
            if devices:
                self.success(f"Found {len(devices)} fastboot device(s)")
                return True
        
        self.warn("No fastboot devices found")
        return False
    
    def check_recovery_connection(self):
        """Check if device is connected via recovery mode"""
        self.info("Checking recovery connection...")
        code, stdout, stderr = self.run_command("adb devices")
        
        if "recovery" in stdout:
            self.success("Device detected in recovery mode")
            return True
        
        self.warn("No recovery devices found")
        return False
    
    def get_bootloader_info(self):
        """Get bootloader information"""
        if not self.check_fastboot_connection():
            return None
        
        self.info("Gathering bootloader information...")
        info = {}
        
        # Common fastboot variables to check
        variables = [
            'version-bootloader', 'version-baseband', 'version-hardware',
            'secure', 'unlocked', 'off-mode-charge', 'hw-revision',
            'serialno', 'product', 'partition-type', 'max-download-size'
        ]
        
        for var in variables:
            code, stdout, stderr = self.run_command(f"fastboot getvar {var}")
            if code == 0:
                # fastboot prints to stderr for some reason
                output = stderr + stdout
                for line in output.split('\n'):
                    if var in line and ':' in line:
                        value = line.split(':', 1)[1].strip()
                        info[var] = value
                        break
        
        return info
    
    def unlock_bootloader(self):
        """Attempt to unlock bootloader"""
        self.warn("BOOTLOADER UNLOCK WARNING:")
        print("- This will WIPE ALL DATA on the device")
        print("- Device warranty may be voided")
        print("- Only proceed if you own the device")
        print("")
        
        response = input("Continue with bootloader unlock? (type 'UNLOCK' to proceed): ")
        if response != "UNLOCK":
            self.info("Bootloader unlock cancelled")
            return False
        
        if not self.check_fastboot_connection():
            self.error("No fastboot device connected")
            return False
        
        self.info("Attempting bootloader unlock...")
        
        # Try common unlock commands
        unlock_commands = [
            "fastboot oem unlock",
            "fastboot flashing unlock",
            "fastboot oem unlock-go",
            "fastboot flashing unlock_critical"
        ]
        
        for cmd in unlock_commands:
            self.info(f"Trying: {cmd}")
            code, stdout, stderr = self.run_command(cmd)
            
            if code == 0:
                self.success("Bootloader unlock command executed successfully")
                self.info("Check device screen for confirmation prompt")
                return True
            else:
                self.warn(f"Command failed: {stderr}")
        
        self.error("All unlock attempts failed")
        return False
    
    def boot_recovery_image(self, recovery_path=None):
        """Boot temporary recovery image"""
        if not self.check_fastboot_connection():
            return False
        
        if not recovery_path:
            # Look for common recovery images
            possible_recoveries = [
                "/tmp/recovery.img",
                "/tmp/twrp.img",
                str(self.tools_dir / "recovery.img"),
                str(self.tools_dir / "twrp.img")
            ]
            
            recovery_path = None
            for path in possible_recoveries:
                if os.path.exists(path):
                    recovery_path = path
                    break
        
        if not recovery_path or not os.path.exists(recovery_path):
            self.error("No recovery image found. Please download a recovery image for your device.")
            self.info("Popular recovery images:")
            self.info("- TWRP: https://twrp.me/Devices/")
            self.info("- LineageOS Recovery: https://download.lineageos.org/")
            return False
        
        self.info(f"Booting recovery image: {recovery_path}")
        code, stdout, stderr = self.run_command(f"fastboot boot {recovery_path}")
        
        if code == 0:
            self.success("Recovery image booted successfully")
            self.info("Device should now be in custom recovery mode")
            time.sleep(5)  # Wait for boot
            return True
        else:
            self.error(f"Failed to boot recovery: {stderr}")
            return False
    
    def enable_debugging_via_recovery(self):
        """Enable USB debugging through recovery mode"""
        if not self.check_recovery_connection():
            self.error("Device not in recovery mode")
            return False
        
        self.info("Attempting to enable debugging via recovery...")
        
        # Mount system partition
        mount_commands = [
            "adb shell mount /system",
            "adb shell mount -o rw /system",
            "adb shell mount -t ext4 /dev/block/bootdevice/by-name/system /system"
        ]
        
        mounted = False
        for cmd in mount_commands:
            code, stdout, stderr = self.run_command(cmd)
            if code == 0:
                mounted = True
                break
        
        if not mounted:
            self.error("Could not mount system partition")
            return False
        
        self.success("System partition mounted")
        
        # Backup original build.prop
        backup_cmd = "adb shell cp /system/build.prop /system/build.prop.backup"
        self.run_command(backup_cmd)
        self.info("Created build.prop backup")
        
        # Add debugging properties
        debug_props = [
            "persist.sys.usb.config=adb",
            "ro.adb.secure=0",
            "ro.debuggable=1",
            "persist.service.adb.enable=1",
            "persist.service.debuggable=1"
        ]
        
        for prop in debug_props:
            cmd = f"adb shell 'echo \"{prop}\" >> /system/build.prop'"
            code, stdout, stderr = self.run_command(cmd)
            if code == 0:
                self.info(f"Added property: {prop}")
            else:
                self.warn(f"Failed to add property: {prop}")
        
        # Set correct permissions
        self.run_command("adb shell chmod 644 /system/build.prop")
        
        self.success("USB debugging properties added to build.prop")
        self.info("Rebooting device...")
        
        self.run_command("adb shell reboot")
        return True
    
    def create_magisk_module(self):
        """Create Magisk module for debugging enabler"""
        module_dir = self.tools_dir / "magisk_debug_enabler"
        module_dir.mkdir(exist_ok=True)
        
        # Module.prop file
        module_prop = """id=usb_debug_enabler
name=USB Debug Enabler
version=v1.0
versionCode=1
author=DataRecoveryToolkit
description=Enables USB debugging and ADB access
"""
        
        with open(module_dir / "module.prop", 'w') as f:
            f.write(module_prop)
        
        # Service.sh file
        service_sh = """#!/system/bin/sh
# USB Debug Enabler Service Script

# Enable USB debugging
setprop persist.sys.usb.config adb
setprop ro.adb.secure 0
setprop ro.debuggable 1
setprop persist.service.adb.enable 1

# Start ADB daemon
start adbd

# Log the activation
echo "$(date): USB debugging enabled by Magisk module" >> /data/debug_enabler.log
"""
        
        with open(module_dir / "service.sh", 'w') as f:
            f.write(service_sh)
        
        # Make service.sh executable
        os.chmod(module_dir / "service.sh", 0o755)
        
        self.success(f"Magisk module created at: {module_dir}")
        self.info("To install:")
        self.info("1. Copy the module directory to /data/adb/modules/")
        self.info("2. Reboot device")
        self.info("3. USB debugging should be automatically enabled")
        
        return module_dir
    
    def bypass_frp_lock(self):
        """Methods for bypassing Factory Reset Protection"""
        self.warn("FRP Bypass Methods (Educational/Legal use only)")
        print("\nCommon FRP bypass methods:")
        print("1. Emergency call method (older Android versions)")
        print("2. Chrome browser exploit (patched in newer versions)")
        print("3. ADB sideload method (requires unlocked bootloader)")
        print("4. Combination firmware method (Samsung devices)")
        print("5. FRP bypass APKs (device-specific)")
        print("\nNote: Most modern devices have patched these vulnerabilities")
        print("Professional tools may be required for newer devices")
    
    def generate_device_report(self):
        """Generate comprehensive device report"""
        report_file = self.logs_dir / f"device-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "operator": os.getenv('USER', 'unknown'),
            "fastboot_info": None,
            "recovery_available": False,
            "bootloader_unlocked": None
        }
        
        # Gather fastboot information
        if self.check_fastboot_connection():
            report["fastboot_info"] = self.get_bootloader_info()
            
            # Check if bootloader is unlocked
            info = report["fastboot_info"]
            if info and "unlocked" in info:
                report["bootloader_unlocked"] = info["unlocked"] == "yes"
        
        # Check recovery availability
        report["recovery_available"] = self.check_recovery_connection()
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.success(f"Device report saved to: {report_file}")
        return report_file

def main():
    tools = AndroidBootloaderTools()
    
    if len(sys.argv) < 2:
        print(f"{tools.colors['CYAN']}Android Bootloader & Recovery Tools{tools.colors['NC']}")
        print("=" * 40)
        print("Commands:")
        print("  check-fastboot    - Check fastboot connection")
        print("  check-recovery    - Check recovery connection")
        print("  bootloader-info   - Get bootloader information")
        print("  unlock-bootloader - Unlock bootloader (DANGEROUS)")
        print("  boot-recovery     - Boot temporary recovery image")
        print("  enable-debug-recovery - Enable debugging via recovery")
        print("  create-magisk-module  - Create Magisk debugging module")
        print("  frp-bypass       - Show FRP bypass methods")
        print("  device-report    - Generate comprehensive device report")
        print("")
        print("Usage: python3 bootloader-recovery-tools.py <command>")
        return
    
    command = sys.argv[1]
    
    # Legal disclaimer for destructive operations
    destructive_commands = ['unlock-bootloader', 'enable-debug-recovery']
    if command in destructive_commands:
        print(f"{tools.colors['RED']}LEGAL DISCLAIMER:{tools.colors['NC']}")
        print("This tool is intended for use only on devices you own or")
        print("have explicit legal authorization to access.")
        print("Unauthorized access may be illegal in your jurisdiction.")
        print("")
        auth = input("Do you have legal authorization? (yes/no): ")
        if auth.lower() != 'yes':
            tools.error("Legal authorization required. Exiting.")
            return
    
    if command == "check-fastboot":
        tools.check_fastboot_connection()
    
    elif command == "check-recovery":
        tools.check_recovery_connection()
    
    elif command == "bootloader-info":
        info = tools.get_bootloader_info()
        if info:
            tools.success("Bootloader Information:")
            for key, value in info.items():
                print(f"  {key}: {value}")
        else:
            tools.error("Could not retrieve bootloader information")
    
    elif command == "unlock-bootloader":
        tools.unlock_bootloader()
    
    elif command == "boot-recovery":
        recovery_path = sys.argv[2] if len(sys.argv) > 2 else None
        tools.boot_recovery_image(recovery_path)
    
    elif command == "enable-debug-recovery":
        tools.enable_debugging_via_recovery()
    
    elif command == "create-magisk-module":
        tools.create_magisk_module()
    
    elif command == "frp-bypass":
        tools.bypass_frp_lock()
    
    elif command == "device-report":
        tools.generate_device_report()
    
    else:
        tools.error(f"Unknown command: {command}")

if __name__ == "__main__":
    main()