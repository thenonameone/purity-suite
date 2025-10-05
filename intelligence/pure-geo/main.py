#!/usr/bin/env python3
"""
Pure GEO - Advanced AI Geolocalization Intelligence System
Main entry point for training and data processing.
"""

import argparse
import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from utils import load_config, setup_logger, create_directories, validate_config
from utils.geo_utils import create_hierarchical_clusters, save_clustering_info
from data.dataset import DataCollector, create_data_loaders, save_processed_data
from models.geoloc_model import create_model
from models.trainer import GeolocalizationTrainer


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Train Geolocalization AI System')
    
    parser.add_argument('--config', type=str, default='configs/config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--data-source', type=str, 
                       choices=['flickr', 'exif', 'custom'],
                       help='Data source type')
    parser.add_argument('--data-path', type=str,
                       help='Path to data source (CSV file or image directory)')
    parser.add_argument('--max-images', type=int, default=10000,
                       help='Maximum number of images to use')
    parser.add_argument('--resume', type=str,
                       help='Resume training from checkpoint')
    parser.add_argument('--eval-only', action='store_true',
                       help='Only run evaluation on test set')
    
    return parser.parse_args()


def collect_and_prepare_data(config, args):
    """Collect and prepare training data."""
    print("\n=== DATA COLLECTION AND PREPARATION ===")
    
    collector = DataCollector(config)
    
    if args.data_source == 'flickr':
        print("Loading data from Flickr CSV...")
        df = collector.collect_from_flickr_csv(args.data_path)
        
        if len(df) > 0 and 'url' in df.columns:
            print(f"Downloading {min(args.max_images, len(df))} images...")
            df = collector.download_images(df, max_images=args.max_images)
        
    elif args.data_source == 'exif':
        print("Extracting GPS coordinates from EXIF data...")
        df = collector.extract_exif_coordinates(args.data_path)
        
    elif args.data_source == 'custom':
        print(f"Loading custom data from {args.data_path}...")
        df = pd.read_csv(args.data_path)
        
        # Validate required columns
        required_columns = ['image_path', 'lat', 'lon']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Custom CSV must contain columns: {required_columns}")
    
    else:
        raise ValueError(f"Unknown data source: {args.data_source}")
    
    if len(df) == 0:
        raise ValueError("No data found or collected. Please check your data source.")
    
    print(f"Collected {len(df)} geotagged images")
    
    # Filter by maximum images if specified
    if len(df) > args.max_images:
        df = df.sample(n=args.max_images, random_state=42).reset_index(drop=True)
        print(f"Randomly sampled {args.max_images} images")
    
    # Basic data validation
    df = df.dropna(subset=['lat', 'lon'])
    df = df[(df['lat'] >= -90) & (df['lat'] <= 90)]
    df = df[(df['lon'] >= -180) & (df['lon'] <= 180)]
    
    print(f"Final dataset size after validation: {len(df)} images")
    
    if len(df) < 100:
        print("Warning: Very small dataset. Consider collecting more data for better results.")
    
    return df


def create_geographic_clusters(df, config):
    """Create hierarchical geographic clusters."""
    print("\n=== CREATING GEOGRAPHIC CLUSTERS ===")
    
    # Extract coordinates
    coordinates = [(row['lat'], row['lon']) for _, row in df.iterrows()]
    
    print(f"Creating hierarchical clusters from {len(coordinates)} unique locations...")
    
    # Create hierarchical clusters
    clustering_info = create_hierarchical_clusters(coordinates, config)
    
    # Save clustering information
    clustering_path = Path(config['data']['processed_dir']) / 'clustering_info.pkl'
    save_clustering_info(clustering_info, str(clustering_path))
    
    return clustering_info


