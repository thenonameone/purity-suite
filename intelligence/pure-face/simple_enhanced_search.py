#!/usr/bin/env python3
"""
Simplified Enhanced Face Search Tool
Extracts actual public information from reverse image searches
"""

import sys
import os
import requests
import json
import time
import re
import asyncio
from urllib.parse import urlencode, quote, urlparse
from PIL import Image
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import tempfile
import base64

class SimplifiedFaceSearch:
    def __init__(self, image_path):
        self.image_path = image_path
        self.results = {}
        self.extracted_info = {
            'names': set(),
            'social_profiles': [],
            'public_records': [],
            'websites': [],
            'locations': set(),
            'occupations': set(),
            'contact_info': [],
            'additional_info': []
        }
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random
        })
        
    def search_and_extract_all(self):
        """Main function to search all platforms and extract results"""
        print(f"🔍 Starting enhanced face search with result extraction...")
        print(f"📷 Analyzing image: {self.image_path}")
        print("=" * 80)
        
        # Analyze image properties
        self.analyze_image_properties()
        
        # Google Images search with requests
        self.search_google_images_requests()
        
        # Yandex Images search
        self.search_yandex_images_requests()
        
        # TinEye search
        self.search_tineye_requests()
        
        # Generate comprehensive report
        self.generate_enhanced_report()
    
    def analyze_image_properties(self):
        """Analyze basic image properties"""
        print("📸 Analyzing image properties...")
        
        try:
            with Image.open(self.image_path) as img:
                width, height = img.size
                format_type = img.format
                mode = img.mode
                
                print(f"✅ Image analyzed: {width}x{height}, {format_type}, {mode}")
                
                self.image_info = {
                    'width': width,
                    'height': height,
                    'format': format_type,
                    'mode': mode,
                    'file_size': os.path.getsize(self.image_path)
                }
                
        except Exception as e:
            print(f"⚠️ Image analysis error: {e}")
            self.image_info = None
    
    def search_google_images_requests(self):
        """Search Google Images using requests"""
        print("🔍 Searching Google Images with automated upload...")
        
        try:
            # Upload image to Google Images
            upload_url = "https://images.google.com/searchbyimage/upload"
            
            with open(self.image_path, 'rb') as img_file:
                files = {'encoded_image': img_file}
                
                response = self.session.post(upload_url, files=files, timeout=30, allow_redirects=True)
                
                if response.status_code == 200:
                    search_url = response.url
                    print(f"✅ Google search successful: {len(response.text)} bytes received")
                    
                    # Extract information from the response
                    google_results = self.extract_google_info(response.text, search_url)
                    self.results['Google Images'] = google_results
                    
                    # Extract names and other info
                    self.extract_info_from_html(response.text, 'Google Images')
                    
                else:
                    print(f"⚠️ Google search failed: Status {response.status_code}")
                    self.results['Google Images'] = {'error': f'HTTP {response.status_code}'}
                    
        except Exception as e:
            print(f"⚠️ Google Images error: {e}")
            self.results['Google Images'] = {'error': str(e)}
    
    def extract_google_info(self, html, search_url):
        """Extract information from Google Images HTML response"""
        info = {
            'search_url': search_url,
            'pages_found': [],
            'similar_images': [],
            'extracted_text': []
        }
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract page titles and links
            links = soup.find_all('a', href=True)
            for link in links[:20]:  # Limit to first 20 links
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                if href.startswith('http') and text:
                    info['pages_found'].append({
                        'url': href,
                        'title': text[:100],  # Limit title length
                        'source': 'Google Images'
                    })
                    
                    # Try to extract names from link text
                    names = self.extract_names_from_text(text)
                    self.extracted_info['names'].update(names)
            
            # Extract any visible text that might contain information
            text_content = soup.get_text()
            self.extract_info_from_text(text_content)
            
            print(f"✅ Google: Extracted {len(info['pages_found'])} page references")
            
        except Exception as e:
            print(f"⚠️ Google extraction error: {e}")
            info['error'] = str(e)
        
        return info
    
    def search_yandex_images_requests(self):
        """Search Yandex Images using requests"""
        print("🔍 Searching Yandex Images...")
        
        try:
            upload_url = "https://yandex.com/images/search"
            
            with open(self.image_path, 'rb') as img_file:
                files = {'upfile': img_file}
                data = {'rpt': 'imageview'}
                
                response = self.session.post(upload_url, files=files, data=data, timeout=30, allow_redirects=True)
                
                if response.status_code == 200:
                    print(f"✅ Yandex search successful: {len(response.text)} bytes received")
                    
                    yandex_results = self.extract_yandex_info(response.text, response.url)
                    self.results['Yandex Images'] = yandex_results
                    
                    # Extract information
                    self.extract_info_from_html(response.text, 'Yandex Images')
                    
                else:
                    print(f"⚠️ Yandex search failed: Status {response.status_code}")
                    
        except Exception as e:
            print(f"⚠️ Yandex error: {e}")
            self.results['Yandex Images'] = {'error': str(e)}
    
    def extract_yandex_info(self, html, search_url):
        """Extract information from Yandex response"""
        info = {
            'search_url': search_url,
            'pages_found': [],
            'extracted_info': []
        }
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract links and information
            links = soup.find_all('a', href=True)
            for link in links[:15]:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                if text and len(text) > 10:
                    info['pages_found'].append({
                        'url': href,
                        'title': text[:100],
                        'source': 'Yandex Images'
                    })
                    
                    # Extract names
                    names = self.extract_names_from_text(text)
                    self.extracted_info['names'].update(names)
            
            print(f"✅ Yandex: Extracted {len(info['pages_found'])} references")
            
        except Exception as e:
            print(f"⚠️ Yandex extraction error: {e}")
            info['error'] = str(e)
        
        return info
    
    def search_tineye_requests(self):
        """Try TinEye search"""
        print("🔍 Attempting TinEye search...")
        
        try:
            # TinEye public API requires registration, so we'll simulate
            self.results['TinEye'] = {
                'status': 'api_required',
                'note': 'TinEye requires API key for automated searches',
                'manual_url': 'https://tineye.com/'
            }
            print("⚠️ TinEye: API key required for automated search")
            
        except Exception as e:
            print(f"⚠️ TinEye error: {e}")
    
    def extract_names_from_text(self, text):
        """Extract potential names from text using patterns"""
        names = set()
        
        if not text:
            return names
        
        # More comprehensive name patterns
        name_patterns = [
            r'\b[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}\b',  # First Last (min 3 chars each)
            r'\b[A-Z][a-z]{2,}\s+[A-Z]\.\s+[A-Z][a-z]{2,}\b',  # First M. Last
            r'\b[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}\b',  # First Middle Last
            r'\b[A-Z][a-z]{2,},\s+[A-Z][a-z]{2,}\b',  # Last, First
        ]
        
        for pattern in name_patterns:
            try:
                matches = re.findall(pattern, text)
                names.update(matches)
            except:
                continue
        
        # Filter out common false positives
        false_positives = {
            'New York', 'Los Angeles', 'United States', 'Google Inc', 'Facebook Inc',
            'Privacy Policy', 'Terms Service', 'About Us', 'Contact Us', 'Sign In',
            'Learn More', 'Read More', 'Click Here', 'Find Out', 'Get Started'
        }
        names = names - false_positives
        
        # Filter by length and basic validation
        valid_names = set()
        for name in names:
            if len(name) >= 6 and len(name) <= 50:  # Reasonable name length
                parts = name.split()
                if len(parts) >= 2 and all(len(part) >= 2 for part in parts):
                    valid_names.add(name)
        
        return valid_names
    
    def extract_info_from_text(self, text):
        """Extract various types of information from text"""
        if not text:
            return
        
        # Extract email addresses
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        self.extracted_info['contact_info'].extend(emails)
        
        # Extract phone numbers
        phone_patterns = [
            r'\b\d{3}-\d{3}-\d{4}\b',  # 123-456-7890
            r'\b\(\d{3}\)\s*\d{3}-\d{4}\b',  # (123) 456-7890
            r'\b\d{3}\.\d{3}\.\d{4}\b',  # 123.456.7890
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            self.extracted_info['contact_info'].extend(phones)
        
        # Extract social media usernames/handles
        social_patterns = [
            r'@[A-Za-z0-9_]{3,}',  # @username
            r'facebook\.com/[A-Za-z0-9._-]+',
            r'twitter\.com/[A-Za-z0-9._-]+',
            r'instagram\.com/[A-Za-z0-9._-]+',
            r'linkedin\.com/in/[A-Za-z0-9._-]+',
        ]
        
        for pattern in social_patterns:
            matches = re.findall(pattern, text)
            self.extracted_info['social_profiles'].extend(matches)
        
        # Extract locations (basic city, state patterns)
        location_pattern = r'\b[A-Z][a-z]+,\s*[A-Z]{2}\b'  # City, ST
        locations = re.findall(location_pattern, text)
        self.extracted_info['locations'].update(locations)
    
    def extract_info_from_html(self, html, source):
        """Extract structured information from HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract all text content
            text_content = soup.get_text()
            self.extract_info_from_text(text_content)
            
            # Extract meta information
            title = soup.find('title')
            if title:
                title_text = title.get_text()
                names = self.extract_names_from_text(title_text)
                self.extracted_info['names'].update(names)
            
            # Extract specific social media links
            social_links = soup.find_all('a', href=True)
            for link in social_links:
                href = link.get('href', '')
                if any(social in href.lower() for social in ['facebook', 'twitter', 'instagram', 'linkedin', 'tiktok']):
                    self.extracted_info['social_profiles'].append({
                        'url': href,
                        'source': source,
                        'text': link.get_text(strip=True)[:50]
                    })
            
        except Exception as e:
            print(f"⚠️ HTML extraction error for {source}: {e}")
    
    def generate_enhanced_report(self):
        """Generate comprehensive report with extracted information"""
        print("\n" + "=" * 80)
        print("🎯 ENHANCED FACE SEARCH RESULTS - EXTRACTED PUBLIC INFORMATION")
        print("=" * 80)
        print(f"📷 Image analyzed: {self.image_path}")
        print(f"🕐 Search completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Image Properties
        if self.image_info:
            print("📸 IMAGE PROPERTIES:")
            info = self.image_info
            print(f"   📐 Dimensions: {info['width']}x{info['height']} pixels")
            print(f"   📁 Format: {info['format']}")
            print(f"   💾 File size: {info['file_size']:,} bytes")
            print()
        
        # Names Found
        if self.extracted_info['names']:
            print("📝 NAMES DISCOVERED:")
            for name in sorted(self.extracted_info['names']):
                print(f"   • {name}")
            print()
        else:
            print("📝 NAMES: No names automatically detected from search results")
            print()
        
        # Contact Information
        unique_contacts = list(set(self.extracted_info['contact_info']))
        if unique_contacts:
            print(\"📞 CONTACT INFORMATION FOUND:\")
            for contact in unique_contacts:
                if '@' in contact:
                    print(f\"   📧 Email: {contact}\")
                else:
                    print(f\"   📱 Phone: {contact}\")
            print()
        
        # Social Media Profiles
        if self.extracted_info['social_profiles']:
            print(\"📱 SOCIAL MEDIA REFERENCES:\")
            seen = set()
            for profile in self.extracted_info['social_profiles']:
                if isinstance(profile, dict):
                    url = profile.get('url', '')
                    if url not in seen:
                        print(f\"   • {profile.get('text', 'Link')}: {url}\")
                        seen.add(url)
                else:
                    if profile not in seen:
                        print(f\"   • {profile}\")
                        seen.add(profile)
            print()
        
        # Locations
        if self.extracted_info['locations']:
            print(\"📍 LOCATIONS MENTIONED:\")
            for location in sorted(self.extracted_info['locations']):
                print(f\"   • {location}\")
            print()
        
        # Search Results Summary
        print(\"📊 SEARCH RESULTS SUMMARY:\")
        for engine, results in self.results.items():
            if isinstance(results, dict):
                if 'error' in results:
                    print(f\"   ❌ {engine}: Error - {results['error']}\")
                elif 'pages_found' in results:
                    print(f\"   ✅ {engine}: {len(results['pages_found'])} pages analyzed\")
                else:
                    print(f\"   ⚠️ {engine}: Search attempted\")
        
        print(f\"   📝 Total unique names: {len(self.extracted_info['names'])}\")
        print(f\"   📞 Contact details: {len(set(self.extracted_info['contact_info']))}\")
        print(f\"   📱 Social references: {len(self.extracted_info['social_profiles'])}\")
        print(f\"   📍 Locations: {len(self.extracted_info['locations'])}\")
        print()
        
        # Detailed Results
        if any(self.extracted_info['names']):
            print(\"💡 DETAILED FINDINGS:\")
            if self.extracted_info['names']:
                print(\"   🔍 Recommended next steps:\")
                for name in sorted(list(self.extracted_info['names'])[:3]):
                    print(f\"     • Search '{name}' on social media platforms\")
                    print(f\"     • Look up '{name}' in people search engines\")
                    print(f\"     • Cross-reference '{name}' with location data\")
        else:
            print(\"💡 NO AUTOMATIC MATCHES FOUND:\")
            print(\"   • The image may be private or not widely published online\")
            print(\"   • Try specialized face recognition services like PimEyes\")
            print(\"   • Consider manual reverse image search on multiple platforms\")
            print(\"   • The person may not have a significant online presence\")
        
        print()
        print(\"🌐 MANUAL SEARCH RECOMMENDATIONS:\")
        print(\"   • Upload to https://pimeyes.com for face recognition\")
        print(\"   • Try https://images.google.com with manual upload\")
        print(\"   • Search https://yandex.com/images (often finds different results)\")
        print(\"   • Use https://tineye.com for reverse image search\")
        print(\"   • Check social media platforms individually\")
        print()
        
        # Save results
        self.save_results_to_file()
    
    def save_results_to_file(self):
        \"\"\"Save results to a JSON file\"\"\"
        output_file = f\"face_search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json\"
        
        # Convert sets to lists for JSON serialization
        json_data = {}
        for key, value in self.extracted_info.items():
            if isinstance(value, set):
                json_data[key] = list(value)
            else:
                json_data[key] = value
        
        json_data['search_results'] = self.results
        json_data['timestamp'] = datetime.now().isoformat()
        json_data['image_path'] = self.image_path
        json_data['image_info'] = self.image_info
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            print(f\"💾 Detailed results saved to: {output_file}\")
        except Exception as e:
            print(f\"⚠️ Could not save results file: {e}\")

def main():
    if len(sys.argv) != 2:
        print(\"Usage: python3 simple_enhanced_search.py <image_path>\")
        print(\"Example: python3 simple_enhanced_search.py /home/xx/Desktop/rey.jpeg\")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f\"Error: Image file '{image_path}' not found.\")
        sys.exit(1)
    
    # Verify it's an image
    try:
        with Image.open(image_path) as img:
            print(f\"📷 Image loaded: {img.size[0]}x{img.size[1]} pixels, format: {img.format}\")
    except Exception as e:
        print(f\"Error: Could not load image - {e}\")
        sys.exit(1)
    
    # Start enhanced search
    search_engine = SimplifiedFaceSearch(image_path)
    search_engine.search_and_extract_all()

if __name__ == \"__main__\":
    main()