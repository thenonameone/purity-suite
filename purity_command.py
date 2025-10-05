#!/usr/bin/env python3
"""
🌟 PURITY ECOSYSTEM v3.0 - Streamlined Command Center
Advanced Intelligence Suite with Real-Time Tweaks
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
import threading

# Colors for terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class PurityEcosystem:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.config_file = self.base_path / "suite" / "config" / "ecosystem_config.json"
        self.load_config()
        self.setup_paths()
        
    def load_config(self):
        """Load or create ecosystem configuration"""
        default_config = {
            "version": "3.0.0",
            "last_updated": datetime.now().isoformat(),
            "tools": {
                "pure-face": {"status": "active", "path": "intelligence/pure-face", "command": "pure_face.py"},
                "pure-geo": {"status": "active", "path": "intelligence/pure-geo", "command": "launch_pure_geo.sh"},
                "purity-quest": {"status": "active", "path": "intelligence/purity-quest", "command": "purity_quest.py"},
                "pure-data": {"status": "active", "path": "forensics/pure-data/data-recovery", "command": "pure-data.sh"},
                "pure-usb": {"status": "active", "path": "forensics/pure-usb", "command": "pure_usb.py"},
                "pure-pics": {"status": "active", "path": "forensics/pure-pics", "command": "Pure_Pics.py"},
                "anonymity-help": {"status": "active", "path": "privacy/anonymity", "command": "anonymity-help", "type": "system"},
                "go-clear": {"status": "active", "path": "privacy/anonymity", "command": "go-clear", "type": "system"}
            },
            "quick_access": {
                "1": "pure-face",
                "2": "pure-geo", 
                "3": "purity-quest",
                "4": "pure-data",
                "5": "pure-usb",
                "6": "pure-pics",
                "7": "anonymity-help",
                "8": "go-clear"
            },
            "tweaks": {
                "auto_backup": True,
                "verbose_logging": True,
                "performance_mode": "balanced",
                "theme": "matrix"
            }
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Save current configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_paths(self):
        """Setup all ecosystem paths"""
        self.intelligence_path = self.base_path / "intelligence"
        self.forensics_path = self.base_path / "forensics"
        self.logs_path = self.base_path / "logs" / "current"
        self.scripts_path = self.base_path / "scripts"
        
        # Create log directory
        self.logs_path.mkdir(parents=True, exist_ok=True)
    
    def log_activity(self, activity, tool=None):
        """Log ecosystem activities"""
        if self.config["tweaks"]["verbose_logging"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {activity}"
            if tool:
                log_entry += f" - Tool: {tool}"
            
            with open(self.logs_path / "ecosystem.log", "a") as f:
                f.write(log_entry + "\n")
    
    def show_banner(self):
        """Display Purity Ecosystem banner"""
        theme = self.config["tweaks"]["theme"]
        
        if theme == "matrix":
            color = Colors.GREEN
        elif theme == "cyber":
            color = Colors.CYAN
        else:
            color = Colors.BLUE
        
        print(f"{color}{Colors.BOLD}")
        print("  ███████╗ ██╗   ██╗ ██████╗  ██╗ ████████╗ ██╗   ██╗")
        print("  ██╔══██║ ██║   ██║ ██╔══██╗ ██║ ╚══██╔══╝ ██║   ██║")
        print("  ███████║ ██║   ██║ ██████╔╝ ██║    ██║    ╚██╗ ██╔╝")
        print("  ██╔════╝ ██║   ██║ ██╔══██╗ ██║    ██║     ╚████╔╝ ")
        print("  ██║      ╚██████╔╝ ██║  ██║ ██║    ██║      ╚██╔╝  ")
        print("  ╚═╝       ╚═════╝  ╚═╝  ╚═╝ ╚═╝    ╚═╝       ╚═╝   ")
        print()
        print("  ███████╗  ██████╗  ██████╗  ███████╗ ██╗   ██╗ ███████╗ ████████╗ ███████╗ ███╗   ███╗")
        print("  ██╔════╝ ██╔════╝ ██╔═══██╗ ██╔════╝ ╚██╗ ██╔╝ ██╔════╝ ╚══██╔══╝ ██╔════╝ ████╗ ████║")
        print("  █████╗   ██║      ██║   ██║ ███████╗  ╚████╔╝  ███████╗    ██║    █████╗   ██╔████╔██║")
        print("  ██╔══╝   ██║      ██║   ██║ ╚════██║   ╚██╔╝   ╚════██║    ██║    ██╔══╝   ██║╚██╔╝██║")
        print("  ███████╗ ╚██████╗ ╚██████╔╝ ███████║    ██║    ███████║    ██║    ███████╗ ██║ ╚═╝ ██║")
        print("  ╚══════╝  ╚═════╝  ╚═════╝  ╚══════╝    ╚═╝    ╚══════╝    ╚═╝    ╚══════╝ ╚═╝     ╚═╝")
        print(f"{Colors.END}")
        print(f"{Colors.CYAN}                    Advanced Intelligence Suite v{self.config['version']}{Colors.END}")
        print(f"{Colors.PURPLE}                    Streamlined • Real-Time Tweaks • Production Ready{Colors.END}")
        print("=" * 90)
    
    def check_tool_status(self, tool_name):
        """Check if tool is ready and accessible"""
        tool_info = self.config["tools"].get(tool_name, {})
        
        # Special handling for system anonymity commands
        if tool_info.get("type") == "system":
            command = tool_info.get("command", "")
            try:
                result = subprocess.run(["which", command], capture_output=True, text=True)
                if result.returncode == 0:
                    return "✅ READY"
                else:
                    return "❌ MISSING"
            except:
                return "❌ MISSING"
        
        # Original tool checking logic
        tool_path = self.base_path / tool_info.get("path", "")
        
        if tool_path.exists():
            command_file = tool_path / tool_info.get("command", "")
            if command_file.exists():
                return "✅ READY"
            else:
                return "⚠️  CHECK"
        return "❌ MISSING"
    
    def show_main_menu(self):
        """Display main ecosystem menu"""
        os.system('clear')
        self.show_banner()
        
        print(f"{Colors.YELLOW}{Colors.BOLD}🎯 INTELLIGENCE SUITE:{Colors.END}")
        print("─" * 50)
        for i in range(1, 4):
            tool_key = str(i)
            tool_name = self.config["quick_access"][tool_key]
            status = self.check_tool_status(tool_name)
            tool_display = tool_name.replace("-", " ").title()
            
            descriptions = {
                "Pure Face": "Facial Recognition & OSINT Intelligence",
                "Pure Geo": "AI Geolocalization Intelligence System", 
                "Purity Quest": "OSINT Investigation Platform"
            }
            
            desc = descriptions.get(tool_display, "Advanced intelligence tool")
            print(f"  [{i}] 🧠 {Colors.BOLD}{tool_display:<15}{Colors.END} - {desc:<40} {status}")
        
        print(f"\n{Colors.YELLOW}{Colors.BOLD}🔧 FORENSICS SUITE:{Colors.END}")
        print("─" * 50)
        for i in range(4, 7):
            tool_key = str(i)
            tool_name = self.config["quick_access"][tool_key]
            status = self.check_tool_status(tool_name)
            tool_display = tool_name.replace("-", " ").title()
            
            descriptions = {
                "Pure Data": "Digital Forensics & Data Recovery",
                "Pure Usb": "USB Device Analysis & Forensics",
                "Pure Pics": "Image Forensics & Analysis"
            }
            
            desc = descriptions.get(tool_display, "Advanced forensics tool")
            print(f"  [{i}] 🔍 {Colors.BOLD}{tool_display:<15}{Colors.END} - {desc:<40} {status}")
        
        print(f"\n{Colors.YELLOW}{Colors.BOLD}🕵️ PRIVACY & ANONYMITY:{Colors.END}")
        print("─" * 50)
        for i in range(7, 9):
            tool_key = str(i)
            if tool_key in self.config["quick_access"]:
                tool_name = self.config["quick_access"][tool_key]
                status = self.check_tool_status(tool_name)
                tool_display = tool_name.replace("-", " ").title()
                
                descriptions = {
                    "Anonymity Help": "📚 Complete Anonymity Command Reference",
                    "Go Clear": "🗡️ Launch Go Clear Anonymity Control Center (GUI)"
                }
                
                desc = descriptions.get(tool_display, "Privacy protection tool")
                icons = {"Anonymity Help": "📚", "Go Clear": "🗡️"}
                icon = icons.get(tool_display, "🛡️")
                print(f"  [{i}] {icon} {Colors.BOLD}{tool_display:<15}{Colors.END} - {desc:<40} {status}")
        
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚡ REAL-TIME MANAGEMENT:{Colors.END}")
        print("─" * 50)
        print(f"  [t] 🛠️  {Colors.BOLD}Tweak Center{Colors.END}      - Real-time configuration & optimization")
        print(f"  [s] 📊 {Colors.BOLD}System Status{Colors.END}     - Health monitoring & performance stats")
        print(f"  [u] 🔄 {Colors.BOLD}Update Hub{Colors.END}        - Tool updates & maintenance")
        print(f"  [b] 💾 {Colors.BOLD}Backup Manager{Colors.END}    - Data protection & recovery")
        
        print(f"\n{Colors.YELLOW}{Colors.BOLD}📖 SUPPORT:{Colors.END}")
        print("─" * 50)
        print(f"  [h] 📚 Help & Documentation    [l] 📋 View Logs    [q] 🚪 Exit")
        
        print("=" * 90)
        current_path = str(self.base_path).replace("/home/xx/", "~/")
        print(f"📍 Location: {current_path} | 🎯 Active Tools: 8 | 💚 System Health: Excellent")
        print("=" * 90)
    
    def launch_tool(self, tool_name):
        """Launch selected tool with environment activation"""
        print(f"{Colors.BLUE}🚀 Launching {tool_name.replace('-', ' ').title()}...{Colors.END}")
        self.log_activity(f"Launching tool: {tool_name}")
        
        tool_info = self.config["tools"][tool_name]
        command = tool_info["command"]
        
        # Special handling for system anonymity commands
        if tool_info.get("type") == "system":
            try:
                print(f"{Colors.CYAN}🔧 Executing system command: {command}{Colors.END}")
                
                # Special handling for anonymity commands
                if tool_name in ["make-anonymous", "make-visible"]:
                    subprocess.run([command], check=True)
                elif tool_name == "anonymity-help":
                    subprocess.run([command], check=True)
                else:
                    subprocess.run([command], check=True)
                    
            except subprocess.CalledProcessError as e:
                print(f"{Colors.RED}❌ Error executing {tool_name}: {e}{Colors.END}")
            except FileNotFoundError:
                print(f"{Colors.RED}❌ Command not found: {command}{Colors.END}")
            
            input(f"\n{Colors.YELLOW}Press Enter to return to main menu...{Colors.END}")
            return
        
        # Original tool launching logic for non-system tools
        tool_path = self.base_path / tool_info["path"]
        
        # Change to tool directory
        original_path = os.getcwd()
        os.chdir(tool_path)
        
        try:
            if tool_name == "pure-geo":
                # Special handling for Pure GEO
                subprocess.run(["bash", command], check=True)
            elif command.endswith(".py"):
                # Python tools with virtual environment
                if (self.base_path / "environment" / "face_recognition_env").exists():
                    venv_python = self.base_path / "environment" / "face_recognition_env" / "bin" / "python"
                    subprocess.run([str(venv_python), command], check=True)
                else:
                    subprocess.run(["python3", command], check=True)
            else:
                # Execute using absolute path within the tool directory to avoid PATH dependency
                cmd_path = tool_path / command
                subprocess.run([str(cmd_path)], check=True)
                
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}❌ Error launching {tool_name}: {e}{Colors.END}")
        except FileNotFoundError:
            print(f"{Colors.RED}❌ Tool not found: {tool_name}{Colors.END}")
        finally:
            os.chdir(original_path)
        
        input(f"\n{Colors.YELLOW}Press Enter to return to main menu...{Colors.END}")
    
    def tweak_center(self):
        """Real-time configuration and optimization"""
        while True:
            os.system('clear')
            print(f"{Colors.GREEN}{Colors.BOLD}🛠️  PURITY TWEAK CENTER{Colors.END}")
            print("=" * 60)
            
            print(f"{Colors.YELLOW}CURRENT SETTINGS:{Colors.END}")
            print(f"  🎨 Theme: {self.config['tweaks']['theme']}")
            print(f"  📊 Performance: {self.config['tweaks']['performance_mode']}")
            print(f"  📝 Verbose Logging: {self.config['tweaks']['verbose_logging']}")
            print(f"  💾 Auto Backup: {self.config['tweaks']['auto_backup']}")
            
            print(f"\n{Colors.YELLOW}TWEAK OPTIONS:{Colors.END}")
            print("  [1] 🎨 Change Theme (matrix/cyber/classic)")
            print("  [2] ⚡ Performance Mode (turbo/balanced/eco)")
            print("  [3] 📝 Toggle Verbose Logging")
            print("  [4] 💾 Toggle Auto Backup")
            print("  [5] 🔄 Reset to Defaults")
            print("  [r] 🔁 Reload Configuration")
            print("  [b] ⬅️  Back to Main Menu")
            
            choice = input(f"\n{Colors.CYAN}Select tweak: {Colors.END}").lower().strip()
            
            if choice == '1':
                themes = ['matrix', 'cyber', 'classic']
                print(f"Available themes: {', '.join(themes)}")
                new_theme = input("Enter theme: ").lower().strip()
                if new_theme in themes:
                    self.config['tweaks']['theme'] = new_theme
                    self.save_config()
                    print(f"✅ Theme changed to {new_theme}")
                    
            elif choice == '2':
                modes = ['turbo', 'balanced', 'eco']
                print(f"Available modes: {', '.join(modes)}")
                new_mode = input("Enter mode: ").lower().strip()
                if new_mode in modes:
                    self.config['tweaks']['performance_mode'] = new_mode
                    self.save_config()
                    print(f"✅ Performance mode set to {new_mode}")
                    
            elif choice == '3':
                self.config['tweaks']['verbose_logging'] = not self.config['tweaks']['verbose_logging']
                self.save_config()
                status = "enabled" if self.config['tweaks']['verbose_logging'] else "disabled"
                print(f"✅ Verbose logging {status}")
                
            elif choice == '4':
                self.config['tweaks']['auto_backup'] = not self.config['tweaks']['auto_backup']
                self.save_config()
                status = "enabled" if self.config['tweaks']['auto_backup'] else "disabled"
                print(f"✅ Auto backup {status}")
                
            elif choice == '5':
                confirm = input("Reset all settings to defaults? (y/N): ").lower().strip()
                if confirm == 'y':
                    self.config['tweaks'] = {
                        "auto_backup": True,
                        "verbose_logging": True,
                        "performance_mode": "balanced",
                        "theme": "matrix"
                    }
                    self.save_config()
                    print("✅ Settings reset to defaults")
                    
            elif choice == 'r':
                self.load_config()
                print("✅ Configuration reloaded")
                
            elif choice == 'b':
                break
            
            if choice != 'b':
                input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    def system_status(self):
        """Show comprehensive system status"""
        os.system('clear')
        print(f"{Colors.GREEN}{Colors.BOLD}📊 PURITY ECOSYSTEM STATUS{Colors.END}")
        print("=" * 70)
        
        # Tool Status
        print(f"{Colors.YELLOW}TOOL STATUS:{Colors.END}")
        for tool_name in self.config["tools"]:
            status = self.check_tool_status(tool_name)
            tool_display = tool_name.replace("-", " ").title()
            print(f"  {tool_display:<20} {status}")
        
        # System Resources
        print(f"\n{Colors.YELLOW}SYSTEM RESOURCES:{Colors.END}")
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            print(f"  CPU Usage:     {cpu_percent:.1f}%")
            print(f"  Memory Used:   {memory.percent:.1f}% ({memory.used // 1024**3}GB / {memory.total // 1024**3}GB)")
            print(f"  Disk Usage:    {disk.percent:.1f}% ({disk.used // 1024**3}GB / {disk.total // 1024**3}GB)")
        except ImportError:
            print("  System monitoring: Install 'psutil' for detailed stats")
        
        # Environment Status
        print(f"\n{Colors.YELLOW}ENVIRONMENT STATUS:{Colors.END}")
        venv_path = self.base_path / "environment" / "face_recognition_env"
        if venv_path.exists():
            print("  Virtual Environment: ✅ Active")
        else:
            print("  Virtual Environment: ⚠️  Not Found")
        
        # Recent Activity
        print(f"\n{Colors.YELLOW}RECENT ACTIVITY:{Colors.END}")
        log_file = self.logs_path / "ecosystem.log"
        if log_file.exists():
            with open(log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-5:]:  # Show last 5 activities
                    print(f"  {line.strip()}")
        else:
            print("  No recent activity logged")
        
        input(f"\n{Colors.YELLOW}Press Enter to return...{Colors.END}")
    
    def run(self):
        """Main ecosystem loop"""
        while True:
            self.show_main_menu()
            choice = input(f"{Colors.CYAN}Enter your choice: {Colors.END}").strip().lower()
            
            # Quick access to tools (1-9)
            if choice in self.config["quick_access"]:
                tool_name = self.config["quick_access"][choice]
                self.launch_tool(tool_name)
                
            # Management options
            elif choice == 't':
                self.tweak_center()
            elif choice == 's':
                self.system_status()
            elif choice == 'u':
                print("🔄 Update hub - Feature coming soon!")
                input("Press Enter to continue...")
            elif choice == 'b':
                print("💾 Backup manager - Feature coming soon!")
                input("Press Enter to continue...")
            elif choice == 'h':
                print("📚 Opening documentation...")
                subprocess.run(["less", str(self.base_path / "docs" / "README.md")], check=False)
            elif choice == 'l':
                log_file = self.logs_path / "ecosystem.log"
                if log_file.exists():
                    subprocess.run(["less", str(log_file)], check=False)
                else:
                    print("No logs found")
                    input("Press Enter to continue...")
            elif choice == 'q':
                print(f"{Colors.GREEN}🌟 Thanks for using Purity Ecosystem! Stay secure! 🛡️{Colors.END}")
                self.log_activity("Ecosystem shutdown")
                break
            else:
                print(f"{Colors.RED}❌ Invalid choice. Please try again.{Colors.END}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        ecosystem = PurityEcosystem()
        ecosystem.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Ecosystem interrupted. Exiting safely...{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}❌ Critical error: {e}{Colors.END}")
        sys.exit(1)