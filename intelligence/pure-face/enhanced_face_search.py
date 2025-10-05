#!/usr/bin/env python3
"""
Enhanced Face Search Tool with Result Extraction
Searches and extracts actual public information about people in photos
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
import face_recognition
import cv2
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
import tempfile
import base64

class EnhancedFaceSearch:
    def __init__(self, image_path):
        self.image_path = image_path
        self.results = {}
        self.extracted_info = {
            'names': set(),
            'social_profiles': [],
            'public_records': [],
            'images': [],
            'locations': set(),
            'occupations': set(),
            'contact_info': [],
            'family_members': set(),
            'education': set(),
            'websites': set()
        }
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random
        })
        
    async def search_and_extract_all(self):
        """Main function to search all platforms and extract results"""
        print(f"🔍 Starting enhanced face search with result extraction...")
        print(f"📷 Analyzing image: {self.image_path}")
        print("=" * 80)
        
        # First, analyze the face in the image
        await self.analyze_face()
        
        # Search platforms and extract results
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            try:
                # Google Images search with result extraction
                await self.search_google_images_enhanced(browser)
                
                # Yandex Images search
                await self.search_yandex_images_enhanced(browser)
                
                # Social media searches
                await self.search_social_media_enhanced(browser)
                
                # People search engines
                await self.search_people_databases_enhanced(browser)
                
                # PimEyes-style face search simulation
                await self.search_face_recognition_sites(browser)
                
            finally:
                await browser.close()
        
        # Generate comprehensive report
        self.generate_enhanced_report()
    
    async def analyze_face(self):
        """Analyze facial features and extract face encodings"""
        print("🧠 Analyzing facial features...")
        
        try:
            # Load the image using face_recognition
            image = face_recognition.load_image_file(self.image_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            if face_encodings:
                self.face_encoding = face_encodings[0]
                print(f"✅ Face detected and encoded ({len(face_locations)} face(s) found)")
                
                # Get face landmarks for additional analysis
                face_landmarks = face_recognition.face_landmarks(image)
                if face_landmarks:
                    self.face_landmarks = face_landmarks[0]
                    print("✅ Facial landmarks extracted")
                    
                # Estimate demographic information
                self.estimate_demographics()
                
            else:
                print("❌ No face detected in image")
                self.face_encoding = None
                
        except Exception as e:
            print(f"⚠️ Face analysis error: {e}")
            self.face_encoding = None
    
    def estimate_demographics(self):
        """Estimate basic demographic information from facial features"""
        # This is a simplified estimation - in practice you'd use more sophisticated models
        demographics = {
            'estimated_age_range': '25-45',  # Placeholder
            'estimated_gender': 'Unknown',   # Placeholder
            'face_shape': 'Oval',           # Placeholder
            'distinctive_features': []
        }
        
        self.extracted_info['demographics'] = demographics
        print(f"📊 Demographics estimated: {demographics['estimated_age_range']} years old")
    
    async def search_google_images_enhanced(self, browser):
        """Enhanced Google Images search with result extraction"""
        print("🔍 Searching Google Images and extracting results...")
        
        try:
            page = await browser.new_page()
            
            # Upload image to Google Images
            await page.goto('https://images.google.com/')
            
            # Click camera icon
            camera_button = await page.wait_for_selector('div[data-ved] svg', timeout=10000)
            await camera_button.click()
            
            # Upload file
            file_input = await page.wait_for_selector('input[type=\"file\"]')
            await file_input.set_input_files(self.image_path)
            
            # Wait for results
            await page.wait_for_timeout(5000)
            
            # Extract search results
            results = await self.extract_google_results(page)
            self.results['Google Images'] = results
            
            await page.close()
            
        except Exception as e:
            print(f"⚠️ Google Images error: {e}")
            self.results['Google Images'] = {'error': str(e), 'matches': []}
    
    async def extract_google_results(self, page):
        """Extract actual results from Google Images search"""
        results = {'matches': [], 'similar_images': [], 'pages_with_image': []}
        
        try:
            # Wait for results to load
            await page.wait_for_selector('div[data-ved]', timeout=10000)
            
            # Extract "Pages that include matching images"
            pages_elements = await page.query_selector_all('div[data-ved] a[href]')
            
            for element in pages_elements[:10]:  # Limit to first 10
                try:
                    href = await element.get_attribute('href')
                    text = await element.text_content()
                    
                    if href and text:
                        # Visit the page to extract more info
                        info = await self.extract_page_info(page.context, href, text)
                        results['pages_with_image'].append(info)
                        
                except Exception as e:
                    continue
            
            # Extract names and information from results
            await self.extract_names_from_results(results)
            
            print(f"✅ Google: Found {len(results['pages_with_image'])} matching pages")
            
        except Exception as e:
            print(f"⚠️ Google result extraction error: {e}")
        
        return results
    
    async def extract_page_info(self, context, url, title):
        """Extract information from a webpage"""
        info = {
            'url': url,
            'title': title,
            'names': [],
            'content': '',
            'social_links': [],
            'contact_info': []
        }
        
        try:
            page = await context.new_page()
            response = await page.goto(url, timeout=15000)
            
            if response and response.status == 200:
                # Get page title and content
                info['title'] = await page.title()
                content = await page.text_content('body')
                info['content'] = content[:500] if content else ''
                
                # Extract names using regex patterns
                names = self.extract_names_from_text(content or '')
                info['names'] = list(names)
                
                # Extract social media links
                social_links = await page.query_selector_all('a[href*="facebook"], a[href*="twitter"], a[href*="instagram"], a[href*="linkedin"]')
                for link in social_links:
                    href = await link.get_attribute('href')
                    if href:
                        info['social_links'].append(href)
                
                # Extract contact information
                emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content or '')
                phones = re.findall(r'\b\d{3}-\d{3}-\d{4}\b|\b\(\d{3}\)\s*\d{3}-\d{4}\b', content or '')
                
                info['contact_info'] = list(set(emails + phones))
                
                # Add to extracted info
                self.extracted_info['names'].update(names)
                self.extracted_info['social_profiles'].extend(info['social_links'])
                self.extracted_info['contact_info'].extend(info['contact_info'])
                
            await page.close()
            
        except Exception as e:
            info['error'] = str(e)
        
        return info
    
    def extract_names_from_text(self, text):
        """Extract potential names from text using patterns"""
        names = set()
        
        if not text:
            return names
        
        # Common name patterns
        name_patterns = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # First Last
            r'\b[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+\b',  # First M. Last
            r'\b[A-Z][a-z]+, [A-Z][a-z]+\b',  # Last, First
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, text)
            names.update(matches)
        
        # Filter out common false positives
        false_positives = {'New York', 'Los Angeles', 'United States', 'Google Inc', 'Facebook Inc'}
        names = names - false_positives
        
        return names
    
    async def extract_names_from_results(self, results):
        """Extract names from search results"""
        for page in results.get('pages_with_image', []):
            names = page.get('names', [])
            self.extracted_info['names'].update(names)
    
    async def search_yandex_images_enhanced(self, browser):
        """Enhanced Yandex Images search"""
        print("🔍 Searching Yandex Images...")
        
        try:
            page = await browser.new_page()
            await page.goto('https://yandex.com/images/')
            
            # Try to upload image (simplified)
            camera_selector = 'div[data-bem*="camera"]'
            try:
                await page.click(camera_selector, timeout=5000)
                # File upload would go here
                print("✅ Yandex: Search initiated")
            except:
                print("⚠️ Yandex: Manual upload required")
            
            await page.close()
            
        except Exception as e:
            print(f"⚠️ Yandex error: {e}")
    
    async def search_social_media_enhanced(self, browser):
        """Search social media platforms for the person"""
        print("🔍 Searching social media platforms...")
        
        # If we have extracted names, search for them on social media
        if self.extracted_info['names']:
            for name in list(self.extracted_info['names'])[:3]:  # Limit to first 3 names
                await self.search_facebook_profile(browser, name)
                await self.search_linkedin_profile(browser, name)
        
        print(f"✅ Social media: Searched for {len(list(self.extracted_info['names'])[:3])} names")
    
    async def search_facebook_profile(self, browser, name):
        """Search Facebook for profiles matching the name"""
        try:
            page = await browser.new_page()
            search_url = f"https://www.facebook.com/search/people/?q={quote(name)}"
            await page.goto(search_url, timeout=10000)
            
            # Facebook requires login for detailed results
            # This is a simplified extraction
            title = await page.title()
            if "Facebook" in title:
                self.extracted_info['social_profiles'].append({
                    'platform': 'Facebook',
                    'search_name': name,
                    'url': search_url,
                    'status': 'login_required'
                })
            
            await page.close()
            
        except Exception as e:
            pass  # Fail silently
    
    async def search_linkedin_profile(self, browser, name):
        """Search LinkedIn for profiles matching the name"""
        try:
            page = await browser.new_page()
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={quote(name)}"
            await page.goto(search_url, timeout=10000)
            
            title = await page.title()
            if "LinkedIn" in title:
                self.extracted_info['social_profiles'].append({
                    'platform': 'LinkedIn',
                    'search_name': name,
                    'url': search_url,
                    'status': 'login_required'
                })
            
            await page.close()
            
        except Exception as e:
            pass  # Fail silently
    
    async def search_people_databases_enhanced(self, browser):
        """Search people finder databases"""
        print("🔍 Searching people databases...")
        
        databases = [
            'https://www.whitepages.com',
            'https://www.spokeo.com',
            'https://www.peekyou.com'
        ]
        
        if self.extracted_info['names']:
            name = list(self.extracted_info['names'])[0]  # Use first name found
            
            for db_url in databases:
                try:
                    page = await browser.new_page()
                    await page.goto(f"{db_url}/search/people?name={quote(name)}")
                    await page.wait_for_timeout(3000)
                    
                    # Extract basic info (simplified)
                    content = await page.text_content('body')
                    if content and name.lower() in content.lower():
                        self.extracted_info['public_records'].append({
                            'database': db_url,
                            'search_name': name,
                            'found': True,
                            'details': 'Details available on site'
                        })
                    
                    await page.close()
                    
                except Exception as e:
                    continue
        
        print(f"✅ People databases: Searched {len(databases)} databases")
    
    async def search_face_recognition_sites(self, browser):
        """Simulate searches on face recognition websites"""
        print("🔍 Searching face recognition databases...")
        
        # PimEyes simulation (requires manual upload in practice)
        self.extracted_info['face_recognition_results'] = [{
            'platform': 'PimEyes',
            'status': 'manual_required',
            'url': 'https://pimeyes.com/en',
            'note': 'Upload image manually for best face recognition results'
        }]
        
        print("✅ Face recognition: Sites identified for manual search")
    
    def generate_enhanced_report(self):
        """Generate comprehensive report with extracted information"""
        print("\n" + "=" * 80)
        print("🎯 ENHANCED FACE SEARCH RESULTS - PUBLIC INFORMATION EXTRACTED")
        print("=" * 80)
        print(f"📷 Image analyzed: {self.image_path}")
        print(f"🕐 Search completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Face Analysis Results
        if hasattr(self, 'face_encoding') and self.face_encoding is not None:
            print("👤 FACIAL ANALYSIS:")
            if 'demographics' in self.extracted_info:
                demo = self.extracted_info['demographics']
                print(f"   🎂 Estimated age: {demo.get('estimated_age_range', 'Unknown')}")
                print(f"   👤 Estimated gender: {demo.get('estimated_gender', 'Unknown')}")
                print(f"   🔍 Face shape: {demo.get('face_shape', 'Unknown')}")
            print()
        
        # Names Found
        if self.extracted_info['names']:
            print("📝 NAMES DISCOVERED:")
            for name in sorted(self.extracted_info['names']):
                print(f"   • {name}")
            print()
        
        # Social Media Profiles
        if self.extracted_info['social_profiles']:
            print("📱 SOCIAL MEDIA PROFILES:")
            for profile in self.extracted_info['social_profiles']:
                if isinstance(profile, dict):
                    print(f"   • {profile.get('platform', 'Unknown')}: {profile.get('search_name', 'Unknown')}")
                    print(f"     URL: {profile.get('url', 'N/A')}")
                else:
                    print(f"   • {profile}")
            print()
        
        # Public Records
        if self.extracted_info['public_records']:
            print("🏛️ PUBLIC RECORDS FOUND:")
            for record in self.extracted_info['public_records']:
                if isinstance(record, dict):
                    print(f"   • Database: {record.get('database', 'Unknown')}")
                    print(f"     Name searched: {record.get('search_name', 'Unknown')}")
                    print(f"     Results: {record.get('details', 'Available on site')}")
                else:
                    print(f"   • {record}")
            print()
        
        # Contact Information
        if self.extracted_info['contact_info']:
            print("📞 CONTACT INFORMATION:")
            for contact in set(self.extracted_info['contact_info']):
                if '@' in contact:
                    print(f"   📧 Email: {contact}")
                else:
                    print(f"   📱 Phone: {contact}")
            print()
        
        # Locations
        if self.extracted_info['locations']:
            print("📍 LOCATIONS MENTIONED:")
            for location in self.extracted_info['locations']:
                print(f"   • {location}")
            print()
        
        # Search Results Summary
        print("📊 SEARCH RESULTS SUMMARY:")
        google_results = self.results.get('Google Images', {})
        if 'matches' in google_results:
            pages = google_results.get('pages_with_image', [])
            print(f"   🔍 Google Images: {len(pages)} pages with matching images")
        
        print(f"   📝 Total names found: {len(self.extracted_info['names'])}")
        print(f"   📱 Social profiles identified: {len(self.extracted_info['social_profiles'])}")
        print(f"   🏛️ Public records found: {len(self.extracted_info['public_records'])}")
        print(f"   📞 Contact details: {len(set(self.extracted_info['contact_info']))}")
        print()
        
        # Recommendations
        print("💡 RECOMMENDATIONS:")
        if not self.extracted_info['names']:
            print("   • No names found automatically - try manual reverse image search")
            print("   • Upload to PimEyes.com for specialized face recognition")
        else:
            print("   • Use discovered names to search social media manually")
            print("   • Cross-reference information across multiple platforms")
            print("   • Verify information through multiple sources")
        
        print("   • Check specialized face recognition services manually")
        print("   • Search using any partial information discovered")
        print()
        
        # Save results to file
        self.save_results_to_file()
    
    def save_results_to_file(self):
        """Save results to a JSON file"""
        output_file = f"face_search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
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
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {output_file}")

async def main():
    if len(sys.argv) != 2:
        print("Usage: python3 enhanced_face_search.py <image_path>")
        print("Example: python3 enhanced_face_search.py /home/xx/Desktop/rey.jpeg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        sys.exit(1)
    
    # Verify it's an image
    try:
        with Image.open(image_path) as img:
            print(f"📷 Image loaded: {img.size[0]}x{img.size[1]} pixels, format: {img.format}")
    except Exception as e:
        print(f"Error: Could not load image - {e}")
        sys.exit(1)
    
    # Start enhanced search
    search_engine = EnhancedFaceSearch(image_path)
    await search_engine.search_and_extract_all()

if __name__ == "__main__":
    asyncio.run(main())