# Simple Engraving Filter

Minimalist Python program to apply a black and white engraving effect to images.

## Installation

```bash
pip install opencv-python numpy
```

## Usage

```bash
python engraving_filter.py "dog photo 1.jpg"
```

The program will:
1. Display the filter parameters being used
2. Process the image step by step
3. Save the result as `<original_name>_filtered.png`

## Parameters

The filter uses these fixed parameters (optimized for best results):

| Parameter | Value | Effect |
|-----------|-------|--------|
| **Blur size** | 9 | Moderate smoothing, preserves details |
| **Contrast** | 0.8 | Soft contrast for natural look |
| **Block size** | 17 | Medium line thickness |
| **Adaptive constant** | 4.5 | Fine lines with more white areas |

## Example Output

```
==================================================
ENGRAVING FILTER
==================================================

Parameters:
  Blur size: 9
  Contrast: 0.8
  Block size: 17
  Adaptive constant: 4.5
==================================================

Loading: dog photo 1.jpg
Image size: 724x720 pixels
Applying Gaussian blur...
Adjusting contrast...
Applying adaptive threshold...
Inverting colors...

[SUCCESS] Saved: dog photo 1_filtered.png

Statistics:
  White pixels: 388556 (74.5%)
  Black pixels: 132724 (25.5%)
```

## How It Works

1. **Grayscale conversion** - Converts color to black and white
2. **Gaussian blur** - Reduces noise while preserving edges
3. **Contrast adjustment** - Fine-tunes light/dark separation
4. **Adaptive thresholding** - Creates pure black/white based on local areas
5. **Color inversion** - Produces the final engraving effect

## Files Included

- `engraving_filter.py` - Main program
- `requirements.txt` - Python dependencies
- `dog photo *.jpg` - Sample images for testing

## Help

```bash
python engraving_filter.py --help
```