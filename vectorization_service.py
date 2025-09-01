import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
from PIL import Image
import svgwrite
from scipy import ndimage
from skimage import feature, filters, morphology
import os
import tempfile
import traceback

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:3001', 'http://localhost:3002'])

def decode_base64_image(base64_string):
    """Decode base64 image string to numpy array"""
    try:
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        img_data = base64.b64decode(base64_string)
        img = Image.open(io.BytesIO(img_data))
        
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        return np.array(img)
    except Exception as e:
        print(f"Error decoding image: {e}")
        raise

def encode_image_to_base64(image_array):
    """Encode numpy array to base64 string"""
    try:
        if len(image_array.shape) == 2:
            img = Image.fromarray(image_array.astype('uint8'), 'L')
        else:
            img = Image.fromarray(image_array.astype('uint8'), 'RGB')
        
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:
        print(f"Error encoding image: {e}")
        raise

def apply_advanced_canny(image, low_threshold=50, high_threshold=150):
    """Apply clean line art style with minimal texture"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    # Apply bilateral filter to reduce noise while keeping edges sharp
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Apply edge detection - Canny gives white edges on black background
    edges = cv2.Canny(filtered, low_threshold, high_threshold)
    
    # Dilate slightly to make lines more visible (still white on black)
    kernel_dilate = np.ones((2,2), np.uint8)
    edges = cv2.dilate(edges, kernel_dilate, iterations=1)
    
    # Invert to get black lines on white background
    result = cv2.bitwise_not(edges)
    
    return result

def create_artistic_edges(image):
    """Create clean artistic line art"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    # Apply Gaussian blur to reduce texture
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Canny for clean edges
    edges = cv2.Canny(blurred, 50, 150)
    
    # Dilate to make lines visible
    kernel = np.ones((2,2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # Invert to get black lines on white
    result = cv2.bitwise_not(edges)
    
    return result

def create_embossed_effect(image):
    """Create clean embossed effect for engraving"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    # Apply bilateral filter for edge-preserving smoothing
    smooth = cv2.bilateralFilter(gray, 15, 80, 80)
    
    # Use Canny for reliable edge detection
    edges = cv2.Canny(smooth, 60, 150)
    
    # Dilate for thicker embossed look
    kernel = np.ones((3,3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # Clean up with morphological operations
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    # Invert to get black lines on white background
    result = cv2.bitwise_not(edges)
    
    return result

def create_detailed_engraving(image):
    """Create clean detailed engraving with more features"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    # Use adaptive threshold for consistent results regardless of input
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, 2)
    
    # Apply edge detection on the adaptive threshold result
    edges = cv2.Canny(adaptive, 50, 150)
    
    # Combine adaptive threshold and edges for more detail
    combined = cv2.bitwise_and(adaptive, cv2.bitwise_not(edges))
    
    # Clean up
    kernel = np.ones((2,2), np.uint8)
    result = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel)
    
    return result
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # Additional cleanup to remove small artifacts
    clean = cv2.medianBlur(clean, 3)
    
    return clean

def create_halftone_pattern(image, dot_size=3):
    """Create clean pattern for engraving"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Canny edge detection
    edges = cv2.Canny(blurred, 60, 140)
    
    # Create stipple effect by finding contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create white background
    output = np.ones_like(gray) * 255
    
    # Draw contours as dots/stipples
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 20:  # Filter out tiny noise
            # Get contour center
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                # Draw small circles for stipple effect
                cv2.circle(output, (cx, cy), dot_size, 0, -1)
    
    # Also draw the main edges
    output = cv2.min(output, cv2.bitwise_not(edges))
    
    return output

def create_crosshatch_pattern(image, line_spacing=3):
    """Create clean crosshatch pattern for engraving"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    # Denoise first
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Get edges
    edges = cv2.Canny(denoised, 50, 150)
    
    # Create crosshatch effect
    kernel_diag1 = np.array([[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1]], np.uint8)
    kernel_diag2 = np.array([[0, 0, 1],
                            [0, 1, 0],
                            [1, 0, 0]], np.uint8)
    
    # Apply diagonal dilations
    diag1 = cv2.dilate(edges, kernel_diag1, iterations=1)
    diag2 = cv2.dilate(edges, kernel_diag2, iterations=1)
    
    # Combine for crosshatch effect
    crosshatch = cv2.bitwise_or(diag1, diag2)
    
    # Invert for black lines on white
    output = cv2.bitwise_not(crosshatch)
    
    return output

