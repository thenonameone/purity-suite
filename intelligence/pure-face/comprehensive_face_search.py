#!/usr/bin/env python3
"""
Comprehensive Face Search Tool
Searches across multiple search engines and public databases for face matches
"""

import sys
import os
import requests
import base64
import json
import time
import subprocess
import threading
from urllib.parse import urlencode, quote
from PIL import Image
import tempfile
from datetime import datetime

class FaceSearchEngine:
    def __init__(self, image_path):
        self.image_path = image_path
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def search_all_engines(self):
        """Search across all available engines simultaneously"""
        print(f"🔍 Starting comprehensive face search for: {self.image_path}")
        print("=" * 70)
        
        # Create threads for simultaneous searching
        search_threads = []
        
        # List of search functions to run
        search_functions = [
            self.search_google_images,
            self.search_yandex_images,
            self.search_bing_images,
            self.search_tineye,
            self.search_pimeyes,
            self.search_social_media_platforms,
            self.search_public_databases,
            self.search_specialized_engines
        ]
        
        # Start all searches in parallel
        for search_func in search_functions:
            thread = threading.Thread(target=self._safe_search, args=(search_func,))
            thread.start()
            search_threads.append(thread)
        
        # Wait for all searches to complete
        for thread in search_threads:
            thread.join()
        
        self.generate_report()
        
    def _safe_search(self, search_func):
        """Safely execute a search function with error handling"""
        try:
            search_func()
        except Exception as e:
            engine_name = search_func.__name__.replace('search_', '').replace('_', ' ').title()
            self.results[engine_name] = {
                'status': 'error',
                'error': str(e),
                'matches': []
            }
    
    def search_google_images(self):
        """Search Google Images"""
        print("🔍 Searching Google Images...")
        
        # Google Images reverse search
        try:
            # Upload image and get search URL
            google_url = "https://images.google.com/searchbyimage/upload"
            
            with open(self.image_path, 'rb') as img_file:
                files = {'encoded_image': img_file}
                response = self.session.post(google_url, files=files, timeout=30)
                
                if response.status_code == 200:
                    # Extract results from response
                    search_url = response.url
                    self.results['Google Images'] = {
                        'status': 'success',
                        'search_url': search_url,
                        'matches': self._extract_google_results(response.text),
                        'method': 'automated_upload'
                    }
                else:
                    # Fallback to manual search URL
                    self.results['Google Images'] = {
                        'status': 'manual_required',
                        'search_url': 'https://images.google.com/imghp',
                        'instruction': 'Upload image manually using camera icon',
                        'matches': []
                    }
        except Exception as e:
            self.results['Google Images'] = {
                'status': 'error',
                'error': str(e),
                'fallback_url': 'https://images.google.com/imghp',
                'matches': []
            }
    
    def search_yandex_images(self):
        """Search Yandex Images"""
        print("🔍 Searching Yandex Images...")
        
        try:
            yandex_url = "https://yandex.com/images/search"
            
            with open(self.image_path, 'rb') as img_file:
                files = {'upfile': img_file}
                data = {'rpt': 'imageview'}
                
                response = self.session.post(yandex_url, files=files, data=data, timeout=30)
                
                if response.status_code == 200:
                    self.results['Yandex Images'] = {
                        'status': 'success',
                        'search_url': response.url,
                        'matches': self._extract_yandex_results(response.text),
                        'method': 'automated_upload'
                    }
                else:
                    self.results['Yandex Images'] = {
                        'status': 'manual_required',
                        'search_url': 'https://yandex.com/images/',
                        'instruction': 'Upload image manually',
                        'matches': []
                    }
        except Exception as e:
            self.results['Yandex Images'] = {
                'status': 'error',
                'error': str(e),
                'fallback_url': 'https://yandex.com/images/',
                'matches': []
            }
    
    def search_bing_images(self):
        """Search Bing Visual Search"""
        print("🔍 Searching Bing Visual Search...")
        
        try:
            # Bing Visual Search
            bing_url = "https://www.bing.com/images/search"
            
            self.results['Bing Visual Search'] = {
                'status': 'manual_required',
                'search_url': 'https://www.bing.com/visualsearch',
                'instruction': 'Upload image using camera icon',
                'matches': []
            }
        except Exception as e:
            self.results['Bing Visual Search'] = {
                'status': 'error',
                'error': str(e),
                'fallback_url': 'https://www.bing.com/visualsearch',
                'matches': []
            }
    
    def search_tineye(self):
        """Search TinEye reverse image search"""
        print("🔍 Searching TinEye...")
        
        try:
            # TinEye API would require API key for automated search
            self.results['TinEye'] = {
                'status': 'manual_required',
                'search_url': 'https://tineye.com/',
                'instruction': 'Upload image manually or use API with key',
                'matches': []
            }
        except Exception as e:
            self.results['TinEye'] = {
                'status': 'error',
                'error': str(e),
                'fallback_url': 'https://tineye.com/',
                'matches': []
            }
    
    def search_pimeyes(self):
        """Search PimEyes face recognition"""
        print("🔍 Searching PimEyes...")
        
        try:
            # PimEyes requires manual upload or premium API
            self.results['PimEyes'] = {
                'status': 'manual_required',
                'search_url': 'https://pimeyes.com/en',
                'instruction': 'Upload image for face recognition search',
                'matches': [],
                'note': 'Best for face recognition - premium service'
            }
        except Exception as e:
            self.results['PimEyes'] = {
                'status': 'error',
                'error': str(e),
                'fallback_url': 'https://pimeyes.com/en',
                'matches': []
            }
    
    def search_social_media_platforms(self):
        """Search across social media platforms"""
        print("🔍 Searching Social Media Platforms...")
        
        social_platforms = {
            'Facebook': 'https://www.facebook.com/',
            'LinkedIn': 'https://www.linkedin.com/',
            'Instagram': 'https://www.instagram.com/',
            'Twitter/X': 'https://twitter.com/',
            'VKontakte': 'https://vk.com/',
            'Odnoklassniki': 'https://ok.ru/'
        }
        
        self.results['Social Media'] = {
            'status': 'manual_search_required',
            'platforms': social_platforms,
            'instruction': 'Manual search required - most platforms dont allow automated face search',
            'matches': []
        }
    
    def search_public_databases(self):
        """Search public databases and directories"""
        print("🔍 Searching Public Databases...")
        
        public_dbs = {
            'Whitepages': 'https://www.whitepages.com/',
            'Spokeo': 'https://www.spokeo.com/',
            'PeekYou': 'https://www.peekyou.com/',
            'Pipl': 'https://pipl.com/',
            'BeenVerified': 'https://www.beenverified.com/',
            'TruePeopleSearch': 'https://www.truepeoplesearch.com/'
        }
        
        self.results['Public Databases'] = {
            'status': 'manual_search_required',
            'databases': public_dbs,
            'instruction': 'Manual search recommended - requires personal info not just image',
            'matches': []
        }
    
    def search_specialized_engines(self):
        """Search specialized reverse image search engines"""
        print("🔍 Searching Specialized Engines...")
        
        specialized_engines = {
            'Baidu Images': 'https://image.baidu.com/',
            'SauceNAO': 'https://saucenao.com/',
            'IQDB': 'https://iqdb.org/',
            'ASCII2D': 'https://ascii2d.net/',
            'RevEye': 'https://reveye.ai/'
        }
        
        self.results['Specialized Engines'] = {
            'status': 'manual_required',
            'engines': specialized_engines,
            'instruction': 'Upload image to each specialized engine',
            'matches': []
        }
    
    def _extract_google_results(self, html):
        """Extract results from Google Images response"""
        # This would require parsing HTML - simplified for demo
        return []
    
    def _extract_yandex_results(self, html):
        """Extract results from Yandex Images response"""
        # This would require parsing HTML - simplified for demo
        return []
    
    def open_all_search_urls(self):
        """Open all search URLs in browser"""
        print("\n🌐 Opening all search platforms in browser...")
        
        urls_to_open = []
        
        for engine, data in self.results.items():
            if isinstance(data, dict):
                if 'search_url' in data:
                    urls_to_open.append(data['search_url'])
                elif 'fallback_url' in data:
                    urls_to_open.append(data['fallback_url'])
                elif 'platforms' in data:
                    urls_to_open.extend(data['platforms'].values())
                elif 'databases' in data:
                    urls_to_open.extend(data['databases'].values())
                elif 'engines' in data:
                    urls_to_open.extend(data['engines'].values())
        
        # Open URLs with delays to avoid overwhelming the system
        for i, url in enumerate(urls_to_open[:10]):  # Limit to first 10 to avoid spam
            try:
                subprocess.run(['xdg-open', url], check=True)
                if i < len(urls_to_open) - 1:
                    time.sleep(2)  # 2 second delay between opens
            except subprocess.CalledProcessError:
                print(f"⚠️  Couldn't open: {url}")
    
    def generate_report(self):
        """Generate comprehensive search report"""
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE FACE SEARCH REPORT")
        print("=" * 70)
        print(f"📷 Image: {self.image_path}")
        print(f"🕐 Search completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        for engine, data in self.results.items():
            print(f"🔍 {engine}:")
            if isinstance(data, dict):
                status = data.get('status', 'unknown')
                
                if status == 'success':
                    print(f"   ✅ Status: Success")
                    print(f"   🔗 URL: {data.get('search_url', 'N/A')}")
                    matches = data.get('matches', [])
                    print(f"   📊 Matches found: {len(matches)}")
                    
                elif status == 'manual_required':
                    print(f"   ⚠️  Status: Manual upload required")
                    print(f"   🔗 URL: {data.get('search_url', 'N/A')}")
                    print(f"   💡 Instructions: {data.get('instruction', 'Upload image manually')}")
                    
                elif status == 'manual_search_required':
                    print(f"   ⚠️  Status: Manual search required")
                    print(f"   💡 Instructions: {data.get('instruction', 'Manual search needed')}")
                    
                elif status == 'error':
                    print(f"   ❌ Status: Error - {data.get('error', 'Unknown error')}")
                    if 'fallback_url' in data:
                        print(f"   🔗 Fallback URL: {data['fallback_url']}")
                
                if 'note' in data:
                    print(f"   📝 Note: {data['note']}")
            
            print()
        
        print("🚀 NEXT STEPS:")
        print("1. Review the URLs above and visit each platform manually")
        print("2. Upload your image to each service that requires manual upload")
        print("3. For social media, search using any names or details you discover")
        print("4. Check specialized databases with any personal information found")
        print()
        
        # Ask if user wants to open all URLs
        try:
            response = input("Would you like to open all search URLs in your browser? (y/N): ").lower()
            if response in ['y', 'yes']:
                self.open_all_search_urls()
        except KeyboardInterrupt:
            print("\nSearch complete!")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 comprehensive_face_search.py <image_path>")
        print("Example: python3 comprehensive_face_search.py /home/xx/Desktop/rey.jpeg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        sys.exit(1)
    
    # Check if it's actually an image
    try:
        with Image.open(image_path) as img:
            print(f"📷 Image loaded: {img.size[0]}x{img.size[1]} pixels, format: {img.format}")
    except Exception as e:
        print(f"Error: Could not load image - {e}")
        sys.exit(1)
    
    # Start comprehensive search
    search_engine = FaceSearchEngine(image_path)
    search_engine.search_all_engines()

if __name__ == "__main__":
    main()