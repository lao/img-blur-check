"""
Tests for the blur detection functionality.
"""
import pytest
import numpy as np
import cv2
from blur_detection.blur_detector import BlurDetector

@pytest.fixture
def detector():
    """Create a BlurDetector instance for testing."""
    return BlurDetector(threshold=100.0)

def create_test_image(size=100, is_blurry=False):
    """Create a test image with or without blur."""
    # Create a simple pattern
    x = np.linspace(0, 1, size)
    y = np.linspace(0, 1, size)
    xx, yy = np.meshgrid(x, y)
    image = np.sin(2 * np.pi * xx) * np.sin(2 * np.pi * yy) * 255
    image = image.astype(np.uint8)
    
    if is_blurry:
        # Apply Gaussian blur to create a blurry image
        image = cv2.GaussianBlur(image, (15, 15), 0)
    
    return image

def test_blur_detection_sharp():
    """Test that sharp images are correctly identified."""
    detector = BlurDetector(threshold=100.0)
    sharp_image = create_test_image(is_blurry=False)
    
    is_blurry, score = detector.is_blurry(sharp_image)
    assert not is_blurry
    assert score > detector.threshold

def test_blur_detection_blurry():
    """Test that blurry images are correctly identified."""
    detector = BlurDetector(threshold=100.0)
    blurry_image = create_test_image(is_blurry=True)
    
    is_blurry, score = detector.is_blurry(blurry_image)
    assert is_blurry
    assert score < detector.threshold

def test_process_image_annotation():
    """Test that image annotation works correctly."""
    detector = BlurDetector(threshold=100.0)
    image = create_test_image()
    
    _, _, annotated = detector.process_image(
        "dummy_path",
        annotate=True
    )
    
    assert annotated is not None
    assert annotated.shape[2] == 3  # Should be BGR format

def test_invalid_image_path():
    """Test that invalid image paths raise appropriate errors."""
    detector = BlurDetector()
    
    with pytest.raises(ValueError):
        detector.process_image("nonexistent_image.jpg")