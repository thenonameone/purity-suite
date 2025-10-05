#!/usr/bin/env python3
import sys
import subprocess
import urllib.parse
import base64
import os

def google_reverse_search(image_path):
    """Open Google reverse image search for the given image"""
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return
    
    # Create Google Images search URL
    google_url = "https://images.google.com/searchbyimage?image_url="
    
    # For local files, we'll construct a search URL that opens Google Images
    # and the user can upload the file manually
    search_url = "https://images.google.com/imghp?hl=en&tab=wi&authuser=0"
    
    print(f"Opening Google Reverse Image Search...")
    print(f"Image: {image_path}")
    print(f"URL: {search_url}")
    
    # Try to open in browser
    try:
        subprocess.run(['xdg-open', search_url], check=True)
        print("\nGoogle Images opened in your browser.")
        print("Click the camera icon and upload your image for reverse search.")
    except subprocess.CalledProcessError:
        print(f"\nCouldn't open browser automatically.")
        print(f"Please visit: {search_url}")
        print("Then click the camera icon and upload your image.")

def pimeyes_search(image_path):
    """Open PimEyes for face search"""
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return
        
    pimeyes_url = "https://pimeyes.com/en"
    
    print(f"Opening PimEyes Face Search...")
    print(f"Image: {image_path}")
    print(f"URL: {pimeyes_url}")
    
    try:
        subprocess.run(['xdg-open', pimeyes_url], check=True)
        print("\nPimEyes opened in your browser.")
        print("Upload your image for face recognition search.")
    except subprocess.CalledProcessError:
        print(f"\nCouldn't open browser automatically.")
        print(f"Please visit: {pimeyes_url}")
        print("Then upload your image for face search.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 reverse_face_search.py <service> <image_path>")
        print("Services: google, pimeyes, yandex")
        print("Example: python3 reverse_face_search.py pimeyes /home/xx/Desktop/rey.jpeg")
        sys.exit(1)
    
    service = sys.argv[1].lower()
    image_path = sys.argv[2]
    
    if service == "google":
        google_reverse_search(image_path)
    elif service == "pimeyes":
        pimeyes_search(image_path)
    elif service == "yandex":
        yandex_url = "https://yandex.com/images/"
        print(f"Opening Yandex Images...")
        subprocess.run(['xdg-open', yandex_url], check=True)
        print("Click the camera icon and upload your image.")
    else:
        print(f"Unknown service: {service}")
        print("Available services: google, pimeyes, yandex")

if __name__ == "__main__":
    main()