#!/usr/bin/env python3
"""
Purity Quest - GUI Version with tkinter
Simple, functional GUI with clear input fields
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import re
import json
import requests
from datetime import datetime
import threading
import time

# =============================================================================
# CONFIGURATION
# =============================================================================

class OSINTConfig:
    def __init__(self):
        self.TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
        self.TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
        self.HUNTER_API_KEY = os.getenv('HUNTER_API_KEY', '')
        self.SERPAPI_KEY = os.getenv('SERPAPI_KEY', '')
        self.HIBP_API_KEY = os.getenv('HIBP_API_KEY', '')
        self.IPQS_API_KEY = os.getenv('IPQS_API_KEY', '')
        self.GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
        self.GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')

config = OSINTConfig()

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def format_phone_number(phone):
    """Format phone number in different ways"""
    clean = re.sub(r'[^\d]', '', phone)
    
    if len(clean) == 10:
        formatted = f"({clean[:3]}) {clean[3:6]}-{clean[6:]}"
        dashed = f"{clean[:3]}-{clean[3:6]}-{clean[6:]}"
        dotted = f"{clean[:3]}.{clean[3:6]}.{clean[6:]}"
        return {
            'original': phone,
            'clean': clean,
            'formatted': formatted,
            'dashed': dashed,
            'dotted': dotted
        }
    elif len(clean) == 11 and clean.startswith('1'):
        formatted = f"({clean[1:4]}) {clean[4:7]}-{clean[7:]}"
        dashed = f"{clean[1:4]}-{clean[4:7]}-{clean[7:]}"
        return {
            'original': phone,
            'clean': clean[1:],
            'formatted': formatted,
            'dashed': dashed,
            'dotted': f"{clean[1:4]}.{clean[4:7]}.{clean[7:]}"
        }
    else:
        return {'original': phone, 'clean': clean, 'formatted': phone, 'dashed': phone, 'dotted': phone}

def validate_email(email):
    """Basic email validation"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(pattern, email) is not None

def get_email_provider(email):
    """Identify email provider"""
    if '@' not in email:
        return "Invalid"
    
    domain = email.split('@')[1].lower()
    providers = {
        'gmail.com': 'Gmail', 'googlemail.com': 'Gmail',
        'outlook.com': 'Outlook', 'hotmail.com': 'Hotmail',
        'yahoo.com': 'Yahoo', 'aol.com': 'AOL',
        'icloud.com': 'iCloud', 'protonmail.com': 'ProtonMail'
    }
    return providers.get(domain, f"Custom ({domain})")

# =============================================================================
# SEARCH QUERY GENERATORS
# =============================================================================

PHONE_QUERIES = {
    '🔴 Basic Searches': [
        '"{phone}"',
        '"{phone_formatted}"',
        'phone number "{phone}"'
    ],
    '💀 Social Media': [
        '"{phone}" site:facebook.com',
        '"{phone}" site:instagram.com',
        '"{phone}" site:twitter.com',
        '"{phone}" site:linkedin.com'
    ],
    '🏴‍☠️ Business Directory': [
        '"{phone}" yellowpages',
        '"{phone}" whitepages',
        '"{phone}" business directory'
    ],
    '🎯 Address & Location': [
        '"{phone}" address',
        '"{phone}" street city location',
        '"{phone}" property owner'
    ],
    '⚔️ Security & Scam Check': [
        '"{phone}" scam spam fraud',
        '"{phone}" robocall complaint',
        '"{phone}" reverse phone lookup'
    ]
}

EMAIL_QUERIES = {
    '🔴 Basic Searches': [
        '"{email}"',
        '"{email_username}" email'
    ],
    '💀 Social Platforms': [
        '"{email}" site:facebook.com',
        '"{email}" site:linkedin.com',
        '"{email}" site:twitter.com'
    ],
    '🏴‍☠️ Professional': [
        '"{email}" linkedin resume CV',
        '"{email}" business contact'
    ],
    '⚔️ Security': [
        '"{email}" breach leaked hacked',
        '"{email}" security incident'
    ]
}

def generate_phone_queries(phone_data):
    """Generate comprehensive phone number search queries"""
    formatted_queries = {}
    
    for category, query_templates in PHONE_QUERIES.items():
        formatted_queries[category] = []
        for template in query_templates:
            try:
                query = template.format(
                    phone=phone_data['clean'],
                    phone_formatted=phone_data['formatted']
                )
                formatted_queries[category].append(query)
            except KeyError:
                continue
    
    return formatted_queries

def generate_email_queries(email):
    """Generate comprehensive email search queries"""
    if '@' in email:
        username = email.split('@')[0]
        domain = email.split('@')[1]
    else:
        username = email
        domain = ""
    
    formatted_queries = {}
    
    for category, query_templates in EMAIL_QUERIES.items():
        formatted_queries[category] = []
        for template in query_templates:
            try:
                query = template.format(
                    email=email,
                    email_username=username,
                    email_domain=domain
                )
                formatted_queries[category].append(query)
            except KeyError:
                continue
    
    return formatted_queries

# =============================================================================
# API INVESTIGATION FUNCTIONS
# =============================================================================

