#!/bin/bash

echo "🚀 Deploying PupRing Python Services to Railway (Minimal Version)"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ] || [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the pupring-python-services directory"
    exit 1
fi

echo "📋 Checking deployment files..."
echo "✅ app.py (minimal version)"
echo "✅ requirements.txt (6 lightweight packages)"
echo "✅ Procfile (gunicorn configuration)"
echo "✅ railway.toml (Railway configuration)"

echo ""
echo "📦 Current requirements:"
cat requirements.txt
echo ""

echo "🔧 Verifying git status..."
git status --porcelain

echo ""
echo "📤 Deploying to Railway..."

# Add all changes
git add .

# Commit with timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "Deploy minimal version to Railway - $TIMESTAMP"

# Push to Railway
echo "🚀 Pushing to Railway..."
git push origin main

echo ""
echo "✅ Deployment triggered!"
echo ""
echo "📊 Monitor deployment:"
echo "1. Go to Railway dashboard"
echo "2. Watch the deployment progress"
echo "3. Should complete in 1-2 minutes"
echo ""
echo "🧪 After deployment, test with:"
echo "curl https://your-railway-url.up.railway.app/health"
echo ""
echo "🎯 Expected response:"
echo '{"status": "healthy", "service": "PupRing AI Python Services"}'
echo ""
echo "🔗 Once successful, update your frontend environment variables:"
echo "PYTHON_SERVICE_URL=https://your-railway-url.up.railway.app"
echo ""
echo "🎉 Good luck with deployment!"