def split_data(df, config):
    """Split data into train/validation/test sets."""
    print("\n=== SPLITTING DATA ===")
    
    val_split = config['training']['validation_split']
    test_split = config['training']['test_split']
    
    # First split: separate test set
    train_val_df, test_df = train_test_split(
        df, 
        test_size=test_split, 
        random_state=42,
        stratify=None  # Could stratify by country clusters if available
    )
    
    # Second split: separate train and validation
    val_size_adjusted = val_split / (1 - test_split)
    train_df, val_df = train_test_split(
        train_val_df,
        test_size=val_size_adjusted,
        random_state=42,
        stratify=None
    )
    
    print(f"Data split - Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
    
    return train_df, val_df, test_df


def main():
    """Main training function."""
    args = parse_arguments()
    
    print("🌍 Pure GEO - AI Geolocalization Training System")
    print("=" * 52)
    
    # Load configuration
    print(f"Loading configuration from {args.config}...")
    config = load_config(args.config)
    validate_config(config)
    
    # Setup directories and logging
    create_directories(config)
    setup_logger(
        config['logging']['level'],
        config['logging']['file'],
        config['logging']['format']
    )
    
    print(f"System device: {config['system']['device']}")
    print(f"Model backbone: {config['model']['backbone']}")
    
    # Skip data collection if only evaluating
    if not args.eval_only:
        # Collect and prepare data
        if not args.data_source or not args.data_path:
            raise ValueError("Must specify --data-source and --data-path for training")
            
        df = collect_and_prepare_data(config, args)
        
        # Create geographic clusters
        clustering_info = create_geographic_clusters(df, config)
        
        # Split data
        train_df, val_df, test_df = split_data(df, config)
        
        # Save processed data
        processed_dir = config['data']['processed_dir']
        save_processed_data(df, clustering_info, processed_dir)
        
        # Save split datasets
        train_df.to_csv(Path(processed_dir) / 'train.csv', index=False)
        val_df.to_csv(Path(processed_dir) / 'val.csv', index=False)
        test_df.to_csv(Path(processed_dir) / 'test.csv', index=False)
        
        print(f"Processed data saved to {processed_dir}")
    
    else:
        # Load processed data for evaluation
        print("Loading processed data for evaluation...")
        from data.dataset import load_processed_data
        
        processed_dir = config['data']['processed_dir']
        df, clustering_info = load_processed_data(processed_dir)
        
        # Load test split
        test_df = pd.read_csv(Path(processed_dir) / 'test.csv')
        train_df = val_df = None  # Not needed for evaluation
    
    # Create model
    print("\n=== CREATING MODEL ===")
    model = create_model(config, clustering_info)
    print(f"Model created with {sum(p.numel() for p in model.parameters())} parameters")
    
    if not args.eval_only:
        # Create data loaders
        print("\n=== CREATING DATA LOADERS ===")
        train_loader, val_loader = create_data_loaders(
            train_df, val_df, clustering_info, config
        )
        
        print(f"Training batches: {len(train_loader)}")
        print(f"Validation batches: {len(val_loader)}")
        
        # Create trainer
        print("\n=== INITIALIZING TRAINER ===")
        trainer = GeolocalizationTrainer(model, train_loader, val_loader, config, clustering_info)
        
        # Resume from checkpoint if specified
        if args.resume:
            print(f"Resuming from checkpoint: {args.resume}")
            trainer.load_checkpoint(args.resume)
        
        # Start training
        print("\n=== STARTING TRAINING ===")
        training_history = trainer.train()
        
        print("\n=== TRAINING COMPLETED ===")
        print(f"Best validation loss: {trainer.best_val_loss:.4f}")
        print(f"Best distance error: {trainer.best_distance_error:.2f} km")
        
        # Load best model for final evaluation
        trainer.load_checkpoint('best_model.pth')
    
    else:
        # Load pre-trained model for evaluation
        if not args.resume:
            raise ValueError("Must specify --resume checkpoint for evaluation mode")
        
        from models.geoloc_model import load_pretrained_model
        model = load_pretrained_model(args.resume, config, clustering_info)
        
        trainer = GeolocalizationTrainer(model, None, None, config, clustering_info)
    
    # Final evaluation on test set
    if 'test_df' in locals() and len(test_df) > 0:
        print("\n=== FINAL EVALUATION ===")
        
        # Create test data loader
        from data.dataset import GeoImageDataset
        from torch.utils.data import DataLoader
        
        test_dataset = GeoImageDataset(
            test_df, 
            clustering_info, 
            config['data']['raw_dir'],
            image_size=tuple(config['data']['image_size']),
            augment=False
        )
        
        test_loader = DataLoader(
            test_dataset,
            batch_size=config['training']['batch_size'],
            shuffle=False,
            num_workers=config['system']['num_workers']
        )
        
        test_metrics = trainer.evaluate_model(test_loader)
        
        print("\n=== FINAL RESULTS ===")
        for threshold in config['evaluation']['distance_thresholds']:
            accuracy = test_metrics[f'accuracy_{threshold}km'] * 100
            print(f"Accuracy within {threshold:4d}km: {accuracy:5.1f}%")
        
        print(f"Mean distance error:   {test_metrics['mean_distance_error_km']:8.2f} km")
        print(f"Median distance error: {test_metrics['median_distance_error_km']:8.2f} km")
    
    print("\nTraining and evaluation completed successfully!")


if __name__ == '__main__':
    main()