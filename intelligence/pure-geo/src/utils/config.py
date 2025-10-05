"""
Configuration utilities for the geolocalization system.
"""

import yaml
import torch
import os
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str = "configs/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary containing configuration parameters
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Resolve relative paths
    base_dir = Path.cwd()
    if 'data' in config:
        for key in ['raw_dir', 'processed_dir', 'models_dir']:
            if key in config['data']:
                config['data'][key] = str(base_dir / config['data'][key])
    
    return config


def get_device(device_preference: str = "auto") -> str:
    """
    Determine the best available device for computation.
    
    Args:
        device_preference: Preferred device ("auto", "cpu", "cuda", "mps")
        
    Returns:
        Device string for PyTorch
    """
    if device_preference == "auto":
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    elif device_preference == "cuda":
        if not torch.cuda.is_available():
            print("Warning: CUDA requested but not available. Using CPU.")
            return "cpu"
        return "cuda"
    
    elif device_preference == "mps":
        if not (hasattr(torch.backends, "mps") and torch.backends.mps.is_available()):
            print("Warning: MPS requested but not available. Using CPU.")
            return "cpu"
        return "mps"
    
    else:
        return "cpu"


def create_directories(config: Dict[str, Any]) -> None:
    """
    Create necessary directories based on configuration.
    
    Args:
        config: Configuration dictionary
    """
    directories = [
        config['data']['raw_dir'],
        config['data']['processed_dir'], 
        config['data']['models_dir'],
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration parameters.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if configuration is valid
    """
    required_sections = ['data', 'model', 'training', 'clustering']
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Required configuration section missing: {section}")
    
    # Validate image size
    if len(config['data']['image_size']) != 2:
        raise ValueError("image_size must be a list of 2 integers")
    
    # Validate model parameters
    if config['model']['num_classes'] <= 0:
        raise ValueError("num_classes must be positive")
        
    return True