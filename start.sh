#!/bin/bash

# PupRing AI Python Services Startup Script

echo "🚀 Starting PupRing AI Python Services..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if port is available
PORT=${PORT:-5001}
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port $PORT is already in use. Please free the port or set a different PORT environment variable."
    exit 1
fi

# Start the service
echo "🎯 Starting service on port $PORT..."
echo "📍 Health check: http://localhost:$PORT/health"
echo "📖 API docs: http://localhost:$PORT/services"
echo ""
echo "Press Ctrl+C to stop the service"
echo ""

python app.py