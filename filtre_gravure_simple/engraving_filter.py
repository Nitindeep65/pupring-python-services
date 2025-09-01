#!/usr/bin/env python3
"""
Simple Engraving Filter - Black and white engraving style effect
Usage: python engraving_filter.py <image_path>
"""

import cv2
import numpy as np
import sys
import os

def apply_engraving_filter(image_path):
    """
    Apply an engraving style filter to an image with fixed parameters
    """
    
    # Fixed parameters (your preferred settings)
    blur_size = 7      # Reduced from 9 for less blur
    contrast = 0.8
    block_size = 17
    adapt_c = 3.5      # Reduced from 4.5 for more black
    
    try:
        # Display parameters
        print("\n" + "="*50)
        print("ENGRAVING FILTER")
        print("="*50)
        print("\nParameters:")
        print(f"  Blur size: {blur_size}")
        print(f"  Contrast: {contrast}")
        print(f"  Block size: {block_size}")
        print(f"  Adaptive constant: {adapt_c}")
        print("="*50 + "\n")
        
        # 1. Load image
        print(f"Loading: {os.path.basename(image_path)}")
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Unable to load image: {image_path}")
        
        # 2. Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(f"Image size: {gray.shape[1]}x{gray.shape[0]} pixels")
        
        # 3. Apply Gaussian blur
        print("Applying Gaussian blur...")
        if blur_size % 2 == 0:
            blur_size += 1  # Ensure odd
        gray = cv2.GaussianBlur(gray, (blur_size, blur_size), 0)
        
        # 4. Adjust contrast
        print("Adjusting contrast...")
        gray_norm = gray.astype(np.float32) / 255.0
        gray_norm = np.clip((gray_norm - 0.5) * contrast + 0.5, 0, 1)
        gray = (gray_norm * 255).astype(np.uint8)
        
        # 5. Apply adaptive threshold
        print("Applying adaptive threshold...")
        if block_size % 2 == 0:
            block_size += 1  # Ensure odd
        
        binary = cv2.adaptiveThreshold(gray, 255, 
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY_INV,
                                      block_size, adapt_c)
        
        # 6. Invert image
        print("Inverting colors...")
        result = cv2.bitwise_not(binary)
        
        # 7. Save result
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(
            os.path.dirname(__file__) or '.',
            f"{base_name}_filtered.png"
        )
        
        cv2.imwrite(output_path, result)
        print(f"\n[SUCCESS] Saved: {output_path}")
        
        # Display statistics
        white_pixels = np.sum(result == 255)
        black_pixels = np.sum(result == 0)
        total_pixels = result.shape[0] * result.shape[1]
        
        print(f"\nStatistics:")
        print(f"  White pixels: {white_pixels} ({white_pixels/total_pixels*100:.1f}%)")
        print(f"  Black pixels: {black_pixels} ({black_pixels/total_pixels*100:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False

def main():
    """Main function"""
    
    # Check arguments
    if len(sys.argv) < 2:
        print("\nUsage: python engraving_filter.py <image>")
        print("Example: python engraving_filter.py \"dog photo 1.jpg\"")
        sys.exit(1)
    
    # Check if it's a help request
    if sys.argv[1] in ['--help', '-h', 'help', '?']:
        print("""
SIMPLE ENGRAVING FILTER
=======================

Usage:
------
python engraving_filter.py <image>

This applies an engraving effect with the following fixed parameters:
  - Blur size: 7 (less blur, more details)
  - Contrast: 0.8 (soft contrast)
  - Block size: 17 (medium line thickness)
  - Adaptive constant: 3.5 (balanced black/white ratio)

Output:
-------
The filtered image is saved as <original_name>_filtered.png

Example:
--------
python engraving_filter.py "dog photo 1.jpg"
Output: dog photo 1_filtered.png
""")
        sys.exit(0)
    
    # Get image path
    image_path = sys.argv[1].strip('"').strip("'")  # Remove quotes if present
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"\n[ERROR] File not found: {image_path}")
        sys.exit(1)
    
    # Apply filter
    success = apply_engraving_filter(image_path)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()