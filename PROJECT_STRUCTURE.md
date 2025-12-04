# 📁 Project File Structure

## Полный список файлов проекта с описанием

```
BackendMireaCursovaya/
│
├── 📄 README.md                          # Главный readme файл
├── 📄 IMPLEMENTATION.md                  # Описание реализации
├── 📄 SETUP_COMPLETE.md                  # Гайд по интеграции
├── 📄 CHANGES.md                         # Список всех изменений
├── 📄 DEPLOYMENT.md                      # Гайд по deployment
├── 📄 requirements                       # Python зависимости
├── 📄 test_api.py                        # Тестирование API (Python клиент)
├── 📄 .gitignore                         # Git исключения
│
├── 📁 app/                               # Главная папка приложения
│   ├── __init__.py
│   ├── 📄 main.py                        # ⭐ ОБНОВЛЕНО: Точка входа приложения
│   │
│   ├── 📁 entities/                      # Domain models
│   │   ├── __init__.py
│   │   ├── mechanic.py                   # GameMechanic dataclass
│   │   ├── link.py                       # EvolutionLink dataclass
│   │   └── 📄 user.py                    # 🆕 User & EmailToken dataclasses
│   │
│   ├── 📁 use_cases/                     # Business logic
│   │   ├── create_mechanic.py            # Создание механики
│   │   ├── get_tree.py                   # Получение дерева эволюции
│   │   └── 📄 auth.py                    # 🆕 Аутентификация
│   │                                     #    - RegisterUserUseCase
│   │                                     #    - VerifyEmailUseCase
│   │                                     #    - AuthenticateUserUseCase
│   │
│   ├── 📁 interfaces/                    # API & Repositories
│   │   ├── 📁 api/
│   │   │   ├── __init__.py
│   │   │   ├── 📄 dependencies.py        # ⭐ ОБНОВЛЕНО: Dependency injection
│   │   │   │                             #    + get_user_repo
│   │   │   │                             #    + get_email_token_repo
│   │   │   │                             #    + get_current_user
│   │   │   └── 📁 v1/
│   │   │       ├── __init__.py
│   │   │       ├── 📄 routes.py          # ⭐ ОБНОВЛЕНО: Router agregator
│   │   │       ├── schemas.py            # MechanicDTO, LinkDTO
│   │   │       ├── 📄 auth_routes.py     # 🆕 Auth endpoints
│   │   │       │                         #    - POST /auth/register
│   │   │       │                         #    - POST /auth/verify-email
│   │   │       │                         #    - POST /auth/login
│   │   │       │                         #    - GET /auth/me
│   │   │       ├── 📄 auth_schemas.py    # 🆕 Auth Pydantic models
│   │   │       │                         #    - UserRegisterRequest
│   │   │       │                         #    - UserLoginRequest
│   │   │       │                         #    - TokenResponse
│   │   │       └── 📄 mechanics_routes.py # 🆕 Механик endpoints
│   │   │                                 #    - GET/POST /mechanics/
│   │   │                                 #    - GET/POST /mechanics/links
│   │   │                                 #    - GET /mechanics/{id}/tree
│   │   │
│   │   └── 📁 repos/                     # Repository interfaces
│   │       ├── mechanic_repo.py          # IMechanicRepository
│   │       ├── link_repo.py              # ILinkRepository
│   │       └── 📄 user_repo.py           # 🆕 IUserRepository
│   │                                     #    IEmailTokenRepository
│   │
│   └── 📁 infra/                         # Infrastructure
│       ├── __init__.py
│       ├── 📄 config.py                  # ⭐ ОБНОВЛЕНО: Settings (Pydantic v2)
│       ├── 📄 security.py                # 🆕 Password & JWT security
│       ├── 📁 database/
│       │   ├── __init__.py
│       │   ├── 📄 models.py              # ⭐ ОБНОВЛЕНО: SQLAlchemy models
│       │   │                             #    + UserDB
│       │   │                             #    + EmailTokenDB
│       │   ├── engine.py                 # (опционально)
│       │   └── 📄 session.py             # ⭐ ОБНОВЛЕНО: AsyncSession factory
│       │
│       └── 📁 repos_impl/                # Repository implementations
│           ├── __init__.py
│           ├── mechanic_repo_impl.py     # MechanicRepository
│           ├── link_repo_impl.py         # LinkRepository
│           └── 📄 user_repo_impl.py      # 🆕 UserRepository
│                                         #    EmailTokenRepository
│
├── 📁 static/                            # Фронтенд файлы
│   ├── 📄 index.html                     # ⭐ ПЕРЕПИСАН: Регистрация + граф
│   ├── 📄 style.css                      # ⭐ ПЕРЕПИСАН: Современный дизайн
│   └── 📄 script.js                      # ⭐ ПЕРЕПИСАН: Cytoscape + API
│
├── 📁 tests/                             # Тесты
│   ├── conftest.py
│   ├── test_api/
│   │   └── test_mechanics.py
│   └── (можно добавить тесты auth)
│
├── 📁 alembic/                           # Миграции БД (плейсхолдер)
│   └── ...
│
├── 📄 docker-compose.yml                 # Docker конфигурация
├── 📄 Dockerfile                         # Docker образ
└── .env                                  # 🆕 (нужно создать)
                                          #    DB credentials
                                          #    SECRET_KEY
```

