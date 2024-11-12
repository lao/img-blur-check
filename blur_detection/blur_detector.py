"""
Blur detection functionality using the Variance of Laplacian method.
"""
import cv2
import numpy as np
import requests
from typing import Tuple, Optional
from urllib.parse import urlparse

class BlurDetector:
    """A class to detect blur in images using the Variance of Laplacian method."""
    
    def __init__(self, threshold: float = 130.0):
        """
        Initialize the blur detector.
        
        Args:
            threshold (float): The threshold below which an image is considered blurry.
                             Default is 130.0.
        """
        self.threshold = threshold

    def load_image_from_url(self, url: str) -> Optional[np.ndarray]:
        """
        Load an image from a URL.
        
        Args:
            url (str): URL of the image
            
        Returns:
            Optional[np.ndarray]: Image array or None if loading fails
            
        Raises:
            ValueError: If the image cannot be loaded from the URL
        """
        try:
            # Validate URL format
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError("Invalid URL format")

            # Download image
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Convert to numpy array
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            
            if image is None:
                raise ValueError("Failed to decode image")
                
            return image
            
        except Exception as e:
            raise ValueError(f"Failed to load image from URL: {str(e)}")

    def ensure_gray_scale(self, image: np.ndarray) -> np.ndarray:
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

    def compute_blur_metrics(self, image: np.ndarray) -> Tuple[bool, float, float]:
        """
        Compute the blur metrics of an image.
        
        Args:
            image (np.ndarray): Input image array
            
        Returns:
            Tuple[bool, float, float]: (is_blurry, blur_score, blur_percentage)
        """
        # Convert to grayscale if needed
        gray = self.ensure_gray_scale(image)
        
        # Compute Laplacian variance
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        score = laplacian.var()
        
        # Calculate blur percentage (inverted score normalized to 0-100%)
        max_score = self.threshold * 2
        blur_percentage = max(0, min(100, (1 - (score / max_score)) * 100))
        
        return score < self.threshold, score, blur_percentage

    def process_image(self, image_path: str) -> dict:
        """
        Process an image file or URL and determine if it's blurry.
        
        Args:
            image_path (str): Path to image file or URL
            
        Returns:
            dict: Contains blur detection results with keys:
                - path: Original image path or URL
                - is_blurry: Boolean indicating if image is blurry
                - blur_score: Technical score (Laplacian variance)
                - blur_percentage: Blur amount as a percentage
                
        Raises:
            ValueError: If the image cannot be loaded
        """
        # Load image (handles both local paths and URLs)
        if image_path.startswith(('http://', 'https://')):
            image = self.load_image_from_url(image_path)
        else:
            image = cv2.imread(image_path)
            
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")

        # Compute blur metrics
        is_blurry, score, blur_percentage = self.compute_blur_metrics(image)
        
        return {
            'path': image_path,
            'is_blurry': is_blurry,
            'blur_score': score,
            'blur_percentage': blur_percentage
        }

