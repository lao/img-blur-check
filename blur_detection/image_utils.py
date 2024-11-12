"""
Utility functions for image handling and processing.
"""
import cv2
import numpy as np
import requests
from typing import Optional

def load_image_from_url(url: str) -> Optional[np.ndarray]:
    """
    Load an image from a URL.
    
    Args:
        url (str): URL of the image
        
    Returns:
        Optional[np.ndarray]: Image array or None if loading fails
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        image_array = np.asarray(bytearray(resp.content), dtype=np.uint8)
        return cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    except Exception as e:
        raise ValueError(f"Failed to load image from URL: {str(e)}")

def ensure_gray_scale(image: np.ndarray) -> np.ndarray:
    """
    Ensure an image is in grayscale format.
    
    Args:
        image (np.ndarray): Input image array
        
    Returns:
        np.ndarray: Grayscale image array
    """
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def save_image(image: np.ndarray, path: str) -> None:
    """
    Save an image to disk.
    
    Args:
        image (np.ndarray): Image array to save
        path (str): Path where to save the image
    """
    cv2.imwrite(path, image)