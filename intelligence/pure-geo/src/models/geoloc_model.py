"""
Main geolocalization neural network model.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from typing import Dict, List, Tuple, Optional
import timm


class GeolocalizationModel(nn.Module):
    """
    Hierarchical geolocalization model that predicts location at multiple scales.
    """
    
    def __init__(self, 
                 backbone: str = "efficientnet-b4",
                 num_classes_dict: Dict[str, int] = None,
                 embedding_dim: int = 512,
                 dropout: float = 0.2,
                 pretrained: bool = True):
        """
        Initialize the geolocalization model.
        
        Args:
            backbone: Backbone architecture name
            num_classes_dict: Dictionary with number of classes for each hierarchy level
            embedding_dim: Dimension of the feature embedding
            dropout: Dropout rate
            pretrained: Whether to use pretrained weights
        """
        super(GeolocalizationModel, self).__init__()
        
        if num_classes_dict is None:
            num_classes_dict = {
                'country': 195,
                'region': 1000, 
                'city': 10000,
                'precise': 100000
            }
        
        self.num_classes_dict = num_classes_dict
        self.embedding_dim = embedding_dim
        
        # Load backbone model
        self.backbone = self._create_backbone(backbone, pretrained)
        
        # Get feature dimension from backbone
        self.feature_dim = self._get_feature_dim()
        
        # Feature embedding layer
        self.feature_embedding = nn.Sequential(
            nn.Linear(self.feature_dim, embedding_dim * 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(embedding_dim * 2, embedding_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        # Classification heads for different hierarchy levels
        self.classifiers = nn.ModuleDict()
        for level, num_classes in num_classes_dict.items():
            self.classifiers[level] = nn.Sequential(
                nn.Linear(embedding_dim, embedding_dim // 2),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(embedding_dim // 2, num_classes)
            )
        
        # Coordinate regression head (lat, lon)
        self.coord_regressor = nn.Sequential(
            nn.Linear(embedding_dim, embedding_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(embedding_dim // 2, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, 2),
            nn.Tanh()  # Output between -1 and 1, will be scaled to lat/lon ranges
        )
        
    def _create_backbone(self, backbone_name: str, pretrained: bool) -> nn.Module:
        """Create the backbone model."""
        if backbone_name.startswith('efficientnet'):
            model = timm.create_model(backbone_name, pretrained=pretrained, num_classes=0)
            return model
        elif backbone_name.startswith('resnet'):
            if backbone_name == 'resnet18':
                model = models.resnet18(pretrained=pretrained)
            elif backbone_name == 'resnet50':
                model = models.resnet50(pretrained=pretrained)
            else:
                raise ValueError(f"Unsupported ResNet variant: {backbone_name}")
            # Remove the final classification layer
            model = nn.Sequential(*list(model.children())[:-1])
            return model
        elif backbone_name.startswith('vit'):
            model = timm.create_model(backbone_name, pretrained=pretrained, num_classes=0)
            return model
        else:
            raise ValueError(f"Unsupported backbone: {backbone_name}")
    
    def _get_feature_dim(self) -> int:
        """Get the feature dimension of the backbone."""
        dummy_input = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            features = self.backbone(dummy_input)
            if features.dim() > 2:
                features = F.adaptive_avg_pool2d(features, (1, 1))
                features = features.flatten(1)
            return features.shape[1]
    
    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Forward pass through the model.
        
        Args:
            x: Input tensor of shape (batch_size, 3, height, width)
            
        Returns:
            Dictionary containing predictions for each hierarchy level and coordinates
        """
        # Extract features using backbone
        features = self.backbone(x)
        
        # Handle different backbone output shapes
        if features.dim() > 2:
            features = F.adaptive_avg_pool2d(features, (1, 1))
            features = features.flatten(1)
        
        # Get feature embedding
        embedding = self.feature_embedding(features)
        
        # Predictions for each hierarchy level
        predictions = {}
        for level in self.classifiers.keys():
            predictions[level] = self.classifiers[level](embedding)
        
        # Coordinate regression
        coord_pred = self.coord_regressor(embedding)
        # Scale coordinates to proper ranges: lat [-90, 90], lon [-180, 180]
        coord_pred = torch.stack([
            coord_pred[:, 0] * 90,   # Latitude
            coord_pred[:, 1] * 180   # Longitude
        ], dim=1)
        
        predictions['coordinates'] = coord_pred
        predictions['embedding'] = embedding
        
        return predictions


