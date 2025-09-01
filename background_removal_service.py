#!/usr/bin/env python3
import os
import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import io
import base64
from rembg import remove
import logging

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:3001'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'background-removal',
        'version': '1.0.0'
    })

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        image_data = data['image']
        if image_data.startswith('data:'):
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        input_image = Image.open(io.BytesIO(image_bytes))
        
        if input_image.mode != 'RGBA':
            input_image = input_image.convert('RGBA')
        
        output_image = remove(input_image)
        
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        
        output_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{output_base64}',
            'width': output_image.width,
            'height': output_image.height
        })
        
    except Exception as e:
        logger.error(f"Error removing background: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    logger.info(f"Starting Background Removal Service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)