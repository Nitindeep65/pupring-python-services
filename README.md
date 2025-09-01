# PupRing AI Python Services

A standalone Python microservice providing AI-powered image processing capabilities for pet engraving applications.

## 🚀 Features

- **Background Removal**: AI-powered background removal using advanced models
- **Image Vectorization**: Convert raster images to vector formats
- **Professional Engraving**: Create professional pet engravings from photos
- **Health Monitoring**: Built-in health checks and service status endpoints
- **Multi-Platform Deployment**: Docker, Heroku, Railway, Vercel support

## 📋 Services Overview

### 1. Background Removal Service
- **Endpoint**: `POST /remove-background`
- **Description**: Remove backgrounds from pet images using AI
- **Input**: Image file (JPEG, PNG)
- **Output**: Processed image with transparent background

### 2. Vectorization Service  
- **Endpoint**: `POST /vectorize`
- **Description**: Convert raster images to vector formats
- **Input**: Image file
- **Output**: Vectorized image data

### 3. Professional Engraving Service
- **Endpoint**: `POST /professional-engraving`
- **Description**: Create professional pet engravings
- **Input**: Pet photo
- **Output**: High-quality engraved image

## 🛠️ Installation & Setup

### Local Development

1. **Clone the repository**:
```bash
git clone <repository-url>
cd pupring-python-services
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the service**:
```bash
python app.py
```

The service will start on `http://localhost:5001`

### Environment Variables

```bash
PORT=5001                    # Service port (default: 5001)
DEBUG=false                  # Debug mode (default: false)
FLASK_ENV=production         # Flask environment
```

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build the image
docker build -t pupring-python-services .

# Run the container
docker run -p 5001:5001 pupring-python-services
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Cloud Deployment

### Deploy to Heroku

1. **Install Heroku CLI** and login:
```bash
heroku login
```

2. **Create Heroku app**:
```bash
heroku create pupring-python-services
```

3. **Deploy**:
```bash
git push heroku main
```

4. **Scale the application**:
```bash
heroku ps:scale web=1
```

### Deploy to Railway

1. **Connect to Railway**:
   - Visit [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Railway will auto-detect the Python application

2. **Configure environment**:
   - Set environment variables in Railway dashboard
   - The service will auto-deploy on git push

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## 📡 API Documentation

### Health Check Endpoints

#### GET /
Basic health check
```json
{
  "status": "healthy",
  "service": "PupRing AI Python Services",
  "version": "1.0.0",
  "timestamp": "2025-01-01T00:00:00.000Z"
}
```

#### GET /health
Detailed health check
```json
{
  "status": "healthy",
  "services": {
    "background_removal": "available",
    "vectorization": "available", 
    "professional_engraving": "available"
  },
  "system": {
    "python_version": "3.11.0",
    "flask_port": 5001
  }
}
```

#### GET /services
List all available services
```json
{
  "available_services": [
    {
      "name": "Background Removal",
      "endpoint": "/remove-background",
      "method": "POST"
    }
  ]
}
```

### Processing Endpoints

#### POST /remove-background
Remove background from images

**Request**:
```bash
curl -X POST http://localhost:5001/remove-background \
  -F "image=@pet_photo.jpg"
```

**Response**:
```json
{
  "success": true,
  "processedUrl": "https://cloudinary.com/processed_image.png",
  "method": "rembg",
  "processingTime": 2.5
}
```

#### POST /vectorize
Convert image to vector format

**Request**:
```bash
curl -X POST http://localhost:5001/vectorize \
  -F "image=@pet_photo.jpg"
```

#### POST /professional-engraving
Create professional engraving

**Request**:
```bash
curl -X POST http://localhost:5001/professional-engraving \
  -F "image=@pet_photo.jpg"
```

**Response**:
```json
{
  "success": true,
  "engravingUrl": "https://cloudinary.com/engraved_image.png",
  "style": "professional",
  "processingTime": 5.2
}
```

## 🔧 Configuration

### Performance Tuning

For production deployments, adjust these settings:

```bash
# Gunicorn workers (CPU cores * 2 + 1)
gunicorn --workers 4 --timeout 120 app:app

# Memory limits for Docker
docker run -m 2g pupring-python-services
```

### Scaling Considerations

- **Memory**: Each worker needs ~512MB-1GB RAM
- **CPU**: Image processing is CPU-intensive
- **Storage**: Temporary files need disk space
- **Timeout**: Set appropriate timeouts for large images

## 📊 Monitoring

### Health Checks

The service includes built-in health checks:
- HTTP endpoint: `GET /health`
- Docker healthcheck: Automatic container monitoring
- Process monitoring: Gunicorn worker management

### Logging

Logs are structured and include:
- Request IDs for tracing
- Processing times
- Error details with stack traces
- Service status updates

```bash
# View logs in Docker
docker logs pupring-python-services

# View logs in production
heroku logs --tail -a pupring-python-services
```

## 🚨 Troubleshooting

### Common Issues

**Port already in use**:
```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9
```

**Out of memory**:
- Reduce number of workers
- Increase container memory limit
- Optimize image processing parameters

**Slow processing**:
- Use GPU-enabled instances
- Implement image preprocessing
- Add caching layer

**Dependencies issues**:
```bash
# Rebuild with no cache
pip install --no-cache-dir -r requirements.txt

# Or with Docker
docker build --no-cache -t pupring-python-services .
```

### Error Codes

- `400`: Bad request (missing/invalid image)
- `500`: Internal server error (processing failed)
- `503`: Service unavailable (overloaded)

## 🔒 Security

### Best Practices

1. **File validation**: Only accept valid image formats
2. **Size limits**: Limit upload file sizes
3. **Temporary cleanup**: Auto-delete processed files
4. **Rate limiting**: Implement request rate limits
5. **CORS**: Configure appropriate CORS policies

### Production Security

```python
# Add to app.py for production
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
```

## 📈 Performance Benchmarks

| Operation | Average Time | Memory Usage |
|-----------|--------------|--------------|
| Background Removal | 2-5s | ~800MB |
| Vectorization | 1-3s | ~400MB |
| Professional Engraving | 3-8s | ~1.2GB |

*Benchmarks on 4-core CPU, 8GB RAM*

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit pull request

## 📄 License

This project is part of the PupRing AI system. All rights reserved.

## 📞 Support

For technical support:
- Check logs for detailed error messages
- Verify all dependencies are installed
- Test with the health check endpoints
- Contact the development team with specific error details

---

🎉 **Your Python services are ready to deploy independently!**