class GeolocationLoss(nn.Module):
    """
    Multi-task loss function for hierarchical geolocalization.
    """
    
    def __init__(self, 
                 level_weights: Dict[str, float] = None,
                 coord_weight: float = 1.0,
                 use_focal_loss: bool = False):
        """
        Initialize the loss function.
        
        Args:
            level_weights: Weights for each hierarchy level
            coord_weight: Weight for coordinate regression loss
            use_focal_loss: Whether to use focal loss for classification
        """
        super(GeolocationLoss, self).__init__()
        
        if level_weights is None:
            level_weights = {
                'country': 0.3,
                'region': 0.3,
                'city': 0.2,
                'precise': 0.2
            }
        
        self.level_weights = level_weights
        self.coord_weight = coord_weight
        self.use_focal_loss = use_focal_loss
        
        if use_focal_loss:
            self.focal_loss = FocalLoss()
        else:
            self.ce_loss = nn.CrossEntropyLoss()
        
        self.mse_loss = nn.MSELoss()
        self.smooth_l1_loss = nn.SmoothL1Loss()
    
    def forward(self, 
                predictions: Dict[str, torch.Tensor], 
                targets: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Calculate multi-task loss.
        
        Args:
            predictions: Model predictions
            targets: Ground truth targets
            
        Returns:
            Dictionary containing individual losses and total loss
        """
        losses = {}
        total_loss = 0
        
        # Classification losses for each hierarchy level
        for level, weight in self.level_weights.items():
            if level in predictions and level in targets:
                if self.use_focal_loss:
                    loss = self.focal_loss(predictions[level], targets[level])
                else:
                    loss = self.ce_loss(predictions[level], targets[level])
                
                losses[f'{level}_loss'] = loss
                total_loss += weight * loss
        
        # Coordinate regression loss
        if 'coordinates' in predictions and 'coordinates' in targets:
            coord_loss = self.smooth_l1_loss(predictions['coordinates'], targets['coordinates'])
            losses['coord_loss'] = coord_loss
            total_loss += self.coord_weight * coord_loss
        
        losses['total_loss'] = total_loss
        return losses


class FocalLoss(nn.Module):
    """
    Focal Loss for addressing class imbalance.
    """
    
    def __init__(self, alpha: float = 1.0, gamma: float = 2.0):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
    
    def forward(self, inputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        return focal_loss.mean()


def create_model(config: Dict, clustering_info: Dict[str, Dict]) -> GeolocalizationModel:
    """
    Create a geolocalization model based on configuration.
    
    Args:
        config: Configuration dictionary
        clustering_info: Hierarchical clustering information
        
    Returns:
        Initialized model
    """
    # Extract number of classes for each level
    num_classes_dict = {}
    for level in ['country', 'region', 'city', 'precise']:
        if level in clustering_info:
            num_classes_dict[level] = clustering_info[level]['num_clusters']
    
    model = GeolocalizationModel(
        backbone=config['model']['backbone'],
        num_classes_dict=num_classes_dict,
        embedding_dim=config['model']['embedding_dim'],
        dropout=config['model']['dropout'],
        pretrained=config['model']['pretrained']
    )
    
    return model


def load_pretrained_model(model_path: str, 
                         config: Dict, 
                         clustering_info: Dict[str, Dict]) -> GeolocalizationModel:
    """
    Load a pre-trained model from checkpoint.
    
    Args:
        model_path: Path to the model checkpoint
        config: Configuration dictionary
        clustering_info: Hierarchical clustering information
        
    Returns:
        Loaded model
    """
    model = create_model(config, clustering_info)
    
    # Load state dict
    checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)
    
    if 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
    
    return model