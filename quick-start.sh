#!/bin/bash
# Evolution Tree - Quick Start Script
# Скрипт для быстрого запуска проекта

set -e

echo "Evolution Tree Backend - Quick Start"
echo "========================================"
echo ""

echo "Проверка Python..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 не установлен. Пожалуйста, установите Python 3.9+"
    exit 1
fi
echo "Python $(python3 --version | awk '{print $2}') найден"

echo ""
echo "Проверка PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL не найден. Для production используйте БД."
    echo "Для development можно использовать docker-compose: docker-compose up -d db"
else
    echo "PostgreSQL найден"
fi

echo ""
echo "Создание виртуального окружения..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Окружение создано"
else
    echo "Окружение уже существует"
fi

echo ""
echo "Активация окружения..."
source venv/bin/activate

echo ""
echo "Установка зависимостей..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements > /dev/null 2>&1

echo ""
echo "Проверка конфигурации..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
DB_USER=postgres
DB_PASS=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=evolution_db
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
EOF
    echo "Файл .env создан"
else
    echo "Файл .env уже существует"
fi

echo ""
echo "Информация о базе данных:"
echo "Host: localhost"
echo "Port: 5432"
echo "User: postgres"
echo "Password: postgres"
echo "Database: evolution_db"

echo ""
echo "Готово. Для запуска:"
echo "source venv/bin/activate"
echo "uvicorn app.main:app --reload"

echo "Документация: README.md, IMPLEMENTATION.md, DEPLOYMENT.md, PROJECT_STRUCTURE.md"
echo "Для тестов: python test_api.py"
