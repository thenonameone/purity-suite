# Geolocalization AI - Determine Photo Location from Visual Content

This project implements a state-of-the-art deep learning system that can predict where a photograph was taken based solely on visual content like landmarks, landscape, architecture, and other geographic indicators.

## 🌟 Features

- **Hierarchical Prediction**: Predicts location at multiple scales (country → region → city → precise coordinates)
- **Advanced CNN Architecture**: Uses EfficientNet, ResNet, or Vision Transformer backbones
- **Multi-task Learning**: Simultaneously learns coordinate regression and hierarchical classification
- **Comprehensive Data Pipeline**: Supports multiple data sources (Flickr, EXIF, custom datasets)
- **Robust Training**: Mixed precision training, early stopping, and comprehensive evaluation
- **Easy Inference**: Simple prediction interface for new images

## 🏗️ Architecture

The system uses a hierarchical approach with several key components:

1. **Feature Extraction**: CNN backbone (EfficientNet-B4 by default)
2. **Multi-head Prediction**: Separate heads for coordinate regression and hierarchical classification
3. **Geographic Clustering**: K-means clustering to create discrete location classes at different scales
4. **Multi-task Loss**: Weighted combination of regression and classification losses

## 📋 Requirements

```bash
# Core ML/DL frameworks
torch>=2.0.0
torchvision>=0.15.0
timm>=0.9.0

# Computer Vision
opencv-python>=4.8.0
pillow>=10.0.0
scikit-image>=0.21.0

# Data processing
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0

# Geographic utilities  
geopy>=2.3.0
shapely>=2.0.0

# Utilities
tqdm>=4.65.0
pyyaml>=6.0
loguru>=0.7.0
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd geolocalization-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Your Data

The system supports three data sources:

#### Option A: Flickr/YFCC100M Dataset
```bash
# Download YFCC100M subset with GPS coordinates
# Format: photo_id, user_id, latitude, longitude, url, ...
python main.py --data-source flickr --data-path /path/to/yfcc100m.tsv --max-images 50000
```

#### Option B: Extract from EXIF Data
```bash
# Extract GPS coordinates from images with EXIF data
python main.py --data-source exif --data-path /path/to/image/directory --max-images 10000
```

#### Option C: Custom CSV Dataset
```bash
# Use your own dataset (CSV with columns: image_path, lat, lon)
python main.py --data-source custom --data-path /path/to/dataset.csv --max-images 20000
```

### 3. Train the Model

```bash
# Start training with default configuration
python main.py --data-source custom --data-path data/my_dataset.csv --max-images 10000

# Or with custom configuration
python main.py --config configs/custom_config.yaml --data-source flickr --data-path data/flickr.tsv
```

### 4. Make Predictions

```bash
# Predict location for a single image
python predict.py --model data/models/best_model.pth --data-dir data/processed --image /path/to/photo.jpg

# Save results to JSON
python predict.py --model data/models/best_model.pth --data-dir data/processed --image photo.jpg --output results.json
```

## 📊 Configuration

The system is highly configurable through YAML files. Key parameters:

```yaml
# Model architecture
model:
  backbone: "efficientnet-b4"  # efficientnet-b4, resnet50, vit-base
  embedding_dim: 512
  dropout: 0.2

# Training settings
training:
  batch_size: 32
  learning_rate: 0.001
  num_epochs: 100
  early_stopping_patience: 10

# Geographic clustering
clustering:
  country_clusters: 195
  region_clusters: 1000  
  city_clusters: 10000
  precise_clusters: 100000

# Evaluation thresholds (km)
evaluation:
  distance_thresholds: [1, 25, 200, 750, 2500]
```

## 🔧 Advanced Usage

### Custom Model Architecture

```python
from src.models.geoloc_model import GeolocalizationModel

# Create custom model
model = GeolocalizationModel(
    backbone="resnet50",
    num_classes_dict={
        'country': 195,
        'region': 1000,
        'city': 5000
    },
    embedding_dim=1024,
    dropout=0.3
)
```

### Custom Data Processing

```python
from src.data.dataset import DataCollector, GeoImageDataset

