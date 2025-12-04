#!/bin/bash
# 🚀 Evolution Tree - Quick Start Script
# Скрипт для быстрого запуска проекта

set -e

echo "🚀 Evolution Tree Backend - Quick Start"
echo "========================================"
echo ""

# Проверить Python
echo "📌 Проверка Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен. Пожалуйста, установите Python 3.9+"
    exit 1
fi
echo "✅ Python $(python3 --version | awk '{print $2}') найден"

# Проверить PostgreSQL
echo ""
echo "📌 Проверка PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL не найден. Для production используйте БД."
    echo "   Для development можно использовать docker-compose:"
    echo "   docker-compose up -d db"
else
    echo "✅ PostgreSQL найден"
fi

# Создать виртуальное окружение
echo ""
echo "📌 Создание виртуального окружения..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Окружение создано"
else
    echo "✅ Окружение уже существует"
fi

# Активировать окружение
echo ""
echo "📌 Активация окружения..."
source venv/bin/activate
echo "✅ Окружение активировано"

# Установить зависимости
echo ""
echo "📌 Установка зависимостей..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements > /dev/null 2>&1
echo "✅ Зависимости установлены"

# Создать .env файл если его нет
echo ""
echo "📌 Проверка конфигурации..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Database Configuration
DB_USER=postgres
DB_PASS=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=evolution_db
DEBUG=True

# Security (для production измените!)
SECRET_KEY=dev-secret-key-change-in-production

# Email (для отправки верификационных писем)
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=your-email@gmail.com
# SMTP_PASSWORD=your-app-password
EOF
    echo "✅ Файл .env создан с настройками по умолчанию"
else
    echo "✅ Файл .env уже существует"
fi

# Информация о БД
echo ""
echo "📌 Информация о базе данных..."
echo "   Убедитесь, что PostgreSQL запущен и доступен:"
echo "   - Host: localhost"
echo "   - Port: 5432"
echo "   - User: postgres"
echo "   - Password: postgres"
echo "   - Database: evolution_db"
echo ""
echo "   Если БД не готова, запустите:"
echo "   $ docker-compose up -d db"
echo ""

# Показать инструкции по запуску
echo "========================================"
echo "✨ Подготовка завершена!"
echo "========================================"
echo ""
echo "🚀 Для запуска приложения выполните:"
echo ""
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "📂 Затем откройте в браузере:"
echo "   http://localhost:8000"
echo ""
echo "📚 Документация:"
echo "   - README.md - Общая информация"
echo "   - IMPLEMENTATION.md - Описание реализации"
echo "   - DEPLOYMENT.md - Гайд по развертыванию"
echo "   - PROJECT_STRUCTURE.md - Структура проекта"
echo ""
echo "🧪 Для тестирования API:"
echo "   python test_api.py"
echo ""
echo "========================================"
