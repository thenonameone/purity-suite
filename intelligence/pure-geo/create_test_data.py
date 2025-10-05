#!/usr/bin/env python3
"""
Create test data for the geolocalization system.
"""

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import os
from pathlib import Path

def create_synthetic_test_images():
    """Create synthetic test images with different visual patterns for different regions."""
    
    # Create directories
    os.makedirs("data/test_images", exist_ok=True)
    
    test_data = []
    
    # Define some test locations with distinctive visual patterns
    locations = [
        {"name": "desert", "lat": 25.0, "lon": 55.0, "color": (255, 180, 120)},  # Desert (Dubai)
        {"name": "forest", "lat": 45.5, "lon": -122.5, "color": (34, 139, 34)}, # Forest (Portland)
        {"name": "urban", "lat": 40.7, "lon": -74.0, "color": (128, 128, 128)},  # Urban (NYC)
        {"name": "beach", "lat": 21.3, "lon": -157.8, "color": (255, 218, 185)}, # Beach (Hawaii)
        {"name": "mountain", "lat": 46.5, "lon": 7.7, "color": (139, 69, 19)},   # Mountain (Switzerland)
    ]
    
    # Create multiple images for each location
    for i, location in enumerate(locations):
        for j in range(5):  # 5 images per location
            # Create a synthetic image
            img = Image.new('RGB', (224, 224), color=location["color"])
            draw = ImageDraw.Draw(img)
            
            # Add some random patterns to make images unique
            np.random.seed(i * 10 + j)
            
            # Add some random rectangles/circles
            for _ in range(np.random.randint(3, 8)):
                x1 = np.random.randint(0, 150)
                y1 = np.random.randint(0, 150)
                x2 = x1 + np.random.randint(20, 74)
                y2 = y1 + np.random.randint(20, 74)
                
                # Vary color slightly
                color_var = tuple(max(0, min(255, c + np.random.randint(-50, 50))) 
                                for c in location["color"])
                
                if np.random.random() > 0.5:
                    draw.rectangle([x1, y1, x2, y2], fill=color_var)
                else:
                    draw.ellipse([x1, y1, x2, y2], fill=color_var)
            
            # Save image
            filename = f"{location['name']}_{j:02d}.jpg"
            filepath = f"data/test_images/{filename}"
            img.save(filepath)
            
            # Add some noise to coordinates
            lat_noise = np.random.normal(0, 0.1)
            lon_noise = np.random.normal(0, 0.1)
            
            test_data.append({
                'image_path': filename,
                'lat': location['lat'] + lat_noise,
                'lon': location['lon'] + lon_noise,
                'region': location['name']
            })
    
    # Create CSV file
    df = pd.DataFrame(test_data)
    df.to_csv("data/test_dataset.csv", index=False)
    
    print(f"Created {len(test_data)} test images and dataset CSV")
    print("Test locations:")
    for location in locations:
        print(f"  {location['name']}: ({location['lat']}, {location['lon']})")
    
    return df

if __name__ == "__main__":
    create_synthetic_test_images()