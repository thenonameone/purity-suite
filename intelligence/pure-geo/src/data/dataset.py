"""
Dataset handling and preprocessing for geolocalized images.
"""

import os
import pandas as pd
import numpy as np
from PIL import Image, ImageOps, ExifTags
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from typing import Dict, List, Tuple, Optional, Union
import requests
from tqdm import tqdm
import json
import pickle
import exifread
import piexif
from pathlib import Path


class GeoImageDataset(Dataset):
    """
    Custom dataset for geotagged images.
    """
    
    def __init__(self, 
                 data_df: pd.DataFrame,
                 clustering_info: Dict[str, Dict],
                 image_dir: str,
                 image_size: Tuple[int, int] = (224, 224),
                 transform: Optional[transforms.Compose] = None,
                 augment: bool = True):
        """
        Initialize the dataset.
        
        Args:
            data_df: DataFrame with columns ['image_path', 'lat', 'lon', ...]
            clustering_info: Hierarchical clustering information
            image_dir: Directory containing images
            image_size: Target image size
            transform: Custom transforms
            augment: Whether to apply data augmentation
        """
        self.data_df = data_df.reset_index(drop=True)
        self.clustering_info = clustering_info
        self.image_dir = Path(image_dir)
        self.image_size = image_size
        
        # Create transforms if not provided
        if transform is None:
            self.transform = self._create_transforms(augment)
        else:
            self.transform = transform
            
        # Pre-compute class labels for all hierarchy levels
        self._compute_class_labels()
    
    def _create_transforms(self, augment: bool) -> transforms.Compose:
        """Create image transforms."""
        transform_list = [
            transforms.Resize(self.image_size),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ]
        
        if augment:
            # Add data augmentation for training
            augment_list = [
                transforms.RandomResizedCrop(self.image_size[0], scale=(0.8, 1.0)),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomRotation(degrees=15),
                transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
                transforms.RandomAffine(degrees=0, translate=(0.1, 0.1))
            ] + transform_list[1:]  # Skip resize as we're using RandomResizedCrop
            
            return transforms.Compose(augment_list)
        
        return transforms.Compose(transform_list)
    
    def _compute_class_labels(self):
        """Pre-compute class labels for all images."""
        try:
            from ..utils.geo_utils import coord_to_class
        except ImportError:
            from utils.geo_utils import coord_to_class
        
        print("Computing class labels for all images...")
        
        for level in ['country', 'region', 'city', 'precise']:
            if level in self.clustering_info:
                class_labels = []
                for _, row in tqdm(self.data_df.iterrows(), total=len(self.data_df), 
                                desc=f"Computing {level} labels"):
                    class_id = coord_to_class(
                        row['lat'], row['lon'], 
                        self.clustering_info[level]
                    )
                    class_labels.append(class_id)
                
                self.data_df[f'{level}_class'] = class_labels
        
        print("Class labels computed successfully.")
    
    def __len__(self) -> int:
        return len(self.data_df)
    
    def __getitem__(self, idx: int) -> Dict[str, Union[torch.Tensor, np.ndarray]]:
        """Get a single item from the dataset."""
        row = self.data_df.iloc[idx]
        
        # Load image
        image_path = self.image_dir / row['image_path']
        
        try:
            image = Image.open(image_path).convert('RGB')
            
            # Handle EXIF orientation
            image = ImageOps.exif_transpose(image)
            
            # Apply transforms
            if self.transform:
                image = self.transform(image)
            
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            # Return a black image as fallback
            image = torch.zeros(3, *self.image_size)
        
        # Prepare targets
        targets = {
            'coordinates': torch.tensor([row['lat'], row['lon']], dtype=torch.float32)
        }
        
        # Add hierarchical class labels
        for level in ['country', 'region', 'city', 'precise']:
            if f'{level}_class' in row:
                targets[level] = torch.tensor(row[f'{level}_class'], dtype=torch.long)
        
        return {
            'image': image,
            'targets': targets,
            'metadata': {
                'image_path': str(image_path),
                'lat': row['lat'],
                'lon': row['lon']
            }
        }


