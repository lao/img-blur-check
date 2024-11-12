# Blur Detection

A Python package for detecting and processing blurry images using the Variance of Laplacian method. This tool can process both local images and images from URLs, making it versatile for various use cases.

## Features

- Detect blur in both local images and images from URLs
- Process individual images or entire directories
- Configurable blur threshold
- Option to automatically delete blurry images
- Generate annotated images with blur scores
- Python API for integration into other projects
- Command-line interface for easy use

## Installation

### From PyPI (Recommended)

```bash
pip install blur-detection
```

### From Source

```bash
git clone https://github.com/yourusername/blur_detection.git
cd blur_detection
pip install -e .
```

## Usage

### Command Line Interface

1. Process a single image from URL:
```bash
detect-blur -u https://example.com/image.jpg -t 130.0 -o output_directory
```

2. Process all images in a directory:
```bash
detect-blur -i /path/to/images -t 130.0 -o output_directory
```

3. Process and delete blurry images:
```bash
detect-blur -i /path/to/images -t 130.0 -d
```

### Python API

```python
from blur_detection import BlurDetector

# Initialize detector
detector = BlurDetector(threshold=130.0)

# Process a local image
is_blurry, score, annotated_image = detector.process_image(
    "path/to/image.jpg",
    annotate=True
)

# Process an image from URL
is_blurry, score, annotated_image = detector.process_image(
    "https://example.com/image.jpg",
    annotate=True
)

# Print results
print(f"Image is {'blurry' if is_blurry else 'not blurry'}")
print(f"Blur score: {score}")
```

## Command Line Arguments

- `-i, --images`: Path to input directory of images
- `-u, --url`: URL of a single image to process
- `-t, --threshold`: Blur threshold (default: 130.0)
- `-d, --delete`: Delete images detected as blurry
- `-o, --output`: Output directory for annotated images

## How It Works

The blur detection is based on the Variance of Laplacian method:

1. Convert the image to grayscale
2. Compute the Laplacian to get the second derivative of the image
3. Calculate the variance of the Laplacian
4. Compare the variance against a threshold:
   - Lower variance = more blurry
   - Higher variance = less blurry

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Running Tests

```bash
pip install pytest
pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on the Variance of Laplacian method for blur detection
- Uses OpenCV for image processing
- Inspired by various blur detection techniques in computer vision
