"""
PupRing AI Python Services
Combined Flask application serving multiple AI endpoints
"""

import os
import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import logging
from datetime import datetime
import tempfile
import traceback

# Import individual services
from background_removal_service import remove_background_endpoint
from vectorization_service import vectorize_image_endpoint
from filtre_gravure_simple.professional_pet_engraving import create_professional_engraving

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
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PupRing AI Python Services',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            '/health': 'Health check',
            '/remove-background': 'Background removal service',
            '/vectorize': 'Image vectorization service', 
            '/professional-engraving': 'Professional pet engraving filter',
            '/services': 'List all available services'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Detailed health check"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'background_removal': 'available',
            'vectorization': 'available',
            'professional_engraving': 'available'
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
                'name': 'Background Removal',
                'endpoint': '/remove-background',
                'method': 'POST',
                'description': 'Remove background from pet images using AI',
                'input': 'multipart/form-data with image file',
                'output': 'JSON with processed image URL'
            },
            {
                'name': 'Image Vectorization',
                'endpoint': '/vectorize',
                'method': 'POST', 
                'description': 'Convert images to vector format',
                'input': 'multipart/form-data with image file',
                'output': 'JSON with vectorized image URL'
            },
            {
                'name': 'Professional Engraving',
                'endpoint': '/professional-engraving',
                'method': 'POST',
                'description': 'Create professional pet engraving from image',
                'input': 'multipart/form-data with image file',
                'output': 'JSON with engraved image URL'
            }
        ]
    })

@app.route('/remove-background', methods=['POST'])
def remove_background():
    """Background removal endpoint"""
    try:
        logger.info("Background removal request received")
        return remove_background_endpoint()
    except Exception as e:
        logger.error(f"Background removal error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Background removal service error',
            'details': str(e)
        }), 500

@app.route('/vectorize', methods=['POST'])
def vectorize():
    """Vectorization endpoint"""
    try:
        logger.info("Vectorization request received")
        return vectorize_image_endpoint()
    except Exception as e:
        logger.error(f"Vectorization error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Vectorization service error',
            'details': str(e)
        }), 500

@app.route('/professional-engraving', methods=['POST'])
def professional_engraving():
    """Professional engraving endpoint"""
    try:
        logger.info("Professional engraving request received")
        
        # Check if file is in request
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
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Process with professional engraving
            result = create_professional_engraving(temp_path)
            return jsonify(result)
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        logger.error(f"Professional engraving error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Professional engraving service error',
            'details': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/health', '/services', '/remove-background', 
            '/vectorize', '/professional-engraving'
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
    logger.info(f"Starting PupRing AI Python Services on port {PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    
    # Print available endpoints
    logger.info("Available endpoints:")
    logger.info("  GET  / - Health check")
    logger.info("  GET  /health - Detailed health check")
    logger.info("  GET  /services - List all services")
    logger.info("  POST /remove-background - Background removal")
    logger.info("  POST /vectorize - Image vectorization")
    logger.info("  POST /professional-engraving - Professional engraving")
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG,
        use_reloader=False  # Avoid issues in production
    )