class DataCollector:
    """
    Collects geotagged images from various sources.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.data_dir = Path(config['data']['raw_dir'])
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def collect_from_flickr_csv(self, csv_path: str) -> pd.DataFrame:
        """
        Collect data from Flickr CSV (like YFCC100M subset).
        
        Expected CSV columns: ['photo_id', 'user_id', 'latitude', 'longitude', 'url', ...]
        """
        print(f"Loading Flickr data from {csv_path}")
        
        try:
            df = pd.read_csv(csv_path, sep='\t')  # YFCC100M uses tab-separated
            
            # Rename columns to standard format
            column_mapping = {
                'latitude': 'lat',
                'longitude': 'lon',
                'photo_id': 'image_id'
            }
            
            df = df.rename(columns=column_mapping)
            
            # Filter valid coordinates
            df = df.dropna(subset=['lat', 'lon'])
            df = df[(df['lat'] >= -90) & (df['lat'] <= 90)]
            df = df[(df['lon'] >= -180) & (df['lon'] <= 180)]
            
            print(f"Loaded {len(df)} valid geotagged images")
            return df
            
        except Exception as e:
            print(f"Error loading Flickr data: {e}")
            return pd.DataFrame()
    
    def download_images(self, df: pd.DataFrame, max_images: int = 10000) -> pd.DataFrame:
        """
        Download images from URLs in the dataframe.
        """
        print(f"Downloading up to {max_images} images...")
        
        downloaded_data = []
        
        for idx, row in tqdm(df.head(max_images).iterrows(), total=min(max_images, len(df))):
            try:
                image_id = row['image_id']
                url = row['url']
                
                # Create filename
                filename = f"{image_id}.jpg"
                filepath = self.data_dir / filename
                
                # Skip if already exists
                if filepath.exists():
                    downloaded_data.append({
                        'image_path': filename,
                        'lat': row['lat'],
                        'lon': row['lon'],
                        'image_id': image_id
                    })
                    continue
                
                # Download image
                response = requests.get(url, timeout=30, stream=True)
                response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Verify image can be opened
                try:
                    img = Image.open(filepath)
                    img.verify()
                    
                    downloaded_data.append({
                        'image_path': filename,
                        'lat': row['lat'],
                        'lon': row['lon'],
                        'image_id': image_id
                    })
                    
                except Exception:
                    # Remove invalid image
                    if filepath.exists():
                        filepath.unlink()
                
            except Exception as e:
                print(f"Error downloading {url}: {e}")
                continue
        
        result_df = pd.DataFrame(downloaded_data)
        print(f"Successfully downloaded {len(result_df)} images")
        return result_df
    
    def extract_exif_coordinates(self, image_dir: str) -> pd.DataFrame:
        """
        Extract GPS coordinates from EXIF data of images in a directory.
        """
        print(f"Extracting EXIF GPS data from images in {image_dir}")
        
        image_dir = Path(image_dir)
        image_data = []
        
        # Supported image extensions
        extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif'}
        
        image_files = [f for f in image_dir.iterdir() 
                      if f.is_file() and f.suffix.lower() in extensions]
        
        for image_path in tqdm(image_files, desc="Processing images"):
            try:
                # Try PIL EXIF first
                coords = self._extract_gps_pil(image_path)
                
                if coords is None:
                    # Try exifread as fallback
                    coords = self._extract_gps_exifread(image_path)
                
                if coords is not None:
                    lat, lon = coords
                    image_data.append({
                        'image_path': image_path.name,
                        'lat': lat,
                        'lon': lon
                    })
                    
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                continue
        
        result_df = pd.DataFrame(image_data)
        print(f"Extracted GPS data from {len(result_df)} images")
        return result_df
    
    def _extract_gps_pil(self, image_path: Path) -> Optional[Tuple[float, float]]:
        """Extract GPS coordinates using PIL."""
        try:
            with Image.open(image_path) as img:
                exifdata = img.getexif()
                
                if exifdata is not None:
                    for tag_id in exifdata:
                        tag = ExifTags.TAGS.get(tag_id, tag_id)
                        if tag == "GPSInfo":
                            gps_data = exifdata[tag_id]
                            return self._parse_gps_data(gps_data)
        except Exception:
            pass
        return None
    
    def _extract_gps_exifread(self, image_path: Path) -> Optional[Tuple[float, float]]:
        """Extract GPS coordinates using exifread."""
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f)
                
                lat_ref = tags.get('GPS GPSLatitudeRef')
                lat = tags.get('GPS GPSLatitude')
                lon_ref = tags.get('GPS GPSLongitudeRef')
                lon = tags.get('GPS GPSLongitude')
                
                if all(v is not None for v in [lat_ref, lat, lon_ref, lon]):
                    lat_deg = self._convert_to_degrees(lat.values)
                    lon_deg = self._convert_to_degrees(lon.values)
                    
                    if str(lat_ref) == 'S':
                        lat_deg = -lat_deg
                    if str(lon_ref) == 'W':
                        lon_deg = -lon_deg
                        
                    return lat_deg, lon_deg
        except Exception:
            pass
        return None
    
    def _parse_gps_data(self, gps_data: Dict) -> Optional[Tuple[float, float]]:
        """Parse GPS data from PIL EXIF."""
        try:
            lat = gps_data.get(2)  # GPSLatitude
            lat_ref = gps_data.get(1)  # GPSLatitudeRef
            lon = gps_data.get(4)  # GPSLongitude 
            lon_ref = gps_data.get(3)  # GPSLongitudeRef
            
            if all(v is not None for v in [lat, lat_ref, lon, lon_ref]):
                lat_deg = self._convert_to_degrees(lat)
                lon_deg = self._convert_to_degrees(lon)
                
                if lat_ref == 'S':
                    lat_deg = -lat_deg
                if lon_ref == 'W':
                    lon_deg = -lon_deg
                    
                return lat_deg, lon_deg
        except Exception:
            pass
        return None
    
    def _convert_to_degrees(self, values) -> float:
        """Convert GPS coordinates to decimal degrees."""
        if hasattr(values, 'values'):  # exifread format
            d, m, s = values
            return float(d.num / d.den) + float(m.num / m.den) / 60 + float(s.num / s.den) / 3600
        else:  # PIL format
            d, m, s = values
            return float(d) + float(m) / 60 + float(s) / 3600


def create_data_loaders(train_df: pd.DataFrame,
                       val_df: pd.DataFrame,
                       clustering_info: Dict[str, Dict],
                       config: Dict) -> Tuple[DataLoader, DataLoader]:
    """
    Create training and validation data loaders.
    """
    image_dir = config['data']['raw_dir']
    image_size = tuple(config['data']['image_size'])
    batch_size = config['training']['batch_size']
    num_workers = config['system']['num_workers']
    
    # Create datasets
    train_dataset = GeoImageDataset(
        train_df, 
        clustering_info, 
        image_dir, 
        image_size=image_size,
        augment=True
    )
    
    val_dataset = GeoImageDataset(
        val_df, 
        clustering_info, 
        image_dir, 
        image_size=image_size,
        augment=False
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=config['system'].get('pin_memory', True),
        drop_last=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=config['system'].get('pin_memory', True)
    )
    
    return train_loader, val_loader


def save_processed_data(df: pd.DataFrame, 
                       clustering_info: Dict[str, Dict],
                       output_dir: str):
    """Save processed dataset and clustering info."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save dataframe
    df.to_csv(output_dir / 'dataset.csv', index=False)
    
    # Save clustering info
    with open(output_dir / 'clustering_info.pkl', 'wb') as f:
        pickle.dump(clustering_info, f)
    
    print(f"Saved processed data to {output_dir}")


def load_processed_data(data_dir: str) -> Tuple[pd.DataFrame, Dict[str, Dict]]:
    """Load processed dataset and clustering info."""
    data_dir = Path(data_dir)
    
    # Load dataframe
    df = pd.read_csv(data_dir / 'dataset.csv')
    
    # Load clustering info
    with open(data_dir / 'clustering_info.pkl', 'rb') as f:
        clustering_info = pickle.load(f)
    
    return df, clustering_info