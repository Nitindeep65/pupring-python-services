"""
PupRing AI Python Services - Minimal Version for Railway
Basic Flask application without heavy ML dependencies
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import tempfile
import traceback
from PIL import Image
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
PORT = int(os.environ.get('PORT', 5001))
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'

@app.route('/', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PupRing AI Python Services',
        'version': '1.0.0-minimal',
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            '/health': 'Health check',
            '/remove-background': 'Basic background processing',
            '/professional-engraving': 'Basic engraving processing',
            '/services': 'List available services'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Detailed health check"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'basic_processing': 'available',
            'image_optimization': 'available'
        },
        'system': {
            'python_version': sys.version,
            'flask_port': PORT,
            'debug_mode': DEBUG
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/services', methods=['GET'])
def list_services():
    """List all available services"""
    return jsonify({
        'available_services': [
            {
                'name': 'Basic Background Processing',
                'endpoint': '/remove-background',
                'method': 'POST',
                'description': 'Basic image processing for background removal',
                'status': 'available'
            },
            {
                'name': 'Basic Engraving Processing',
                'endpoint': '/professional-engraving',
                'method': 'POST',
                'description': 'Basic engraving processing',
                'status': 'available'
            }
        ]
    })

@app.route('/remove-background', methods=['POST'])
def remove_background():
    """Basic background processing endpoint"""
    try:
        logger.info("Background processing request received")
        
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # For now, return the original image (basic processing)
        # This can be enhanced once Railway deployment is working
        return jsonify({
            'success': True,
            'message': 'Basic processing completed',
            'method': 'basic',
            'processedUrl': 'https://via.placeholder.com/400x400.png?text=Processed+Image',
            'processingTime': 2.0,
            'note': 'This is a basic version - full AI processing will be added after successful deployment'
        })
        
    except Exception as e:
        logger.error(f"Background processing error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Processing service error',
            'details': str(e)
        }), 500

@app.route('/professional-engraving', methods=['POST'])
def professional_engraving():
    """Basic engraving processing endpoint"""
    try:
        logger.info("Engraving processing request received")
        
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Basic image processing with Pillow
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                file.save(temp_file.name)
                temp_path = temp_file.name
            
            # Basic processing with Pillow
            with Image.open(temp_path) as img:
                # Convert to grayscale for basic engraving effect
                grayscale = img.convert('L')
                
                # For now, return a placeholder
                # This demonstrates the endpoint is working
                return jsonify({
                    'success': True,
                    'engravingUrl': 'https://via.placeholder.com/400x400.png?text=Engraved+Image',
                    'style': 'basic',
                    'method': 'pillow-basic',
                    'processingTime': 1.5,
                    'dimensions': {
                        'width': img.width,
                        'height': img.height
                    },
                    'note': 'Basic processing completed - full AI engraving will be added after successful deployment'
                })
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        logger.error(f"Engraving processing error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Engraving service error', 
            'details': str(e)
        }), 500

@app.route('/vectorize', methods=['POST'])
def vectorize():
    """Basic vectorization endpoint"""
    try:
        logger.info("Vectorization request received")
        
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        # Basic response for now
        return jsonify({
            'success': True,
            'vectorizedUrl': 'https://via.placeholder.com/400x400.svg?text=Vectorized',
            'format': 'svg',
            'method': 'basic',
            'processingTime': 1.0,
            'note': 'Basic vectorization - advanced features will be added after deployment'
        })
        
    except Exception as e:
        logger.error(f"Vectorization error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Vectorization service error',
            'details': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/', '/health', '/services', '/remove-background', 
            '/professional-engraving', '/vectorize'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'Please check the logs for more details'
    }), 500

if __name__ == '__main__':
    logger.info(f"Starting PupRing AI Python Services (Minimal) on port {PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    
    # Print available endpoints
    logger.info("Available endpoints:")
    logger.info("  GET  / - Health check")
    logger.info("  GET  /health - Detailed health check")
    logger.info("  GET  /services - List all services")
    logger.info("  POST /remove-background - Basic background processing")
    logger.info("  POST /professional-engraving - Basic engraving processing")
    logger.info("  POST /vectorize - Basic vectorization")
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG,
        use_reloader=False
    )