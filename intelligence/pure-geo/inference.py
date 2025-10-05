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
        
        print(f\"Loaded model on device: {self.device}\")
        print(f\"Model ready for inference\")
    
    def preprocess_image(self, image_path: str) -> torch.Tensor:
        \"\"\"
        Preprocess an image for inference.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image tensor
        \"\"\"
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
        \"\"\"
        Predict location for a single image.
        
        Args:
            image_path: Path to the image file
            top_k: Number of top predictions to return for hierarchical levels
            
        Returns:
            Dictionary containing predictions
        \"\"\"
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
                logits = predictions[level].cpu().numpy()[0]\n                probabilities = torch.softmax(predictions[level], dim=1).cpu().numpy()[0]\\n                \\n                # Get top-k predictions\\n                top_indices = np.argsort(probabilities)[::-1][:top_k]\\n                \\n                level_predictions = []\\n                for idx in top_indices:\\n                    confidence = float(probabilities[idx])\\n                    \\n                    # Convert class ID back to coordinates if clustering info available\\n                    if level in self.clustering_info:\\n                        try:\\n                            from utils.geo_utils import class_to_coord\\n                            lat, lon = class_to_coord(idx, self.clustering_info[level])\\n                            level_predictions.append({\\n                                'class_id': int(idx),\\n                                'confidence': confidence,\\n                                'coordinates': {\\n                                    'latitude': float(lat),\\n                                    'longitude': float(lon)\\n                                }\\n                            })\\n                        except (KeyError, ValueError):\\n                            level_predictions.append({\\n                                'class_id': int(idx),\\n                                'confidence': confidence,\\n                                'coordinates': None\\n                            })\\n                \\n                results['hierarchical_predictions'][level] = level_predictions\\n                results['confidence_scores'][level] = float(probabilities[top_indices[0]])\\n        \\n        return results\\n    \\n    def predict_batch(self, image_paths: list, batch_size: int = 32) -> list:\\n        \\\"\\\"\\\"\\n        Predict locations for multiple images.\\n        \\n        Args:\\n            image_paths: List of image file paths\\n            batch_size: Batch size for processing\\n            \\n        Returns:\\n            List of prediction results\\n        \\\"\\\"\\\"\\n        results = []\\n        \\n        for i in range(0, len(image_paths), batch_size):\\n            batch_paths = image_paths[i:i + batch_size]\\n            batch_tensors = []\\n            \\n            # Preprocess batch\\n            for path in batch_paths:\\n                try:\\n                    tensor = self.preprocess_image(path)\\n                    batch_tensors.append(tensor)\\n                except Exception as e:\\n                    print(f\\\"Error processing {path}: {e}\\\")\\n                    batch_tensors.append(None)\\n            \\n            # Filter out failed images\\n            valid_indices = [i for i, t in enumerate(batch_tensors) if t is not None]\\n            valid_tensors = [batch_tensors[i] for i in valid_indices]\\n            valid_paths = [batch_paths[i] for i in valid_indices]\\n            \\n            if valid_tensors:\\n                # Combine into batch\\n                batch_tensor = torch.cat(valid_tensors, dim=0).to(self.device)\\n                \\n                # Run inference\\n                with torch.no_grad():\\n                    batch_predictions = self.model(batch_tensor)\\n                \\n                # Process results\\n                for j, path in enumerate(valid_paths):\\n                    result = {\\n                        'image_path': path,\\n                        'predicted_coordinates': {\\n                            'latitude': float(batch_predictions['coordinates'][j, 0].cpu()),\\n                            'longitude': float(batch_predictions['coordinates'][j, 1].cpu())\\n                        }\\n                    }\\n                    results.append(result)\\n        \\n        return results\\n    \\n    def visualize_prediction(self, result: dict, save_path: str = None):\\n        \\\"\\\"\\\"\\n        Create a visualization of the prediction result.\\n        \\n        Args:\\n            result: Prediction result from predict()\\n            save_path: Optional path to save the visualization\\n        \\\"\\\"\\\"\\n        try:\\n            import folium\\n            import matplotlib.pyplot as plt\\n            from matplotlib.patches import Rectangle\\n            import matplotlib.image as mpimg\\n        except ImportError:\\n            print(\\\"Visualization requires folium and matplotlib. Install with:\\\")\\n            print(\\\"pip install folium matplotlib\\\")\\n            return\\n        \\n        coords = result['predicted_coordinates']\\n        lat, lon = coords['latitude'], coords['longitude']\\n        \\n        # Create map centered on prediction\\n        m = folium.Map(location=[lat, lon], zoom_start=10)\\n        \\n        # Add marker for prediction\\n        folium.Marker(\\n            [lat, lon],\\n            popup=f\\\"Predicted Location<br>Lat: {lat:.4f}<br>Lon: {lon:.4f}\\\",\\n            tooltip=\\\"Predicted Location\\\",\\n            icon=folium.Icon(color='red', icon='info-sign')\\n        ).add_to(m)\\n        \\n        # Add hierarchical predictions if available\\n        colors = ['blue', 'green', 'orange', 'purple']\\n        for i, (level, preds) in enumerate(result.get('hierarchical_predictions', {}).items()):\\n            if preds and preds[0]['coordinates']:\\n                level_coords = preds[0]['coordinates']\\n                confidence = preds[0]['confidence']\\n                \\n                folium.CircleMarker(\\n                    [level_coords['latitude'], level_coords['longitude']],\\n                    radius=8,\\n                    popup=f\\\"{level.title()}<br>Confidence: {confidence:.3f}\\\",\\n                    color=colors[i % len(colors)],\\n                    fill=True,\\n                    opacity=0.7\\n                ).add_to(m)\\n        \\n        # Save or display map\\n        if save_path:\\n            m.save(save_path)\\n            print(f\\\"Map saved to {save_path}\\\")\\n        else:\\n            return m\\n\\n\\ndef parse_arguments():\\n    \\\"\\\"\\\"Parse command line arguments.\\\"\\\"\\\"\\n    parser = argparse.ArgumentParser(description='Geolocalization Inference')\\n    \\n    parser.add_argument('--model', type=str, required=True,\\n                       help='Path to trained model checkpoint')\\n    parser.add_argument('--config', type=str, default='configs/config.yaml',\\n                       help='Path to configuration file')\\n    parser.add_argument('--data-dir', type=str, required=True,\\n                       help='Path to processed data directory')\\n    parser.add_argument('--image', type=str,\\n                       help='Path to single image for prediction')\\n    parser.add_argument('--image-dir', type=str,\\n                       help='Directory containing images for batch prediction')\\n    parser.add_argument('--output', type=str,\\n                       help='Output file path for results')\\n    parser.add_argument('--visualize', action='store_true',\\n                       help='Create visualization of prediction')\\n    \\n    return parser.parse_args()\\n\\n\\ndef main():\\n    \\\"\\\"\\\"Main inference function.\\\"\\\"\\\"\\n    args = parse_arguments()\\n    \\n    print(\\\"Geolocalization AI - Inference Mode\\\")\\n    print(\\\"===================================\\\\n\\\")\\n    \\n    # Initialize predictor\\n    print(\\\"Loading model and configuration...\\\")\\n    predictor = GeolocalizationPredictor(\\n        model_path=args.model,\\n        config_path=args.config,\\n        processed_data_dir=args.data_dir\\n    )\\n    \\n    results = []\\n    \\n    if args.image:\\n        # Single image prediction\\n        print(f\\\"Predicting location for: {args.image}\\\")\\n        result = predictor.predict(args.image)\\n        results.append(result)\\n        \\n        # Print results\\n        coords = result['predicted_coordinates']\\n        print(f\\\"\\\\nPredicted Location:\\\")\\n        print(f\\\"  Latitude:  {coords['latitude']:8.4f}\\\")\\n        print(f\\\"  Longitude: {coords['longitude']:8.4f}\\\")\\n        \\n        # Print hierarchical predictions\\n        for level, preds in result.get('hierarchical_predictions', {}).items():\\n            if preds:\\n                confidence = result['confidence_scores'][level]\\n                print(f\\\"  {level.title()} confidence: {confidence:.3f}\\\")\\n        \\n        # Create visualization\\n        if args.visualize:\\n            output_path = args.output or 'prediction_map.html'\\n            predictor.visualize_prediction(result, output_path)\\n    \\n    elif args.image_dir:\\n        # Batch prediction\\n        import glob\\n        image_patterns = ['*.jpg', '*.jpeg', '*.png', '*.tiff', '*.tif']\\n        image_paths = []\\n        \\n        for pattern in image_patterns:\\n            image_paths.extend(glob.glob(f\\\"{args.image_dir}/{pattern}\\\"))\\n            image_paths.extend(glob.glob(f\\\"{args.image_dir}/**/{pattern}\\\", recursive=True))\\n        \\n        if not image_paths:\\n            print(f\\\"No images found in {args.image_dir}\\\")\\n            return\\n        \\n        print(f\\\"Found {len(image_paths)} images for prediction\\\")\\n        results = predictor.predict_batch(image_paths)\\n        \\n        print(f\\\"\\\\nCompleted predictions for {len(results)} images\\\")\\n    \\n    else:\\n        print(\\\"Error: Must specify either --image or --image-dir\\\")\\n        return\\n    \\n    # Save results if output path specified\\n    if args.output and not args.visualize:\\n        import json\\n        with open(args.output, 'w') as f:\\n            json.dump(results, f, indent=2)\\n        print(f\\\"Results saved to {args.output}\\\")\\n    \\n    print(\\\"\\\\nInference completed successfully!\\\")\\n\\n\\nif __name__ == '__main__':\\n    main()","line_range_start":38,"line_range_end":292}}
</function_results>

Let me fix the syntax issues in the inference script:

<function_calls>
<invoke name="edit_files">
<parameter name="title">Fix syntax errors in inference.py