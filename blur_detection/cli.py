"""
Command-line interface for blur detection.
"""
import argparse
import json
from imutils import paths
from .blur_detector import BlurDetector

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Detect blur in images")
    
    # Add input source arguments
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "-i", "--images",
        help="path to input directory of images"
    )
    source_group.add_argument(
        "-u", "--url",
        help="URL of a single image to process"
    )
    
    # Add processing arguments
    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=130.0,
        help="focus measures that fall below this value will be considered 'blurry'"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="output results in JSON format"
    )
    
    return parser.parse_args()

def process_directory(detector: BlurDetector, directory: str) -> list:
    """
    Process all images in a directory.
    
    Args:
        detector: BlurDetector instance
        directory: Directory containing images
        
    Returns:
        List of results for each image
    """
    results = []
    
    for image_path in paths.list_images(directory):
        try:
            result = detector.process_image(image_path)
            results.append(result)
        except Exception as e:
            results.append({
                'path': image_path,
                'error': str(e)
            })
            
    return results

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Initialize detector
    detector = BlurDetector(threshold=args.threshold)
    
    try:
        # Process single URL
        if args.url:
            results = [detector.process_image(args.url)]
        # Process directory
        else:
            results = process_directory(detector, args.images)
        
        # Output results
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for result in results:
                if 'error' in result:
                    print(f"\nError processing {result['path']}: {result['error']}")
                    continue
                    
                print(f"\nImage: {result['path']}")
                print(f"Status: {'BLURRY' if result['is_blurry'] else 'SHARP'}")
                print(f"Blur Percentage: {result['blur_percentage']:.1f}%")
                print(f"Technical Score: {result['blur_score']:.2f}")
                
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())