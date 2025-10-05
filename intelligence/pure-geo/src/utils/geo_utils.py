"""
Geographic utility functions for coordinate processing and clustering.
"""

import numpy as np
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from typing import Tuple, List, Dict, Any
from sklearn.cluster import KMeans
import pickle


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
        
    Returns:
        Distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    return c * r


def cluster_coordinates(coordinates: List[Tuple[float, float]], 
                       num_clusters: int, 
                       method: str = "kmeans") -> Dict[str, Any]:
    """
    Cluster geographic coordinates into discrete classes.
    
    Args:
        coordinates: List of (lat, lon) tuples
        num_clusters: Number of clusters to create
        method: Clustering method ("kmeans", "hierarchical")
        
    Returns:
        Dictionary containing clustering model and mappings
    """
    coords_array = np.array(coordinates)
    
    if method == "kmeans":
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(coords_array)
        centroids = kmeans.cluster_centers_
        
        # Create mapping from cluster ID to centroid coordinates
        cluster_to_coord = {i: tuple(centroids[i]) for i in range(num_clusters)}
        
        # Create mapping from coordinates to cluster ID
        coord_to_cluster = {}
        for i, coord in enumerate(coordinates):
            coord_to_cluster[coord] = cluster_labels[i]
        
        return {
            "model": kmeans,
            "cluster_to_coord": cluster_to_coord,
            "coord_to_cluster": coord_to_cluster,
            "num_clusters": num_clusters,
            "method": method
        }
    
    else:
        raise NotImplementedError(f"Clustering method '{method}' not implemented")


def coord_to_class(lat: float, lon: float, clustering_info: Dict[str, Any]) -> int:
    """
    Convert geographic coordinates to class label based on clustering.
    
    Args:
        lat, lon: Latitude and longitude
        clustering_info: Clustering information from cluster_coordinates()
        
    Returns:
        Cluster class ID
    """
    if (lat, lon) in clustering_info["coord_to_cluster"]:
        return clustering_info["coord_to_cluster"][(lat, lon)]
    
    # Find nearest cluster centroid for unknown coordinates
    min_distance = float('inf')
    nearest_cluster = 0
    
    for cluster_id, (c_lat, c_lon) in clustering_info["cluster_to_coord"].items():
        distance = haversine_distance(lat, lon, c_lat, c_lon)
        if distance < min_distance:
            min_distance = distance
            nearest_cluster = cluster_id
    
    return nearest_cluster


def class_to_coord(class_id: int, clustering_info: Dict[str, Any]) -> Tuple[float, float]:
    """
    Convert class label back to geographic coordinates.
    
    Args:
        class_id: Cluster class ID
        clustering_info: Clustering information from cluster_coordinates()
        
    Returns:
        (lat, lon) tuple representing cluster centroid
    """
    if class_id in clustering_info["cluster_to_coord"]:
        return clustering_info["cluster_to_coord"][class_id]
    
    raise ValueError(f"Unknown class ID: {class_id}")


def create_hierarchical_clusters(coordinates: List[Tuple[float, float]], 
                                config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create hierarchical geographic clusters (country -> region -> city -> precise).
    
    Args:
        coordinates: List of (lat, lon) tuples
        config: Configuration dictionary with clustering parameters
        
    Returns:
        Dictionary containing all clustering levels
    """
    clustering_config = config['clustering']
    
    hierarchical_clusters = {}
    
    # Create clusters at different geographic scales
    levels = [
        ("country", clustering_config['country_clusters']),
        ("region", clustering_config['region_clusters']),
        ("city", clustering_config['city_clusters']),
        ("precise", clustering_config['precise_clusters'])
    ]
    
    for level_name, num_clusters in levels:
        print(f"Creating {level_name} level clusters ({num_clusters} clusters)...")
        
        # Adjust number of clusters if we have fewer coordinates
        actual_clusters = min(num_clusters, len(set(coordinates)))
        
        cluster_info = cluster_coordinates(
            coordinates, 
            actual_clusters, 
            method=clustering_config['method']
        )
        
        hierarchical_clusters[level_name] = cluster_info
        
    return hierarchical_clusters


def save_clustering_info(clustering_info: Dict[str, Any], filepath: str) -> None:
    """
    Save clustering information to disk.
    
    Args:
        clustering_info: Clustering information dictionary
        filepath: Path to save the clustering info
    """
    with open(filepath, 'wb') as f:
        pickle.dump(clustering_info, f)
    print(f"Clustering information saved to {filepath}")


def load_clustering_info(filepath: str) -> Dict[str, Any]:
    """
    Load clustering information from disk.
    
    Args:
        filepath: Path to the saved clustering info
        
    Returns:
        Clustering information dictionary
    """
    with open(filepath, 'rb') as f:
        clustering_info = pickle.load(f)
    print(f"Clustering information loaded from {filepath}")
    return clustering_info


def calculate_prediction_accuracy(true_coords: List[Tuple[float, float]], 
                                predicted_coords: List[Tuple[float, float]], 
                                distance_thresholds: List[float]) -> Dict[str, float]:
    """
    Calculate accuracy at different distance thresholds.
    
    Args:
        true_coords: List of true (lat, lon) coordinates
        predicted_coords: List of predicted (lat, lon) coordinates
        distance_thresholds: List of distance thresholds in km
        
    Returns:
        Dictionary with accuracy at each threshold
    """
    if len(true_coords) != len(predicted_coords):
        raise ValueError("Length mismatch between true and predicted coordinates")
    
    distances = []
    for true_coord, pred_coord in zip(true_coords, predicted_coords):
        distance = haversine_distance(
            true_coord[0], true_coord[1],
            pred_coord[0], pred_coord[1]
        )
        distances.append(distance)
    
    accuracies = {}
    for threshold in distance_thresholds:
        correct = sum(1 for d in distances if d <= threshold)
        accuracies[f"accuracy_{threshold}km"] = correct / len(distances)
    
    # Add average distance error
    accuracies["mean_distance_error_km"] = np.mean(distances)
    accuracies["median_distance_error_km"] = np.median(distances)
    
    return accuracies