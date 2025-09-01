# PupRing AI Python Services - Deployment Guide

## 📁 Project Structure

```
pupring-python-services/
├── app.py                          # Main Flask application
├── background_removal_service.py   # Background removal logic
├── vectorization_service.py        # Image vectorization logic
├── run_bg_removal_service.py      # Legacy runner (for reference)
├── filtre_gravure_simple/          # Professional engraving module
│   ├── professional_pet_engraving.py
│   ├── engraving_filter.py
│   └── requirements.txt
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker container configuration
├── docker-compose.yml             # Multi-container orchestration
├── Procfile                        # Heroku deployment configuration
├── vercel.json                     # Vercel deployment configuration
├── railway.json                    # Railway deployment configuration
├── start.sh                        # Local development startup script
├── .env.example                    # Environment variables template
├── .dockerignore                   # Docker ignore patterns
└── README.md                       # Complete documentation
```

## 🚀 Deployment Options

### 1. 🏠 Local Development

**Quick Start:**
```bash
cd pupring-python-services
chmod +x start.sh
./start.sh
```

**Manual Setup:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python app.py
```

**Test the service:**
```bash
curl http://localhost:5001/health
```

### 2. 🐳 Docker Deployment

**Single Container:**
```bash
# Build and run
docker build -t pupring-python-services .
docker run -p 5001:5001 pupring-python-services
```

**Docker Compose (Recommended):**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f pupring-python-services

# Stop services
docker-compose down
```

### 3. ☁️ Heroku Deployment

```bash
# Install Heroku CLI and login
heroku login

# Create new Heroku app
heroku create your-python-services-app

# Set environment variables
heroku config:set PORT=5001 --app your-python-services-app

# Deploy
git add .
git commit -m "Deploy Python services"
git push heroku main

# Scale application
heroku ps:scale web=1 --app your-python-services-app

# View logs
heroku logs --tail --app your-python-services-app
```

**Your service will be available at:**
`https://your-python-services-app.herokuapp.com`

### 4. 🚄 Railway Deployment

1. **Connect Repository:**
   - Go to [railway.app](https://railway.app)
   - Click "Deploy from GitHub repo"
   - Select your `pupring-python-services` repository

2. **Configure Environment:**
   - Railway auto-detects Python applications
   - Set environment variables in dashboard
   - Service deploys automatically on git push

3. **Custom Domain (Optional):**
   - Add custom domain in Railway dashboard
   - Configure DNS settings

### 5. ▲ Vercel Deployment

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from project directory
cd pupring-python-services
vercel --prod

# Follow prompts to configure deployment
```

**Note:** Vercel has limitations for Python ML applications (size, execution time). Consider other platforms for production.

### 6. 🌊 DigitalOcean App Platform

1. **Create App:**
   - Go to DigitalOcean App Platform
   - Connect your GitHub repository
   - Select `pupring-python-services` directory

2. **Configure Build:**
   - Build command: `pip install -r requirements.txt`
   - Run command: `gunicorn --bind 0.0.0.0:$PORT app:app`

3. **Set Environment Variables:**
   ```
   PORT=5001
   FLASK_ENV=production
   ```

### 7. 🏗️ AWS/GCP/Azure

**AWS Elastic Beanstalk:**
```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init
eb create pupring-python-services
eb deploy
```

**Google Cloud Run:**
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT/pupring-python-services
gcloud run deploy --image gcr.io/YOUR_PROJECT/pupring-python-services --platform managed
```

## 🔧 Configuration

### Environment Variables

Create `.env` file or set in your deployment platform:

```bash
# Required
PORT=5001
FLASK_ENV=production
DEBUG=false

# Optional (if using external services)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Performance Tuning

**For Production Deployments:**

1. **Memory Requirements:**
   - Minimum: 1GB RAM
   - Recommended: 2GB+ RAM for better performance

2. **CPU Requirements:**
   - Minimum: 1 vCPU
   - Recommended: 2+ vCPUs for concurrent processing

3. **Gunicorn Configuration:**
```bash
# For 2 CPU cores
gunicorn --workers 4 --timeout 120 --bind 0.0.0.0:$PORT app:app

# For 4 CPU cores  
gunicorn --workers 8 --timeout 120 --bind 0.0.0.0:$PORT app:app
```

## 📊 Monitoring & Health Checks

### Health Check Endpoints

**Basic Health Check:**
```bash
curl https://your-service.com/health
```

**Service Status:**
```bash
curl https://your-service.com/services
```

### Platform-Specific Health Checks

**Docker:**
- Built-in healthcheck in Dockerfile
- Automatic container restart on failures

**Heroku:**
```bash
heroku ps --app your-python-services-app
```

**Railway:**
- Built-in monitoring in dashboard
- Automatic deployments on git push

## 🔗 Integration with Next.js App

Update your Next.js environment variables:

```bash
# .env file in your Next.js app
PYTHON_SERVICE_URL=https://your-python-service.herokuapp.com
PYTHON_API_URL=https://your-python-service.herokuapp.com
NEXT_PUBLIC_PYTHON_API_URL=https://your-python-service.herokuapp.com
```

## 🧪 Testing Your Deployment

### 1. Health Check Test
```bash
curl https://your-service.com/health
```

### 2. Background Removal Test
```bash
curl -X POST https://your-service.com/remove-background \
  -F "image=@test_pet.jpg" \
  -H "Content-Type: multipart/form-data"
```

### 3. Professional Engraving Test
```bash
curl -X POST https://your-service.com/professional-engraving \
  -F "image=@test_pet.jpg"
```

## 🚨 Troubleshooting

### Common Deployment Issues

**Memory Errors:**
- Increase memory allocation in platform settings
- Reduce number of Gunicorn workers

**Timeout Errors:**
- Increase timeout settings
- Optimize image processing parameters

**Port Issues:**
- Ensure PORT environment variable is set correctly
- Check platform-specific port requirements

**Dependencies Issues:**
```bash
# Clear pip cache
pip install --no-cache-dir -r requirements.txt

# Rebuild Docker image
docker build --no-cache -t pupring-python-services .
```

### Platform-Specific Issues

**Heroku:**
- Slug size limits: Remove unnecessary files
- Memory limits: Use hobby or professional dynos

**Vercel:**
- Function size limits: Consider other platforms for ML workloads
- Execution time limits: Optimize processing speed

**Railway:**
- Build timeouts: Increase build timeout in settings
- Resource limits: Monitor usage in dashboard

## 📈 Scaling Considerations

### Horizontal Scaling
- Deploy multiple instances behind load balancer
- Use Redis for shared caching
- Implement request queuing system

### Vertical Scaling
- Increase memory and CPU resources
- Optimize image processing algorithms
- Use GPU instances for faster processing

## 🔒 Security Best Practices

1. **Environment Variables:**
   - Never commit secrets to repository
   - Use platform secret management

2. **File Validation:**
   - Validate uploaded file types
   - Implement file size limits

3. **Rate Limiting:**
   - Implement request rate limiting
   - Monitor for abuse patterns

4. **HTTPS:**
   - Always use HTTPS in production
   - Configure proper CORS settings

---

## 🎉 Deployment Complete!

Your Python services are now ready for independent deployment on any platform. Choose the option that best fits your needs:

- **Development**: Local setup with `./start.sh`
- **Small Scale**: Heroku or Railway
- **Enterprise**: AWS, GCP, or Azure
- **Containerized**: Docker with any container platform

The services will integrate seamlessly with your Next.js application! 🚀