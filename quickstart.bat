@echo off
REM Quick Start Script for Evolution Tree (Windows)

echo 🚀 Evolution Tree - Quick Start
echo ================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    echo 📥 Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed
echo.

REM Build and start containers
echo 🔨 Building and starting containers...
echo This may take a few minutes on first run...
echo.

docker-compose up --build

echo.
echo 🎉 Evolution Tree is running!
echo.
echo 📍 Access points:
echo    Frontend:   http://localhost:3000
echo    Backend:    http://localhost:8000
echo    Docs:       http://localhost:8000/docs
echo    ReDoc:      http://localhost:8000/redoc
echo.
echo 👤 Demo Account:
echo    Email: demo@example.com
echo    Password: Demo123456!
echo.
echo 💡 To stop containers, press Ctrl+C
pause
