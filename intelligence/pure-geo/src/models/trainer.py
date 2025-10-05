"""
Training module for the geolocalization model.
"""

import os
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from torch.cuda.amp import autocast, GradScaler
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import ReduceLROnPlateau, CosineAnnealingLR

import pandas as pd
import numpy as np
from tqdm import tqdm
from loguru import logger

from .geoloc_model import GeolocalizationModel, GeolocationLoss
try:
    from ..utils.geo_utils import class_to_coord, calculate_prediction_accuracy
except ImportError:
    # Fallback for when running as main module
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from utils.geo_utils import class_to_coord, calculate_prediction_accuracy


class GeolocalizationTrainer:
    """
    Trainer for the geolocalization model.
    """
    
    def __init__(self, 
                 model: GeolocalizationModel,
                 train_loader: DataLoader,
                 val_loader: DataLoader,
                 config: Dict,
                 clustering_info: Dict[str, Dict]):
        """
        Initialize the trainer.
        
        Args:
            model: The geolocalization model
            train_loader: Training data loader
            val_loader: Validation data loader
            config: Configuration dictionary
            clustering_info: Hierarchical clustering information
        """
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config
        self.clustering_info = clustering_info
        
        # Setup device
        self.device = torch.device(self.config['system']['device']) \
            if self.config['system']['device'] != 'auto' \
            else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Move model to device
        self.model = self.model.to(self.device)
        
        # Setup loss function
        self.criterion = GeolocationLoss(
            level_weights=self.config['training']['hierarchical_weights'],
            coord_weight=1.0,
            use_focal_loss=False
        )
        
        # Setup optimizer
        self.optimizer = optim.AdamW(
            self.model.parameters(),
            lr=self.config['training']['learning_rate'],
            weight_decay=1e-4
        )
        
        # Setup learning rate scheduler
        self.scheduler = ReduceLROnPlateau(
            self.optimizer, 
            mode='min', 
            factor=0.5, 
            patience=5
        )
        
        # Mixed precision training
        self.use_amp = self.config['system'].get('mixed_precision', True)
        self.scaler = GradScaler() if self.use_amp else None
        
        # Training state
        self.current_epoch = 0
        self.best_val_loss = float('inf')
        self.best_distance_error = float('inf')
        self.epochs_without_improvement = 0
        
        # Metrics tracking
        self.train_losses = []
        self.val_losses = []
        self.val_accuracies = []
        
        # Create model save directory
        self.model_dir = Path(self.config['data']['models_dir'])
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Trainer initialized. Using device: {self.device}")
        logger.info(f"Model has {sum(p.numel() for p in self.model.parameters())} parameters")
    
    def train_epoch(self) -> Dict[str, float]:
        """Train for one epoch."""
        self.model.train()
        
        total_loss = 0
        total_coord_loss = 0
        level_losses = {level: 0 for level in ['country', 'region', 'city', 'precise']}
        
        progress_bar = tqdm(self.train_loader, desc=f"Epoch {self.current_epoch + 1}")
        
        for batch_idx, batch in enumerate(progress_bar):
            # Move data to device
            images = batch['image'].to(self.device, non_blocking=True)
            targets = {k: v.to(self.device, non_blocking=True) 
                      for k, v in batch['targets'].items()}
            
            self.optimizer.zero_grad()
            
            # Forward pass with mixed precision
            if self.use_amp:
                with autocast():
                    predictions = self.model(images)
                    loss_dict = self.criterion(predictions, targets)
                    loss = loss_dict['total_loss']
                
                # Backward pass
                self.scaler.scale(loss).backward()
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                predictions = self.model(images)
                loss_dict = self.criterion(predictions, targets)
                loss = loss_dict['total_loss']
                
                # Backward pass
                loss.backward()
                self.optimizer.step()
            
            # Update metrics
            total_loss += loss.item()
            if 'coord_loss' in loss_dict:
                total_coord_loss += loss_dict['coord_loss'].item()
            
            for level in level_losses.keys():
                if f'{level}_loss' in loss_dict:
                    level_losses[level] += loss_dict[f'{level}_loss'].item()
            
            # Update progress bar
            progress_bar.set_postfix({
                'loss': f"{loss.item():.4f}",
                'coord_loss': f"{loss_dict.get('coord_loss', 0):.4f}"
            })
        
        # Calculate average losses
        num_batches = len(self.train_loader)
        avg_loss = total_loss / num_batches
        avg_coord_loss = total_coord_loss / num_batches
        avg_level_losses = {level: loss / num_batches for level, loss in level_losses.items()}
        
        metrics = {
            'train_loss': avg_loss,
            'train_coord_loss': avg_coord_loss,
            **{f'train_{level}_loss': loss for level, loss in avg_level_losses.items()}
        }
        
        return metrics
    
    def validate_epoch(self) -> Dict[str, float]:
        """Validate for one epoch."""
        self.model.eval()
        
        total_loss = 0
        total_coord_loss = 0
        level_losses = {level: 0 for level in ['country', 'region', 'city', 'precise']}
        
        # For accuracy calculation
        true_coords = []
        predicted_coords = []
        
        with torch.no_grad():
            for batch in tqdm(self.val_loader, desc="Validating"):
                # Move data to device
                images = batch['image'].to(self.device, non_blocking=True)
                targets = {k: v.to(self.device, non_blocking=True) 
                          for k, v in batch['targets'].items()}
                
                # Forward pass
                if self.use_amp:
                    with autocast():
                        predictions = self.model(images)
                        loss_dict = self.criterion(predictions, targets)
                else:
                    predictions = self.model(images)
                    loss_dict = self.criterion(predictions, targets)
                
                # Update metrics
                total_loss += loss_dict['total_loss'].item()
                if 'coord_loss' in loss_dict:
                    total_coord_loss += loss_dict['coord_loss'].item()
                
                for level in level_losses.keys():
                    if f'{level}_loss' in loss_dict:
                        level_losses[level] += loss_dict[f'{level}_loss'].item()
                
                # Collect coordinates for accuracy calculation
                batch_true_coords = targets['coordinates'].cpu().numpy()
                batch_pred_coords = predictions['coordinates'].cpu().numpy()
                
                true_coords.extend(batch_true_coords)
                predicted_coords.extend(batch_pred_coords)
        
        # Calculate average losses
        num_batches = len(self.val_loader)
        avg_loss = total_loss / num_batches
        avg_coord_loss = total_coord_loss / num_batches
        avg_level_losses = {level: loss / num_batches for level, loss in level_losses.items()}
        
        # Calculate geographic accuracies
        true_coords_list = [(coord[0], coord[1]) for coord in true_coords]
        predicted_coords_list = [(coord[0], coord[1]) for coord in predicted_coords]
        
        accuracy_metrics = calculate_prediction_accuracy(
            true_coords_list,
            predicted_coords_list,
            self.config['evaluation']['distance_thresholds']
        )
        
        metrics = {
            'val_loss': avg_loss,
            'val_coord_loss': avg_coord_loss,
            **{f'val_{level}_loss': loss for level, loss in avg_level_losses.items()},
            **{f'val_{k}': v for k, v in accuracy_metrics.items()}
        }
        
        return metrics
    
    def train(self) -> Dict[str, List]:
        """Main training loop."""
        logger.info("Starting training...")
        
        num_epochs = self.config['training']['num_epochs']
        patience = self.config['training']['early_stopping_patience']
        
        for epoch in range(num_epochs):
            self.current_epoch = epoch
            
            # Training phase
            train_metrics = self.train_epoch()
            
            # Validation phase
            val_metrics = self.validate_epoch()
            
            # Combine metrics
            epoch_metrics = {**train_metrics, **val_metrics}
            
            # Update learning rate
            self.scheduler.step(val_metrics['val_loss'])
            
            # Log metrics
            self._log_metrics(epoch_metrics)
            
            # Save metrics
            self.train_losses.append(train_metrics['train_loss'])
            self.val_losses.append(val_metrics['val_loss'])
            self.val_accuracies.append(val_metrics.get('val_mean_distance_error_km', 0))
            
            # Check for improvement
            val_loss = val_metrics['val_loss']
            distance_error = val_metrics.get('val_mean_distance_error_km', float('inf'))
            
            improved = False
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                improved = True
            
            if distance_error < self.best_distance_error:
                self.best_distance_error = distance_error
                improved = True
            
            if improved:
                self.epochs_without_improvement = 0
                self.save_checkpoint('best_model.pth', epoch_metrics)
                logger.info(f"New best model saved! Val loss: {val_loss:.4f}, Distance error: {distance_error:.2f} km")
            else:
                self.epochs_without_improvement += 1
            
            # Early stopping
            if self.epochs_without_improvement >= patience:
                logger.info(f"Early stopping after {epoch + 1} epochs")
                break
            
            # Save checkpoint every 10 epochs
            if (epoch + 1) % 10 == 0:
                self.save_checkpoint(f'checkpoint_epoch_{epoch + 1}.pth', epoch_metrics)
        
        logger.info("Training completed!")
        return {
            'train_losses': self.train_losses,
            'val_losses': self.val_losses,
            'val_accuracies': self.val_accuracies
        }
    
    def save_checkpoint(self, filename: str, metrics: Dict[str, float]):
        """Save model checkpoint."""
        checkpoint = {
            'epoch': self.current_epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'best_val_loss': self.best_val_loss,
            'best_distance_error': self.best_distance_error,
            'config': self.config,
            'metrics': metrics
        }
        
        if self.scaler:
            checkpoint['scaler_state_dict'] = self.scaler.state_dict()
        
        torch.save(checkpoint, self.model_dir / filename)
    
    def load_checkpoint(self, filename: str):
        """Load model checkpoint."""
        checkpoint_path = self.model_dir / filename
        
        if not checkpoint_path.exists():
            logger.warning(f"Checkpoint {checkpoint_path} not found")
            return
        
        checkpoint = torch.load(checkpoint_path, map_location=self.device, weights_only=False)
        
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        
        self.current_epoch = checkpoint['epoch']
        self.best_val_loss = checkpoint['best_val_loss']
        self.best_distance_error = checkpoint.get('best_distance_error', float('inf'))
        
        if self.scaler and 'scaler_state_dict' in checkpoint:
            self.scaler.load_state_dict(checkpoint['scaler_state_dict'])
        
        logger.info(f"Loaded checkpoint from epoch {self.current_epoch}")
    
    def _log_metrics(self, metrics: Dict[str, float]):
        """Log training metrics."""
        epoch = self.current_epoch + 1
        
        # Log main metrics
        logger.info(f"Epoch {epoch:3d} | "
                   f"Train Loss: {metrics.get('train_loss', 0):.4f} | "
                   f"Val Loss: {metrics.get('val_loss', 0):.4f} | "
                   f"Distance Error: {metrics.get('val_mean_distance_error_km', 0):.2f} km")
        
        # Log accuracy at different thresholds
        thresholds = self.config['evaluation']['distance_thresholds']
        accuracy_str = " | ".join([f"{t}km: {metrics.get(f'val_accuracy_{t}km', 0)*100:.1f}%" 
                                  for t in thresholds[:3]])  # Log first 3 thresholds
        logger.info(f"Accuracies | {accuracy_str}")
    
    def evaluate_model(self, test_loader: DataLoader) -> Dict[str, float]:
        """Evaluate model on test set."""
        logger.info("Evaluating model on test set...")
        
        self.model.eval()
        
        predictions_list = []
        targets_list = []
        
        with torch.no_grad():
            for batch in tqdm(test_loader, desc="Testing"):
                images = batch['image'].to(self.device)
                targets = batch['targets']
                
                if self.use_amp:
                    with autocast():
                        predictions = self.model(images)
                else:
                    predictions = self.model(images)
                
                # Store predictions and targets
                batch_predictions = {
                    'coordinates': predictions['coordinates'].cpu().numpy(),
                }
                
                batch_targets = {
                    'coordinates': targets['coordinates'].numpy(),
                }
                
                # Add hierarchical predictions if available
                for level in ['country', 'region', 'city', 'precise']:
                    if level in predictions and level in targets:
                        batch_predictions[level] = predictions[level].cpu().numpy()
                        batch_targets[level] = targets[level].numpy()
                
                predictions_list.append(batch_predictions)
                targets_list.append(batch_targets)
        
        # Aggregate results
        all_pred_coords = np.vstack([p['coordinates'] for p in predictions_list])
        all_true_coords = np.vstack([t['coordinates'] for t in targets_list])
        
        # Calculate accuracies
        true_coords_list = [(coord[0], coord[1]) for coord in all_true_coords]
        pred_coords_list = [(coord[0], coord[1]) for coord in all_pred_coords]
        
        test_metrics = calculate_prediction_accuracy(
            true_coords_list,
            pred_coords_list,
            self.config['evaluation']['distance_thresholds']
        )
        
        logger.info("Test Results:")
        logger.info(f"Mean Distance Error: {test_metrics['mean_distance_error_km']:.2f} km")
        logger.info(f"Median Distance Error: {test_metrics['median_distance_error_km']:.2f} km")
        
        for threshold in self.config['evaluation']['distance_thresholds']:
            accuracy = test_metrics[f'accuracy_{threshold}km'] * 100
            logger.info(f"Accuracy within {threshold}km: {accuracy:.1f}%")
        
        return test_metrics


def create_trainer(model: GeolocalizationModel,
                  train_loader: DataLoader,
                  val_loader: DataLoader,
                  config: Dict,
                  clustering_info: Dict[str, Dict]) -> GeolocalizationTrainer:
    """Create a trainer instance."""
    return GeolocalizationTrainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        config=config,
        clustering_info=clustering_info
    )