# Custom data collection
collector = DataCollector(config)
df = collector.extract_exif_coordinates("/path/to/images")

# Custom dataset
dataset = GeoImageDataset(df, clustering_info, image_dir, augment=True)
```

### Evaluation and Analysis

```python
from src.models.trainer import GeolocalizationTrainer

# Evaluate model performance
trainer = GeolocalizationTrainer(model, train_loader, val_loader, config, clustering_info)
test_metrics = trainer.evaluate_model(test_loader)

print(f"Mean distance error: {test_metrics['mean_distance_error_km']:.2f} km")
print(f"Accuracy within 25km: {test_metrics['accuracy_25km']*100:.1f}%")
```

## 📈 Performance Expectations

Based on similar research, you can expect:

- **Country-level accuracy**: 85-95% (for distinctive locations)
- **Within 25km**: 60-80% (depending on data quality and size)
- **Within 200km**: 75-90%
- **Median distance error**: 50-200km (varies significantly by region)

Performance depends heavily on:
- Dataset size and diversity
- Geographic distribution of training data
- Distinctiveness of visual features in images
- Quality of ground truth GPS coordinates

## 🗂️ Project Structure

```
geolocalization-ai/
├── configs/
│   └── config.yaml           # Main configuration file
├── src/
│   ├── utils/
│   │   ├── config.py         # Configuration utilities
│   │   ├── logger.py         # Logging setup
│   │   └── geo_utils.py      # Geographic utilities
│   ├── data/
│   │   └── dataset.py        # Data loading and preprocessing
│   ├── models/
│   │   ├── geoloc_model.py   # Main model architecture
│   │   └── trainer.py        # Training loop
│   └── features/
├── data/
│   ├── raw/                  # Raw images and datasets
│   ├── processed/            # Processed data and clustering info
│   └── models/               # Saved model checkpoints
├── notebooks/                # Jupyter notebooks for analysis
├── main.py                   # Main training script
├── predict.py                # Inference script
└── requirements.txt          # Python dependencies
```

## 🎯 Training Tips

1. **Dataset Quality**: Ensure GPS coordinates are accurate and images are representative
2. **Data Diversity**: Include images from different continents, seasons, and environments
3. **Batch Size**: Adjust based on your GPU memory (16-64 typically works well)
4. **Learning Rate**: Start with 1e-3, reduce if loss plateaus
5. **Data Augmentation**: Helps with generalization, especially for smaller datasets
6. **Hierarchical Weights**: Adjust based on your use case (precise vs. coarse location needs)

## 📚 Evaluation Metrics

The system provides comprehensive evaluation:

- **Distance-based Accuracy**: Percentage of predictions within X km of true location
- **Mean/Median Distance Error**: Average error in kilometers
- **Hierarchical Accuracy**: Classification accuracy at country/region/city levels
- **Great Circle Distance**: Accurate distance calculation using Haversine formula

## 🔍 Troubleshooting

### Common Issues

1. **Out of Memory**: Reduce batch size or image resolution
2. **Slow Training**: Enable mixed precision training, check data loading bottlenecks
3. **Poor Accuracy**: Increase dataset size, check data quality, tune hyperparameters
4. **Clustering Errors**: Ensure sufficient geographic diversity in training data

### Performance Optimization

- Use GPU with sufficient VRAM (8GB+ recommended)
- Enable mixed precision training for 40-50% speedup
- Use multiple data loading workers
- Consider gradient checkpointing for larger models

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest features.

## 📖 References

This implementation is inspired by research in:
- PlaNet: A Deep Neural Network for Location Recognition (Weyand et al., 2016)
- Im2GPS: Estimating Geographic Information from a Single Image (Hays & Efros, 2008)
- Geographic Location Recognition using Deep Learning (Multiple recent papers)

## 🏆 Acknowledgments

- YFCC100M dataset for providing geotagged images
- OpenStreetMap for geographic data
- The computer vision and deep learning communities for foundational research

---

For questions, issues, or contributions, please open an issue on GitHub or contact the maintainers.