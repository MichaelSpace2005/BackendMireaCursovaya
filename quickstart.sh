#!/bin/bash
# Quick Start Script for Evolution Tree

echo "🚀 Evolution Tree - Quick Start"
echo "================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "📥 Download from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Build and start containers
echo "🔨 Building and starting containers..."
echo "This may take a few minutes on first run..."
echo ""

docker-compose up --build

echo ""
echo "🎉 Evolution Tree is running!"
echo ""
echo "📍 Access points:"
echo "   Frontend:   http://localhost:3000"
echo "   Backend:    http://localhost:8000"
echo "   Docs:       http://localhost:8000/docs"
echo "   ReDoc:      http://localhost:8000/redoc"
echo ""
echo "👤 Demo Account:"
echo "   Email: demo@example.com"
echo "   Password: Demo123456!"
echo ""
echo "💡 To stop containers, press Ctrl+C"