---

## 📊 Статистика

### Новые файлы (15)
- app/entities/user.py
- app/infra/security.py
- app/interfaces/repos/user_repo.py
- app/infra/repos_impl/user_repo_impl.py
- app/use_cases/auth.py
- app/interfaces/api/v1/auth_routes.py
- app/interfaces/api/v1/auth_schemas.py
- app/interfaces/api/v1/mechanics_routes.py
- test_api.py
- IMPLEMENTATION.md
- SETUP_COMPLETE.md
- CHANGES.md
- DEPLOYMENT.md
- .env (нужно создать)
- (плюс документация)

### Обновлённые файлы (12)
- app/main.py
- app/infra/config.py
- app/infra/database/models.py
- app/infra/database/session.py
- app/interfaces/api/dependencies.py
- app/interfaces/api/v1/routes.py
- app/interfaces/api/v1/schemas.py
- static/index.html
- static/style.css
- static/script.js
- README.md
- requirements

---

## 🔑 Ключевые компоненты

### Backend (Python/FastAPI)

#### Аутентификация
```
Registration → Verification → Login → JWT Token → Protected Endpoints
```

#### Слои приложения
```
API (routes) 
  ↓
Use Cases (бизнес-логика)
  ↓
Repositories (доступ к данным)
  ↓
Database (PostgreSQL)
```

### Frontend (HTML/CSS/JavaScript)

#### Компоненты UI
```
Auth Section (Регистрация/Логин/Верификация)
  ↓
Main App (после успешного входа)
  ├─ Header (пользователь + logout)
  ├─ Sidebar (управление механиками)
  └─ Graph Container (Cytoscape визуализация)
```

#### API взаимодействие
```
Frontend → HTTP Request → FastAPI Backend
                            ↓
                        Auth Check
                            ↓
                        Business Logic
                            ↓
                        Database Query
                            ↓
                        HTTP Response → Frontend
```

---

## 🔗 Связи между файлами

### Authentication Flow
```
auth_routes.py
    ↓ использует
auth.py (use cases)
    ↓ использует
user_repo_impl.py (repositories)
    ↓ использует
models.py (UserDB, EmailTokenDB)
    ↓ использует
security.py (hash, verify, JWT)
```

### Mechanics Flow
```
mechanics_routes.py
    ↓ использует
create_mechanic.py, get_tree.py (use cases)
    ↓ использует
mechanic_repo_impl.py, link_repo_impl.py
    ↓ использует
models.py (MechanicDB, LinkDB)
```

### Frontend Flow
```
index.html
    ├─ загружает
    ├─ style.css (стили)
    ├─ script.js
    │   ├─ Управление Auth
    │   ├─ API запросы
    │   ├─ Cytoscape граф
    │   └─ Event listeners
    └─ Cytoscape.js (CDN)
```

---

## 📋 Типы файлов

### Python (Backend)
- `main.py` - точка входа
- `entities/` - domain models (dataclasses)
- `use_cases/` - business logic
- `interfaces/` - контракты и API
- `infra/` - низкоуровневые компоненты

### SQL (Database)
- PostgreSQL таблицы (users, email_tokens, mechanics, links)

### Web (Frontend)
- `index.html` - структура страницы
- `style.css` - оформление
- `script.js` - логика и интерактивность
- Cytoscape.js - библиотека для графов

### Documentation
- `.md` файлы - описание проекта и инструкции

---

## 🎯 Точки расширения

### Для добавления новых фич

1. **Новый эндпоинт**
   - Добавить в `routes.py` или создать новый `*_routes.py`
   - Создать `*_schemas.py` для валидации
   - Создать `*_use_case.py` для логики
   - Создать методы в репозитории

2. **Новая таблица БД**
   - Добавить модель в `models.py`
   - Создать интерфейс в `repos/`
   - Создать реализацию в `repos_impl/`

3. **Новый компонент фронтенда**
   - Добавить HTML в `index.html`
   - Добавить CSS в `style.css`
   - Добавить JavaScript функции в `script.js`

---

## 🚀 Развертывание

- `docker-compose.yml` - для локального development
- `Dockerfile` - для production образа
- `DEPLOYMENT.md` - пошаговый гайд

---

**Обновлено:** Декабрь 4, 2024  
**Версия:** 1.0.0
