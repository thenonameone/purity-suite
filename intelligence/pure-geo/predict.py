#!/usr/bin/env python3
"""
Inference script for predicting location from images using trained geolocalization model.
"""

import argparse
import sys
from pathlib import Path
import torch
import numpy as np
from PIL import Image, ImageOps
import torchvision.transforms as transforms

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from utils import load_config
from models.geoloc_model import load_pretrained_model
from data.dataset import load_processed_data


class GeolocalizationPredictor:
    """
    Predictor class for geolocalization inference.
    """
    
    def __init__(self, model_path: str, config_path: str, processed_data_dir: str):
        """
        Initialize the predictor.
        
        Args:
            model_path: Path to the trained model checkpoint
            config_path: Path to the configuration file
            processed_data_dir: Path to processed data directory with clustering info
        """
        # Load configuration
        self.config = load_config(config_path)
        
        # Load clustering information
        _, self.clustering_info = load_processed_data(processed_data_dir)
        
        # Load model
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = load_pretrained_model(model_path, self.config, self.clustering_info)
        self.model.to(self.device)
        self.model.eval()
        
        # Setup image transforms
        self.transform = transforms.Compose([
            transforms.Resize(tuple(self.config['data']['image_size'])),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        print(f"Loaded model on device: {self.device}")
        print(f"Model ready for inference")
    
    def preprocess_image(self, image_path: str) -> torch.Tensor:
        """
        Preprocess an image for inference.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image tensor
        """
        # Load and convert image
        image = Image.open(image_path).convert('RGB')
        
        # Handle EXIF orientation
        image = ImageOps.exif_transpose(image)
        
        # Apply transforms
        image_tensor = self.transform(image)
        
        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)
        
        return image_tensor
    
    def predict(self, image_path: str, top_k: int = 5) -> dict:
        """
        Predict location for a single image.
        
        Args:
            image_path: Path to the image file
            top_k: Number of top predictions to return for hierarchical levels
            
        Returns:
            Dictionary containing predictions
        """
        # Preprocess image
        image_tensor = self.preprocess_image(image_path).to(self.device)
        
        # Run inference
        with torch.no_grad():
            predictions = self.model(image_tensor)
        
        results = {
            'image_path': image_path,
            'predicted_coordinates': {},
            'hierarchical_predictions': {},
            'confidence_scores': {}
        }
        
        # Extract coordinate prediction
        coords = predictions['coordinates'].cpu().numpy()[0]
        results['predicted_coordinates'] = {
            'latitude': float(coords[0]),
            'longitude': float(coords[1])
        }
        
        # Extract hierarchical predictions with confidence scores
        for level in ['country', 'region', 'city', 'precise']:
            if level in predictions:
                logits = predictions[level].cpu().numpy()[0]
                probabilities = torch.softmax(predictions[level], dim=1).cpu().numpy()[0]
                
                # Get top-k predictions
                top_indices = np.argsort(probabilities)[::-1][:top_k]
                
                level_predictions = []
                for idx in top_indices:
                    confidence = float(probabilities[idx])
                    
                    # Convert class ID back to coordinates if clustering info available
                    if level in self.clustering_info:
                        try:
                            from utils.geo_utils import class_to_coord
                            lat, lon = class_to_coord(idx, self.clustering_info[level])
                            level_predictions.append({
                                'class_id': int(idx),
                                'confidence': confidence,
                                'coordinates': {
                                    'latitude': float(lat),
                                    'longitude': float(lon)
                                }
                            })
                        except (KeyError, ValueError):
                            level_predictions.append({
                                'class_id': int(idx),
                                'confidence': confidence,
                                'coordinates': None
                            })
                
                results['hierarchical_predictions'][level] = level_predictions
                results['confidence_scores'][level] = float(probabilities[top_indices[0]])
        
        return results


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Geolocalization Inference')
    
    parser.add_argument('--model', type=str, required=True,
                       help='Path to trained model checkpoint')
    parser.add_argument('--config', type=str, default='configs/config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--data-dir', type=str, required=True,
                       help='Path to processed data directory')
    parser.add_argument('--image', type=str, required=True,
                       help='Path to image for prediction')
    parser.add_argument('--output', type=str,
                       help='Output file path for results')
    
    return parser.parse_args()


def main():
    """Main inference function."""
    args = parse_arguments()
    
print("🌍 Pure GEO - AI Geolocalization Inference")
    print("=" * 42)
    
    # Initialize predictor
    print("Loading model and configuration...")
    predictor = GeolocalizationPredictor(
        model_path=args.model,
        config_path=args.config,
        processed_data_dir=args.data_dir
    )
    
    # Single image prediction
    print(f"Predicting location for: {args.image}")
    result = predictor.predict(args.image)
    
    # Print results
    coords = result['predicted_coordinates']
    print(f"\nPredicted Location:")
    print(f"  Latitude:  {coords['latitude']:8.4f}")
    print(f"  Longitude: {coords['longitude']:8.4f}")
    
    # Print hierarchical predictions
    for level, preds in result.get('hierarchical_predictions', {}).items():
        if preds:
            confidence = result['confidence_scores'][level]
            print(f"  {level.title()} confidence: {confidence:.3f}")
    
    # Save results if output path specified
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to {args.output}")
    
    print("\nInference completed successfully!")


if __name__ == '__main__':
    main()