def create_standard_engraving(image):
    """Create standard clean engraving - minimal lines, high contrast"""
    print(f"Creating standard engraving...")
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    # Use Sobel edge detection for more reliable results
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Combine Sobel X and Y
    sobel_combined = np.sqrt(sobelx**2 + sobely**2)
    sobel_combined = np.uint8(np.clip(sobel_combined, 0, 255))
    
    # Threshold to get binary edges
    _, edges = cv2.threshold(sobel_combined, 30, 255, cv2.THRESH_BINARY)
    
    # Thin the lines
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    edges = cv2.morphologyEx(edges, cv2.MORPH_ERODE, kernel, iterations=1)
    
    # Invert to get black lines on white
    result = cv2.bitwise_not(edges)
    
    print(f"Standard engraving complete - mean value: {result.mean():.2f}")
    
    return result

def create_bold_engraving(image):
    """Create bold engraving - thicker lines for strong impression"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    
    # Use adaptive threshold first
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 15, 2)
    
    # Find edges
    edges = cv2.Canny(gray, 30, 90)
    
    # Make lines thicker
    kernel = np.ones((3,3), np.uint8)
    thick_edges = cv2.dilate(edges, kernel, iterations=3)
    
    # Combine with adaptive for better coverage
    result = cv2.bitwise_and(adaptive, cv2.bitwise_not(thick_edges))
    
    # Final cleanup
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
    
    return result

def vectorize_to_svg(image_array, output_path=None):
    """Convert binary image to SVG using optimized contours"""
    try:
        # Ensure binary image
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        else:
            gray = image_array
        
        # Invert if needed (we want black lines to trace)
        if np.mean(gray) > 127:
            gray = cv2.bitwise_not(gray)
        
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours with hierarchy
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create SVG
        height, width = binary.shape
        dwg = svgwrite.Drawing(size=(width, height))
        
        # Add white background
        dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill='white'))
        
        # Approximate contours for smoother paths suitable for engraving
        for contour in contours:
            if len(contour) > 2:
                # Simplify curves into smooth paths for engraving
                epsilon = 2  # Fixed epsilon for consistent simplification
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                if len(approx) > 2:
                    points = approx.reshape(-1, 2).tolist()
                    path_data = f"M {points[0][0]},{points[0][1]} "
                    for point in points[1:]:
                        path_data += f"L {point[0]},{point[1]} "
                    path_data += "Z"
                    
                    # Thicker stroke for better engraving visibility
                    dwg.add(dwg.path(d=path_data, fill='none', stroke='black', stroke_width=3))
        
        # Save or return SVG
        if output_path:
            dwg.saveas(output_path)
            with open(output_path, 'r') as f:
                return f.read()
        else:
            return dwg.tostring()
    
    except Exception as e:
        print(f"Error creating SVG: {e}")
        raise

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "vectorization"})

@app.route('/vectorize', methods=['POST'])
def vectorize_image():
    try:
        data = request.json
        image_base64 = data.get('image')
        style = data.get('style', 'canny')
        
        if not image_base64:
            return jsonify({"error": "No image provided"}), 400
        
        # Decode image
        image = decode_base64_image(image_base64)
        
        # Apply different vectorization styles
        result_images = {}
        
        # Always generate the three main styles for the dashboard
        standard_result = create_standard_engraving(image)
        result_images['standard'] = encode_image_to_base64(standard_result)
        
        detailed_result = create_detailed_engraving(image)
        result_images['detailed'] = encode_image_to_base64(detailed_result)
        
        bold_result = create_bold_engraving(image)
        result_images['bold'] = encode_image_to_base64(bold_result)
        
        # Additional styles based on request
        if style == 'all' or style == 'canny':
            canny_result = apply_advanced_canny(image)
            result_images['canny'] = encode_image_to_base64(canny_result)
        
        if style == 'all' or style == 'artistic':
            artistic_result = create_artistic_edges(image)
            result_images['artistic'] = encode_image_to_base64(artistic_result)
        
        if style == 'all' or style == 'embossed':
            embossed_result = create_embossed_effect(image)
            result_images['embossed'] = encode_image_to_base64(embossed_result)
        
        if style == 'all' or style == 'halftone':
            halftone_result = create_halftone_pattern(image)
            result_images['halftone'] = encode_image_to_base64(halftone_result)
        
        if style == 'all' or style == 'crosshatch':
            crosshatch_result = create_crosshatch_pattern(image)
            result_images['crosshatch'] = encode_image_to_base64(crosshatch_result)
        
        # Generate SVG for the primary style
        primary_style = style if style != 'all' else 'standard'
        if primary_style == 'standard':
            svg_input = standard_result
        elif primary_style == 'detailed':
            svg_input = detailed_result
        elif primary_style == 'bold':
            svg_input = bold_result
        elif primary_style == 'canny':
            svg_input = apply_advanced_canny(image)
        elif primary_style == 'artistic':
            svg_input = create_artistic_edges(image)
        else:
            svg_input = standard_result
        
        svg_string = vectorize_to_svg(svg_input)
        
        return jsonify({
            "success": True,
            "styles": result_images,  # Changed from "images" to "styles" to match frontend expectation
            "images": result_images,  # Keep for backward compatibility
            "svg": svg_string,
            "style": style
        })
    
    except Exception as e:
        print(f"Error in vectorization: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/remove-background', methods=['POST'])
def remove_background():
    """Remove background from image using OpenCV"""
    try:
        data = request.json
        image_base64 = data.get('image')
        
        if not image_base64:
            return jsonify({"error": "No image provided"}), 400
        
        # Decode image
        image = decode_base64_image(image_base64)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Apply threshold to create a mask
        _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get the largest contour (assumed to be the main subject)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Create a clean mask from the largest contour
            mask_clean = np.zeros(gray.shape, np.uint8)
            cv2.drawContours(mask_clean, [largest_contour], -1, 255, -1)
            
            # Apply some smoothing to the mask edges
            mask_clean = cv2.GaussianBlur(mask_clean, (5, 5), 0)
            _, mask_clean = cv2.threshold(mask_clean, 128, 255, cv2.THRESH_BINARY)
            
            # Create RGBA image
            if len(image.shape) == 3:
                b, g, r = cv2.split(image)
                rgba = cv2.merge([b, g, r, mask_clean])
            else:
                rgba = cv2.merge([gray, gray, gray, mask_clean])
            
            # Convert to PIL Image for encoding
            img_pil = Image.fromarray(rgba, 'RGBA')
            
            # Save to buffer
            buffered = io.BytesIO()
            img_pil.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            return jsonify({
                "success": True,
                "image": f"data:image/png;base64,{img_base64}",
                "has_transparency": True
            })
        else:
            # If no contours found, return original with white background
            return jsonify({
                "success": True,
                "image": encode_image_to_base64(image),
                "has_transparency": False,
                "message": "No clear subject detected, returning original"
            })
            
    except Exception as e:
        print(f"Error in background removal: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/process-pet', methods=['POST'])
def process_pet_image():
    """Special endpoint for pet image processing with face detection"""
    try:
        data = request.json
        image_base64 = data.get('image')
        
        if not image_base64:
            return jsonify({"error": "No image provided"}), 400
        
        # Decode image
        image = decode_base64_image(image_base64)
        
        # Load pet face cascade (we'll use human face cascade as fallback)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Convert to grayscale for detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Process based on detection
        if len(faces) > 0:
            # Get the largest face
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            
            # Add padding
            padding = int(max(w, h) * 0.2)
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(image.shape[1] - x, w + 2 * padding)
            h = min(image.shape[0] - y, h + 2 * padding)
            
            # Crop to face region
            cropped = image[y:y+h, x:x+w]
        else:
            cropped = image
        
        # Create multiple engraving styles optimized for pets
        results = {}
        
        # Soft edges for fur texture
        soft_edges = cv2.bilateralFilter(cropped, 15, 80, 80)
        soft_edges_gray = cv2.cvtColor(soft_edges, cv2.COLOR_BGR2GRAY) if len(soft_edges.shape) == 3 else soft_edges
        _, soft_binary = cv2.threshold(soft_edges_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        results['soft'] = encode_image_to_base64(soft_binary)
        
        # High contrast for clear features
        contrast = cv2.convertScaleAbs(cropped, alpha=2.0, beta=0)
        contrast_edges = apply_advanced_canny(contrast, 30, 90)
        results['contrast'] = encode_image_to_base64(contrast_edges)
        
        # Artistic style
        artistic = create_artistic_edges(cropped)
        results['artistic'] = encode_image_to_base64(artistic)
        
        # Detailed engraving
        detailed = create_detailed_engraving(cropped)
        results['detailed'] = encode_image_to_base64(detailed)
        
        # Generate SVG
        svg_string = vectorize_to_svg(contrast_edges)
        
        return jsonify({
            "success": True,
            "face_detected": len(faces) > 0,
            "face_coordinates": {"x": int(x), "y": int(y), "width": int(w), "height": int(h)} if len(faces) > 0 else None,
            "styles": results,
            "svg": svg_string
        })
    
    except Exception as e:
        print(f"Error in pet processing: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)