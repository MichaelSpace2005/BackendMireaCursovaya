# Evolution Tree of Game Mechanics - Full Stack

Интерактивное дерево механик игровых систем с drag-n-drop визуализацией.

**Backend:** FastAPI, SQLAlchemy, PostgreSQL  
**Frontend:** React, Vite, Tailwind CSS, Reactflow

## 🚀 Требования к курсовой работе

✅ Проект собирается без ошибок  
✅ Понятная структура репозитория (Clean Architecture)  
✅ README на GitHub с инструкциями  
✅ Архитектурные схемы (ARCHITECTURE.md)  
✅ Функционал покрыт тестами (TESTING.md)  
✅ **Фронтэнд с drag-n-drop деревом**

## 🎯 Быстрый старт

### Вариант 1: Docker (РЕКОМЕНДУЕТСЯ)

```bash
# Сборка и запуск всего стека
docker-compose up --build

# Доступ:
# Frontend:        http://localhost:3000
# Backend API:     http://localhost:8000
# Swagger Docs:    http://localhost:8000/docs
```

### Вариант 2: Локально (Backend + Frontend отдельно)

**Backend:**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload  # Port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev  # Port 3000
```

## 📁 Структура проекта

```
MireaCursovaya/
├── app/                        # Backend (FastAPI)
│   ├── entities/               # Доменные модели
│   ├── use_cases/              # Бизнес-логика
│   ├── interfaces/
│   │   ├── api/v1/             # REST API
│   │   └── repos/              # Интерфейсы
│   ├── infra/
│   │   ├── repos_impl/         # Реализация
│   │   ├── database/           # SQLAlchemy
│   │   └── security.py         # JWT + Bcrypt
│   └── main.py
├── frontend/                   # Frontend (React)
│   ├── src/
│   │   ├── components/
│   │   │   ├── MechanicsList.jsx      # Drag-n-drop лист
│   │   │   ├── TreeView.jsx           # Canvas визуализация
│   │   │   ├── TreeViewFlow.jsx       # Reactflow визуализация
│   │   │   ├── LinkCreator.jsx        # Создание связей
│   │   │   └── AuthPanel.jsx          # Аутентификация
│   │   ├── store.js            # Zustand состояние
│   │   ├── App.jsx
│   │   └── index.css
│   ├── Dockerfile
│   ├── vite.config.js
│   └── package.json
├── tests/                      # Backend тесты
├── docker-compose.yml          # Оркестрация
├── Dockerfile                  # Backend образ
└── requirements.txt            # Backend зависимости
```

## 🎮 Основные возможности

### Backend API
- **9 endpoints** для управления механиками и связями
- **JWT аутентификация** с bcrypt
- **Валидация** через Pydantic
- **Асинхронность** везде (async/await)
- **Тесты** 39 штук, 80%+ покрытие

### Frontend
- **Drag-n-drop** для механик и связей
- **Две визуализации** дерева:
  - Canvas-based (простая)
  - Reactflow-based (интерактивная, зумируемая)
- **Управление** - создание механик и связей
- **Аутентификация** - регистрация и вход
- **Realtime** обновления состояния

## 📡 API Endpoints

### Mechanics
```
GET    /api/v1/mechanics/           - Список всех механик
POST   /api/v1/mechanics/           - Создать механику (auth)
GET    /api/v1/mechanics/{id}/tree  - Дерево механики
```

### Links
```
GET    /api/v1/mechanics/links      - Список связей
POST   /api/v1/mechanics/links      - Создать связь (auth)
```

### Authentication
```
POST   /api/v1/auth/register        - Регистрация
POST   /api/v1/auth/login           - Вход (JWT)
GET    /api/v1/auth/me              - Профиль (auth)
POST   /api/v1/auth/verify-email    - Email верификация
```

## 🧪 Запуск тестов

```bash
# С Docker
docker-compose exec web pytest tests/ -v

# С отчетом о покрытии
docker-compose exec web pytest tests/ --cov=app --cov-report=html

# Локально
pytest tests/ -v
```

## 📚 Документация

- **ARCHITECTURE.md** - Полная архитектура (backend + frontend)
- **FRONTEND.md** - Документация фронтэнда (React, Zustand, Reactflow)
- **FRONTEND_SETUP.md** - Установка и настройка фронтэнда
- **TESTING.md** - Тестирование: fixtures, примеры, coverage
- **COURSEWORK.md** - Требования курсовой, диаграммы
- **SUBMISSION.md** - Инструкции по сдаче

## 🛠️ Стек технологий

### Backend
- **FastAPI** - Асинхронный web framework
- **SQLAlchemy 2.0** - ORM с поддержкой async
- **PostgreSQL** - Реляционная БД
- **asyncpg** - Асинхронный драйвер
- **Pydantic v2** - Валидация данных
- **python-jose** - JWT токены
- **passlib** - Хеширование паролей
- **pytest** - Тестирование

### Frontend
- **React 18** - UI библиотека
- **Vite 5** - Build tool
- **Tailwind CSS** - Стили
- **Zustand** - State management
- **React Beautiful DND** - Drag-n-drop
- **Reactflow** - Визуализация графов
- **Axios** - HTTP клиент

## 📤 Развертывание

### Production with Docker

```bash
# Build
docker build -t evolution-tree .
docker build -t evolution-tree-frontend frontend/

# Run with docker-compose
docker-compose -f docker-compose.prod.yml up
```

## ❓ Решение проблем

### Ошибка подключения к БД

```bash
# Проверить статус
docker-compose ps

# Посмотреть логи
docker-compose logs postgres
docker-compose logs web
```

### Фронтэнд не подключается к API

```bash
# Проверить что backend запущен
curl http://localhost:8000/health

# Проверить CORS в backend
# Backend автоматически позволяет все источники в dev режиме
```

### Drag-n-drop не работает

```bash
# Переустановить зависимости frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 🎯 Примеры использования

### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "SecurePass123!"
  }'
```

### Создание механики

```bash
# 1. Получить токен
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "SecurePass123!"}' \
  | jq -r '.access_token')

# 2. Создать механику
curl -X POST "http://localhost:8000/api/v1/mechanics/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Combat System",
    "description": "Main combat mechanics",
    "year": 2024
  }'
```

## 📞 Поддержка

- **Frontend помощь**: см. FRONTEND_SETUP.md
- **Backend помощь**: см. ARCHITECTURE.md
- **Тестирование**: см. TESTING.md

## 🎓 Автор

Курсовая работа по программированию бэкенда  
МИРЭА - Российский технологический университет