def check_phone_with_twilio(phone):
    """Check phone number with Twilio API"""
    if not config.TWILIO_ACCOUNT_SID or not config.TWILIO_AUTH_TOKEN:
        return None
    
    try:
        import base64
        auth_string = f"{config.TWILIO_ACCOUNT_SID}:{config.TWILIO_AUTH_TOKEN}"
        auth_bytes = base64.b64encode(auth_string.encode()).decode()
        
        headers = {'Authorization': f'Basic {auth_bytes}'}
        url = f"https://lookups.twilio.com/v1/PhoneNumbers/{phone}"
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'valid': True,
                'carrier': data.get('carrier', {}).get('name', 'Unknown'),
                'type': data.get('carrier', {}).get('type', 'Unknown'),
                'country': data.get('country_code', 'Unknown')
            }
    except Exception as e:
        print(f"Twilio API error: {e}")
    
    return None

def check_email_with_hunter(email):
    """Check email with Hunter.io API"""
    if not config.HUNTER_API_KEY:
        return None
    
    try:
        url = f"https://api.hunter.io/v2/email-verifier"
        params = {'email': email, 'api_key': config.HUNTER_API_KEY}
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()['data']
            return {
                'valid': data.get('result') == 'deliverable',
                'score': data.get('score', 0),
                'smtp_valid': data.get('smtp_check', False),
                'disposable': data.get('disposable', False),
                'webmail': data.get('webmail', False)
            }
    except Exception as e:
        print(f"Hunter.io API error: {e}")
    
    return None

def check_email_breaches(email):
    """Check email in data breaches with HIBP API"""
    if not config.HIBP_API_KEY:
        return None
    
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {'hibp-api-key': config.HIBP_API_KEY}
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            breaches = response.json()
            return {
                'breach_count': len(breaches),
                'breaches': [breach['Name'] for breach in breaches[:5]]  # Top 5
            }
        elif response.status_code == 404:
            return {'breach_count': 0, 'breaches': []}
    except Exception as e:
        print(f"HIBP API error: {e}")
    
    return None

def search_with_serpapi(query, api_key):
    """Search using SerpAPI"""
    if not api_key:
        return None
    
    try:
        url = "https://serpapi.com/search"
        params = {
            'q': query,
            'api_key': api_key,
            'num': 5
        }
        
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            results = []
            
            for result in data.get('organic_results', [])[:3]:
                results.append({
                    'title': result.get('title', ''),
                    'link': result.get('link', ''),
                    'snippet': result.get('snippet', '')
                })
            
            return results
    except Exception as e:
        print(f"SerpAPI error: {e}")
    
    return None

def check_ipqs_phone(phone):
    """Check phone with IPQualityScore API"""
    if not config.IPQS_API_KEY:
        return None
    
    try:
        url = f"https://ipqualityscore.com/api/json/phone/{config.IPQS_API_KEY}/{phone}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'valid': data.get('valid', False),
                'fraud_score': data.get('fraud_score', 0),
                'carrier': data.get('carrier', 'Unknown'),
                'line_type': data.get('line_type', 'Unknown'),
                'country': data.get('country', 'Unknown'),
                'region': data.get('region', 'Unknown'),
                'city': data.get('city', 'Unknown')
            }
    except Exception as e:
        print(f"IPQS API error: {e}")
    
    return None

def open_api_sites():
    """Open all API signup sites in browser"""
    import subprocess
    
    api_sites = [
        "https://serpapi.com/",
        "https://www.ipqualityscore.com/",
        "https://hunter.io/",
        "https://haveibeenpwned.com/API/v3"
    ]
    
    try:
        # Try chromium first, then fallback to firefox
        subprocess.Popen(['chromium'] + api_sites)
        return True
    except FileNotFoundError:
        try:
            for site in api_sites:
                subprocess.Popen(['firefox', site])
            return True
        except FileNotFoundError:
            return False

# =============================================================================
# MAIN GUI APPLICATION
# =============================================================================

class PurityQuestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🫁 PURITY IS KEY 🫁")
        self.root.geometry("1200x800")
        self.root.configure(bg='#000000')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure('Title.TLabel', 
                           background='#000000', 
                           foreground='#ff0000', 
                           font=('Arial', 24, 'bold'))
        
        self.style.configure('Input.TLabel', 
                           background='#000000', 
                           foreground='#ffffff', 
                           font=('Arial', 14, 'bold'))
        
        self.style.configure('Red.TButton', 
                           background='#ff0000', 
                           foreground='#000000',
                           font=('Arial', 14, 'bold'))
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        
        # Title
        title_label = ttk.Label(self.root, 
                               text="🫁 PURITY IS KEY 🫁", 
                               style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Phone Investigation Tab
        phone_frame = ttk.Frame(notebook)
        notebook.add(phone_frame, text="📱 Phone CPR")
        self.create_phone_tab(phone_frame)
        
        # Email Investigation Tab
        email_frame = ttk.Frame(notebook)
        notebook.add(email_frame, text="📧 Email Life Support")
        self.create_email_tab(email_frame)
        
        # Combined Investigation Tab
        combined_frame = ttk.Frame(notebook)
        notebook.add(combined_frame, text="🚨 Emergency CPR")
        self.create_combined_tab(combined_frame)
        
        # Settings Tab
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙️ API Settings")
        self.create_settings_tab(settings_frame)
        
        # API Configuration Tab
        api_config_frame = ttk.Frame(notebook)
        notebook.add(api_config_frame, text="🔑 API Keys")
        self.create_api_config_tab(api_config_frame)
    
    def create_phone_tab(self, parent):
        """Create phone investigation tab"""
        # Input section
        input_frame = ttk.LabelFrame(parent, text="📱 Patient Phone Number", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(input_frame, text="Enter phone number for resuscitation:", 
                 style='Input.TLabel').pack(anchor='w')
        
        self.phone_entry = ttk.Entry(input_frame, font=('Arial', 16), width=40)
        self.phone_entry.pack(fill='x', pady=5)
        
        ttk.Button(input_frame, text="🫁 RESUSCITATE", 
                  command=self.investigate_phone, style='Red.TButton').pack(pady=5)
        
        # Results section
        results_frame = ttk.LabelFrame(parent, text="🏥 Treatment Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.phone_results = scrolledtext.ScrolledText(results_frame, 
                                                      bg='#1a0000', 
                                                      fg='#ffffff',
                                                      font=('Courier', 14))
        self.phone_results.pack(fill='both', expand=True)
    
    def create_email_tab(self, parent):
        """Create email investigation tab"""
        # Input section
        input_frame = ttk.LabelFrame(parent, text="📧 Patient Email Address", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(input_frame, text="Enter email address for emergency treatment:", 
                 style='Input.TLabel').pack(anchor='w')
        
        self.email_entry = ttk.Entry(input_frame, font=('Arial', 16), width=40)
        self.email_entry.pack(fill='x', pady=5)
        
        ttk.Button(input_frame, text="⚕️ REVIVE", 
                  command=self.investigate_email, style='Red.TButton').pack(pady=5)
        
        # Results section
        results_frame = ttk.LabelFrame(parent, text="🏥 Treatment Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.email_results = scrolledtext.ScrolledText(results_frame, 
                                                      bg='#1a0000', 
                                                      fg='#ffffff',
                                                      font=('Courier', 14))
        self.email_results.pack(fill='both', expand=True)
    
    def create_combined_tab(self, parent):
        """Create combined investigation tab"""
        # Input section
        input_frame = ttk.LabelFrame(parent, text="🚨 Emergency Resuscitation (Both Patients)", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Email input
        ttk.Label(input_frame, text="Email Patient:", style='Input.TLabel').pack(anchor='w')
        self.combined_email_entry = ttk.Entry(input_frame, font=('Arial', 16), width=40)
        self.combined_email_entry.pack(fill='x', pady=2)
        
        # Phone input
        ttk.Label(input_frame, text="Phone Patient:", style='Input.TLabel').pack(anchor='w', pady=(10,0))
        self.combined_phone_entry = ttk.Entry(input_frame, font=('Arial', 16), width=40)
        self.combined_phone_entry.pack(fill='x', pady=2)
        
        ttk.Button(input_frame, text="🚑 EMERGENCY CPR", 
                  command=self.investigate_combined, style='Red.TButton').pack(pady=10)
        
        # Results section
        results_frame = ttk.LabelFrame(parent, text="🏥 Emergency Room Status", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.combined_results = scrolledtext.ScrolledText(results_frame, 
                                                         bg='#1a0000', 
                                                         fg='#ffffff',
                                                         font=('Courier', 14))
        self.combined_results.pack(fill='both', expand=True)
    
    def create_settings_tab(self, parent):
        """Create settings tab"""
        settings_frame = ttk.LabelFrame(parent, text="⚙️ API Configuration", padding=10)
        settings_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.settings_text = scrolledtext.ScrolledText(settings_frame, 
                                                      bg='#1a0000', 
                                                      fg='#ffffff',
                                                      font=('Courier', 14))
        self.settings_text.pack(fill='both', expand=True)
        
        ttk.Button(settings_frame, text="🔄 Refresh Status", 
                  command=self.update_settings, style='Red.TButton').pack(pady=5)
        
        self.update_settings()
    
    def investigate_phone(self):
        """Investigate phone number"""
        phone_number = self.phone_entry.get().strip()
        
        if not phone_number:
            messagebox.showwarning("Warning", "🫁 Enter a phone number to begin digital CPR")
            return
        
        self.phone_results.delete('1.0', tk.END)
        self.phone_results.insert(tk.END, "🚨 STARTING PHONE RESUSCITATION...\n\n")
        self.root.update()
        
        # Format phone number
        phone_data = format_phone_number(phone_number)
        
        # Build initial results display
        result = f"""
🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉

🫁 PATIENT ASSESSMENT RESULTS

Phone Number: {phone_data['original']}
Formatted Pulse: {phone_data['formatted']}
Clean Vitals: {phone_data['clean']}
Status: 💓 PULSE DETECTED

🔍 RUNNING API DIAGNOSTICS...

"""
        
        self.phone_results.delete('1.0', tk.END)
        self.phone_results.insert(tk.END, result)
        self.root.update()
        
        # Check APIs for real information
        result += "💉 API INVESTIGATION RESULTS:\n\n"
        
        # Check Twilio
        twilio_result = check_phone_with_twilio(phone_data['clean'])
        if twilio_result:
            result += "✅ TWILIO LOOKUP:\n"
            result += f"   Valid: {'YES' if twilio_result['valid'] else 'NO'}\n"
            result += f"   Carrier: {twilio_result['carrier']}\n"
            result += f"   Type: {twilio_result['type']}\n"
            result += f"   Country: {twilio_result['country']}\n\n"
        else:
            result += "❌ Twilio Lookup: Not configured or failed\n\n"
        
        # Check IPQS
        ipqs_result = check_ipqs_phone(phone_data['clean'])
        if ipqs_result:
            result += "✅ IPQUALITYSCORE ANALYSIS:\n"
            result += f"   Valid: {'YES' if ipqs_result['valid'] else 'NO'}\n"
            result += f"   Fraud Score: {ipqs_result['fraud_score']}/100\n"
            result += f"   Carrier: {ipqs_result['carrier']}\n"
            result += f"   Line Type: {ipqs_result['line_type']}\n"
            result += f"   Location: {ipqs_result['city']}, {ipqs_result['region']}, {ipqs_result['country']}\n\n"
        else:
            result += "❌ IPQualityScore: Not configured or failed\n\n"
        
        self.phone_results.delete('1.0', tk.END)
        self.phone_results.insert(tk.END, result)
        self.root.update()
        
        # Generate search queries
        queries = generate_phone_queries(phone_data)
        
        # Add search results if SerpAPI is available
        if config.SERPAPI_KEY:
            result += "🔍 LIVE SEARCH RESULTS:\n\n"
            
            key_queries = [
                f'"{phone_data["clean"]}"',
                f'"{phone_data["formatted"]}" address',
                f'"{phone_data["clean"]}" owner name'
            ]
            
            for query in key_queries:
                result += f"Searching: {query}\n"
                search_results = search_with_serpapi(query, config.SERPAPI_KEY)
                
                if search_results:
                    for i, result_item in enumerate(search_results, 1):
                        result += f"  {i}. {result_item['title']}\n"
                        result += f"     URL: {result_item['link']}\n"
                        result += f"     Info: {result_item['snippet'][:100]}...\n\n"
                else:
                    result += "  No results found\n\n"
                
                self.phone_results.delete('1.0', tk.END)
                self.phone_results.insert(tk.END, result)
                self.root.update()
                time.sleep(1)  # Rate limiting
        
        # Add search query suggestions
        result += "\n🚑 MANUAL SEARCH SUGGESTIONS:\n\n"
        
        for category, query_list in queries.items():
            result += f"{category}\n{'='*40}\n"
            for i, query in enumerate(query_list[:3], 1):  # Show top 3 per category
                result += f"{i}. {query}\n"
            result += "\n"
        
        # API Status
        result += f"""
⚕️ MEDICAL EQUIPMENT STATUS:

- 💓 Twilio: {'ONLINE' if config.TWILIO_ACCOUNT_SID and config.TWILIO_AUTH_TOKEN else 'OFFLINE'}
- 💓 SerpAPI: {'ONLINE' if config.SERPAPI_KEY else 'OFFLINE'}
- 💓 IPQualityScore: {'ONLINE' if config.IPQS_API_KEY else 'OFFLINE'}
- 💓 Google Search: {'ONLINE' if config.GOOGLE_API_KEY and config.GOOGLE_SEARCH_ENGINE_ID else 'OFFLINE'}

🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉

🚑 Investigation Complete! Check results above for phone information.
"""
        
        self.phone_results.delete('1.0', tk.END)
        self.phone_results.insert(tk.END, result)
    
    def investigate_email(self):
        """Investigate email address"""
        email = self.email_entry.get().strip()
        
        if not email:
            messagebox.showwarning("Warning", "🚑 Enter an email address to begin resuscitation")
            return
        
        if not validate_email(email):
            messagebox.showerror("Error", "💔 Invalid email pulse detected")
            return
        
        self.email_results.delete('1.0', tk.END)
        self.email_results.insert(tk.END, "🚨 STARTING EMAIL RESUSCITATION...\n\n")
        self.root.update()
        
        # Build initial results display
        result = f"""
🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉

🚑 EMAIL PATIENT ASSESSMENT

Email Patient: {email}
Medical Provider: {get_email_provider(email)}
Vital Signs: 💓 STABLE
Treatment Status: ⚕️ RESPONDING

🔍 RUNNING EMAIL DIAGNOSTICS...

"""
        
        self.email_results.delete('1.0', tk.END)
        self.email_results.insert(tk.END, result)
        self.root.update()
        
        # Check APIs for real information
        result += "💉 EMAIL API INVESTIGATION:\n\n"
        
        # Check Hunter.io
        hunter_result = check_email_with_hunter(email)
        if hunter_result:
            result += "✅ HUNTER.IO VERIFICATION:\n"
            result += f"   Deliverable: {'YES' if hunter_result['valid'] else 'NO'}\n"
            result += f"   Confidence Score: {hunter_result['score']}/100\n"
            result += f"   SMTP Valid: {'YES' if hunter_result['smtp_valid'] else 'NO'}\n"
            result += f"   Disposable: {'YES' if hunter_result['disposable'] else 'NO'}\n"
            result += f"   Webmail: {'YES' if hunter_result['webmail'] else 'NO'}\n\n"
        else:
            result += "❌ Hunter.io: Not configured or failed\n\n"
        
        # Check HIBP
        breach_result = check_email_breaches(email)
        if breach_result is not None:
            result += "✅ HAVE I BEEN PWNED ANALYSIS:\n"
            result += f"   Breaches Found: {breach_result['breach_count']}\n"
            if breach_result['breaches']:
                result += f"   Breach Sites: {', '.join(breach_result['breaches'])}\n"
            else:
                result += "   Status: CLEAN - No breaches found\n"
            result += "\n"
        else:
            result += "❌ Have I Been Pwned: Not configured or failed\n\n"
        
        self.email_results.delete('1.0', tk.END)
        self.email_results.insert(tk.END, result)
        self.root.update()
        
        # Generate search queries
        queries = generate_email_queries(email)
        
        # Add search results if SerpAPI is available
        if config.SERPAPI_KEY:
            result += "🔍 LIVE EMAIL SEARCH RESULTS:\n\n"
            
            key_queries = [
                f'"{email}"',
                f'"{email}" profile',
                f'"{email}" social media'
            ]
            
            for query in key_queries:
                result += f"Searching: {query}\n"
                search_results = search_with_serpapi(query, config.SERPAPI_KEY)
                
                if search_results:
                    for i, result_item in enumerate(search_results, 1):
                        result += f"  {i}. {result_item['title']}\n"
                        result += f"     URL: {result_item['link']}\n"
                        result += f"     Info: {result_item['snippet'][:100]}...\n\n"
                else:
                    result += "  No results found\n\n"
                
                self.email_results.delete('1.0', tk.END)
                self.email_results.insert(tk.END, result)
                self.root.update()
                time.sleep(1)  # Rate limiting
        
        # Add search query suggestions
        result += "\n⚡ MANUAL SEARCH SUGGESTIONS:\n\n"
        
        for category, query_list in queries.items():
            result += f"{category}\n{'='*40}\n"
            for i, query in enumerate(query_list[:3], 1):  # Show top 3 per category
                result += f"{i}. {query}\n"
            result += "\n"
        
        # API Status
        result += f"""
🚑 EMERGENCY EQUIPMENT STATUS:

- 💓 Hunter.io: {'OPERATIONAL' if config.HUNTER_API_KEY else 'FLATLINED'}
- 💓 Have I Been Pwned: {'OPERATIONAL' if config.HIBP_API_KEY else 'FLATLINED'}
- 💓 SerpAPI: {'OPERATIONAL' if config.SERPAPI_KEY else 'FLATLINED'}
- 💓 Google Search: {'OPERATIONAL' if config.GOOGLE_API_KEY and config.GOOGLE_SEARCH_ENGINE_ID else 'FLATLINED'}

🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉

⚕️ Email Investigation Complete! Check results above for detailed information.
"""
        
        self.email_results.delete('1.0', tk.END)
        self.email_results.insert(tk.END, result)
    
    def investigate_combined(self):
        """Investigate both email and phone"""
        email = self.combined_email_entry.get().strip()
        phone = self.combined_phone_entry.get().strip()
        
        if not email or not phone:
            messagebox.showwarning("Warning", "🚨 Need both patients for emergency treatment")
            return
        
        if not validate_email(email):
            messagebox.showerror("Error", "💔 Email patient has no pulse")
            return
        
        self.combined_results.delete('1.0', tk.END)
        self.combined_results.insert(tk.END, "🚨 STARTING EMERGENCY RESUSCITATION...\n\n")
        self.root.update()
        
        # Format phone and generate queries
        phone_data = format_phone_number(phone)
        email_queries = generate_email_queries(email)
        phone_queries = generate_phone_queries(phone_data)
        
        # Combined queries
        combined_queries = [
            f'"{email}" "{phone_data["clean"]}"',
            f'"{email}" "{phone_data["formatted"]}" profile',
            f'"{email}" "{phone_data["clean"]}" contact',
            f'"{email}" "{phone_data["clean"]}" business',
            f'"{email}" "{phone_data["clean"]}" registration'
        ]
        
        # Build results display
        result = f"""
🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉

🚨 EMERGENCY ROOM STATUS REPORT

Email Patient: {email} (Provider: {get_email_provider(email)})
Phone Patient: {phone_data['formatted']} (Vitals: {phone_data['clean']})
Treatment: 🚑 DUAL RESUSCITATION IN PROGRESS

🫁 SYNCHRONIZED CPR PROTOCOL

"""
        
        for i, query in enumerate(combined_queries, 1):
            result += f"{i}. {query}\n"
        
        result += f"""

⚕️ EMAIL TREATMENTS ({sum(len(queries) for queries in email_queries.values())} total)

"""
        for category in list(email_queries.keys())[:3]:
            result += f"**{category}:** {len(email_queries[category])} procedures\n"
        
        result += f"""

🫁 PHONE CPR CYCLES ({sum(len(queries) for queries in phone_queries.values())} total)

"""
        for category in list(phone_queries.keys())[:3]:
            result += f"**{category}:** {len(phone_queries[category])} compressions\n"
        
        total_queries = (
            len(combined_queries) + 
            sum(len(queries) for queries in email_queries.values()) + 
            sum(len(queries) for queries in phone_queries.values())
        )
        
        result += f"""

🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉

🚨 Performed {total_queries} emergency procedures!

Note: Use individual treatment screens for complete protocols.
"""
        
        self.combined_results.insert(tk.END, result)
    
    def update_settings(self):
        """Update settings display"""
        self.settings_text.delete('1.0', tk.END)
        
        apis = [
            ("💀 Phone Validation", [
                ("Twilio", bool(config.TWILIO_ACCOUNT_SID and config.TWILIO_AUTH_TOKEN)),
                ("IPQualityScore", bool(config.IPQS_API_KEY)),
            ]),
            ("🔴 Email Investigation", [
                ("Hunter.io", bool(config.HUNTER_API_KEY)),
                ("Have I Been Pwned", bool(config.HIBP_API_KEY)),
            ]),
            ("⚔️ Search Engines", [
                ("SerpAPI", bool(config.SERPAPI_KEY)),
                ("Google Custom Search", bool(config.GOOGLE_API_KEY and config.GOOGLE_SEARCH_ENGINE_ID)),
            ])
        ]
        
        content = f"""
🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉

🏴‍☠️ API CONFIGURATION STATUS

"""
        
        total_configured = 0
        total_apis = 0
        
        for category, services in apis:
            content += f"\n{category}\n{'='*50}\n"
            for service, configured in services:
                icon = "🔴" if configured else "💀"
                content += f"- {icon} {service}: {'ACTIVE' if configured else 'INACTIVE'}\n"
                if configured:
                    total_configured += 1
                total_apis += 1
        
        content += f"""

SUMMARY
{'='*50}

Active APIs: {total_configured}/{total_apis}
Status: {'🔴 OPERATIONAL' if total_configured > 0 else '💀 OFFLINE'}

⚔️ SETUP INSTRUCTIONS
{'='*50}

To configure APIs, set these environment variables:

# Essential APIs (Free tiers available)
export SERPAPI_KEY="your_serpapi_key"
export IPQS_API_KEY="your_ipqs_key" 
export HUNTER_API_KEY="your_hunter_key"

# Advanced APIs
export TWILIO_ACCOUNT_SID="your_sid"
export TWILIO_AUTH_TOKEN="your_token"
export HIBP_API_KEY="your_hibp_key"

Add these to your ~/.bashrc or ~/.zshrc file for persistence.

🗃️ SIGN-UP LINKS
{'='*50}

- SerpAPI: https://serpapi.com/ (100 searches/month free)
- IPQualityScore: https://www.ipqualityscore.com/ (5000 requests/month free)
- Hunter.io: https://hunter.io/ (100 requests/month free)
- Twilio: https://www.twilio.com/ (Paid, very accurate)
- Have I Been Pwned: https://haveibeenpwned.com/API/v3 ($3.50/month)

🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉
"""
        
        self.settings_text.insert(tk.END, content)
    
    def create_api_config_tab(self, parent):
        """Create API configuration tab with input fields"""
        main_frame = ttk.Frame(parent, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔑 API Key Configuration", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # API Key Input Fields
        self.api_entries = {}
        
        # SerpAPI
        serp_frame = ttk.LabelFrame(scrollable_frame, text="🔍 SerpAPI (Search Engine) - FREE", padding=10)
        serp_frame.pack(fill='x', pady=5)
        ttk.Label(serp_frame, text="100 searches/month free - Sign up at https://serpapi.com/").pack(anchor='w')
        self.api_entries['SERPAPI_KEY'] = ttk.Entry(serp_frame, width=50, show='*', font=('Arial', 12))
        self.api_entries['SERPAPI_KEY'].pack(fill='x', pady=2)
        
        # IPQualityScore
        ipqs_frame = ttk.LabelFrame(scrollable_frame, text="📱 IPQualityScore (Phone Validation) - FREE", padding=10)
        ipqs_frame.pack(fill='x', pady=5)
        ttk.Label(ipqs_frame, text="5000 requests/month free - Sign up at https://www.ipqualityscore.com/").pack(anchor='w')
        self.api_entries['IPQS_API_KEY'] = ttk.Entry(ipqs_frame, width=50, show='*', font=('Arial', 12))
        self.api_entries['IPQS_API_KEY'].pack(fill='x', pady=2)
        
        # Hunter.io
        hunter_frame = ttk.LabelFrame(scrollable_frame, text="📧 Hunter.io (Email Verification) - FREE", padding=10)
        hunter_frame.pack(fill='x', pady=5)
        ttk.Label(hunter_frame, text="100 email checks/month free - Sign up at https://hunter.io/").pack(anchor='w')
        self.api_entries['HUNTER_API_KEY'] = ttk.Entry(hunter_frame, width=50, show='*', font=('Arial', 12))
        self.api_entries['HUNTER_API_KEY'].pack(fill='x', pady=2)
        
        # HIBP
        hibp_frame = ttk.LabelFrame(scrollable_frame, text="🔐 Have I Been Pwned (Data Breaches) - PAID", padding=10)
        hibp_frame.pack(fill='x', pady=5)
        ttk.Label(hibp_frame, text="$3.50/month - Subscribe at https://haveibeenpwned.com/API/v3").pack(anchor='w')
        self.api_entries['HIBP_API_KEY'] = ttk.Entry(hibp_frame, width=50, show='*', font=('Arial', 12))
        self.api_entries['HIBP_API_KEY'].pack(fill='x', pady=2)
        
        # Twilio
        twilio_frame = ttk.LabelFrame(scrollable_frame, text="📞 Twilio (Advanced Phone Lookup) - PAID", padding=10)
        twilio_frame.pack(fill='x', pady=5)
        ttk.Label(twilio_frame, text="Very accurate but paid - Sign up at https://www.twilio.com/").pack(anchor='w')
        ttk.Label(twilio_frame, text="Account SID:").pack(anchor='w')
        self.api_entries['TWILIO_ACCOUNT_SID'] = ttk.Entry(twilio_frame, width=50, show='*', font=('Arial', 12))
        self.api_entries['TWILIO_ACCOUNT_SID'].pack(fill='x', pady=2)
        ttk.Label(twilio_frame, text="Auth Token:").pack(anchor='w')
        self.api_entries['TWILIO_AUTH_TOKEN'] = ttk.Entry(twilio_frame, width=50, show='*', font=('Arial', 12))
        self.api_entries['TWILIO_AUTH_TOKEN'].pack(fill='x', pady=2)
        
        # Google Custom Search
        google_frame = ttk.LabelFrame(scrollable_frame, text="🔍 Google Custom Search - FREE", padding=10)
        google_frame.pack(fill='x', pady=5)
        ttk.Label(google_frame, text="100 searches/day free - Setup at https://developers.google.com/custom-search/").pack(anchor='w')
        ttk.Label(google_frame, text="API Key:").pack(anchor='w')
        self.api_entries['GOOGLE_API_KEY'] = ttk.Entry(google_frame, width=50, show='*', font=('Arial', 12))
        self.api_entries['GOOGLE_API_KEY'].pack(fill='x', pady=2)
        ttk.Label(google_frame, text="Search Engine ID:").pack(anchor='w')
        self.api_entries['GOOGLE_SEARCH_ENGINE_ID'] = ttk.Entry(google_frame, width=50, show='*', font=('Arial', 12))
        self.api_entries['GOOGLE_SEARCH_ENGINE_ID'].pack(fill='x', pady=2)
        
        # Load current values
        self.load_current_api_keys()
        
        # Buttons frame
        buttons_frame = ttk.Frame(scrollable_frame, padding=10)
        buttons_frame.pack(fill='x', pady=20)
        
        # Seek the Warm Embrace button
        embrace_btn = ttk.Button(buttons_frame, 
                                text="🤗 Seek the Warm Embrace",
                                command=self.seek_warm_embrace,
                                style='Red.TButton')
        embrace_btn.pack(side='left', padx=(0, 10))
        
        # Save button
        save_btn = ttk.Button(buttons_frame,
                             text="💾 Save API Keys",
                             command=self.save_api_keys,
                             style='Red.TButton')
        save_btn.pack(side='left', padx=(0, 10))
        
        # Test button
        test_btn = ttk.Button(buttons_frame,
                             text="✅ Test APIs",
                             command=self.test_apis,
                             style='Red.TButton')
        test_btn.pack(side='left')
        
        # Pack the scrollable area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def load_current_api_keys(self):
        """Load current API keys from environment variables"""
        import os
        env_vars = {
            'SERPAPI_KEY': os.getenv('SERPAPI_KEY', ''),
            'IPQS_API_KEY': os.getenv('IPQS_API_KEY', ''),
            'HUNTER_API_KEY': os.getenv('HUNTER_API_KEY', ''),
            'HIBP_API_KEY': os.getenv('HIBP_API_KEY', ''),
            'TWILIO_ACCOUNT_SID': os.getenv('TWILIO_ACCOUNT_SID', ''),
            'TWILIO_AUTH_TOKEN': os.getenv('TWILIO_AUTH_TOKEN', ''),
            'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY', ''),
            'GOOGLE_SEARCH_ENGINE_ID': os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')
        }
        
        for key, value in env_vars.items():
            if key in self.api_entries and value:
                self.api_entries[key].insert(0, value)
    
    def seek_warm_embrace(self):
        """Open all API signup sites - The Warm Embrace"""
        if open_api_sites():
            messagebox.showinfo(
                "Warm Embrace", 
                "🤗 The warm embrace of API knowledge awaits you!\n\n"
                "All signup sites have been opened in your browser.\n"
                "Sign up for the free accounts and return here to enter your keys."
            )
        else:
            messagebox.showerror(
                "Error", 
                "Could not open browser. Please manually visit:\n\n"
                "- https://serpapi.com/\n"
                "- https://www.ipqualityscore.com/\n"
                "- https://hunter.io/\n"
                "- https://haveibeenpwned.com/API/v3"
            )
    
    def save_api_keys(self):
        """Save API keys to environment variables and config file"""
        import os
        
        # Update environment variables
        for key, entry in self.api_entries.items():
            value = entry.get().strip()
            if value:
                os.environ[key] = value
        
        # Update config object
        config.SERPAPI_KEY = os.getenv('SERPAPI_KEY', '')
        config.IPQS_API_KEY = os.getenv('IPQS_API_KEY', '')
        config.HUNTER_API_KEY = os.getenv('HUNTER_API_KEY', '')
        config.HIBP_API_KEY = os.getenv('HIBP_API_KEY', '')
        config.TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
        config.TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
        config.GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
        config.GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')
        
        # Save to shell config file for persistence
        shell_config = os.path.expanduser('~/.zshrc')
        
        try:
            with open(shell_config, 'r') as f:
                content = f.read()
            
            # Add export statements for non-empty keys
            exports = []
            for key, entry in self.api_entries.items():
                value = entry.get().strip()
                if value:
                    export_line = f'export {key}="{value}"'
                    if export_line not in content:
                        exports.append(export_line)
            
            if exports:
                with open(shell_config, 'a') as f:
                    f.write('\n# Purity Quest API Keys\n')
                    f.write('\n'.join(exports) + '\n')
            
            messagebox.showinfo(
                "Success", 
                f"✅ API keys saved!\n\n"
                f"Saved {len([e for e in self.api_entries.values() if e.get().strip()])} keys.\n"
                "Keys are now active for this session and saved to ~/.zshrc for future sessions."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save API keys: {e}")
    
    def test_apis(self):
        """Test API connectivity"""
        # Update config with current values first
        for key, entry in self.api_entries.items():
            value = entry.get().strip()
            if value:
                os.environ[key] = value
                setattr(config, key, value)
        
        results = []
        
        # Test SerpAPI
        if config.SERPAPI_KEY:
            test_result = search_with_serpapi('test query', config.SERPAPI_KEY)
            results.append(f"🔍 SerpAPI: {'✅ Working' if test_result is not None else '❌ Failed'}")
        else:
            results.append("🔍 SerpAPI: ❌ No key provided")
        
        # Test IPQS
        if config.IPQS_API_KEY:
            test_result = check_ipqs_phone('5551234567')
            results.append(f"📱 IPQualityScore: {'✅ Working' if test_result is not None else '❌ Failed'}")
        else:
            results.append("📱 IPQualityScore: ❌ No key provided")
        
        # Test Hunter.io
        if config.HUNTER_API_KEY:
            test_result = check_email_with_hunter('test@example.com')
            results.append(f"📧 Hunter.io: {'✅ Working' if test_result is not None else '❌ Failed'}")
        else:
            results.append("📧 Hunter.io: ❌ No key provided")
        
        # Test HIBP
        if config.HIBP_API_KEY:
            test_result = check_email_breaches('test@example.com')
            results.append(f"🔐 Have I Been Pwned: {'✅ Working' if test_result is not None else '❌ Failed'}")
        else:
            results.append("🔐 Have I Been Pwned: ❌ No key provided")
        
        # Test Twilio
        if config.TWILIO_ACCOUNT_SID and config.TWILIO_AUTH_TOKEN:
            test_result = check_phone_with_twilio('5551234567')
            results.append(f"📞 Twilio: {'✅ Working' if test_result is not None else '❌ Failed'}")
        else:
            results.append("📞 Twilio: ❌ No credentials provided")
        
        messagebox.showinfo("API Test Results", "\n".join(results))
    
    def update_settings(self):
        """Update settings display"""
        self.settings_text.delete('1.0', tk.END)
        
        apis = [
            ("💀 Phone Validation", [
                ("Twilio", bool(config.TWILIO_ACCOUNT_SID and config.TWILIO_AUTH_TOKEN)),
                ("IPQualityScore", bool(config.IPQS_API_KEY)),
            ]),
            ("🔴 Email Investigation", [
                ("Hunter.io", bool(config.HUNTER_API_KEY)),
                ("Have I Been Pwned", bool(config.HIBP_API_KEY)),
            ]),
            ("⚔️ Search Engines", [
                ("SerpAPI", bool(config.SERPAPI_KEY)),
                ("Google Custom Search", bool(config.GOOGLE_API_KEY and config.GOOGLE_SEARCH_ENGINE_ID)),
            ])
        ]
        
        content = f"""
🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉

🏴‍☠️ API CONFIGURATION STATUS

"""
        
        total_configured = 0
        total_apis = 0
        
        for category, services in apis:
            content += f"\n{category}\n{'='*50}\n"
            for service, configured in services:
                icon = "🔴" if configured else "💀"
                content += f"- {icon} {service}: {'ACTIVE' if configured else 'INACTIVE'}\n"
                if configured:
                    total_configured += 1
                total_apis += 1
        
        content += f"""

SUMMARY
{'='*50}

Active APIs: {total_configured}/{total_apis}
Status: {'🔴 OPERATIONAL' if total_configured > 0 else '💀 OFFLINE'}

⚔️ SETUP INSTRUCTIONS
{'='*50}

To configure APIs, set these environment variables:

# Essential APIs (Free tiers available)
export SERPAPI_KEY="your_serpapi_key"
export IPQS_API_KEY="your_ipqs_key" 
export HUNTER_API_KEY="your_hunter_key"

# Advanced APIs
export TWILIO_ACCOUNT_SID="your_sid"
export TWILIO_AUTH_TOKEN="your_token"
export HIBP_API_KEY="your_hibp_key"

Add these to your ~/.bashrc or ~/.zshrc file for persistence.

🗃️ SIGN-UP LINKS
{'='*50}

- SerpAPI: https://serpapi.com/ (100 searches/month free)
- IPQualityScore: https://www.ipqualityscore.com/ (5000 requests/month free)
- Hunter.io: https://hunter.io/ (100 requests/month free)
- Twilio: https://www.twilio.com/ (Paid, very accurate)
- Have I Been Pwned: https://haveibeenpwned.com/API/v3 ($3.50/month)

🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉🫀💉
"""
        
        self.settings_text.insert(tk.END, content)

def main():
    print("🫁 Starting PURITY IS KEY GUI...")
    try:
        root = tk.Tk()
        print("✅ GUI window created")
        app = PurityQuestGUI(root)
        print("✅ GUI initialized - Window should be visible now!")
        root.mainloop()
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
