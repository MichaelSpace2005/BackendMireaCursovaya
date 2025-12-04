# 📚 Documentation Index

Полный индекс документации проекта Evolution Tree

---

## 🚀 Быстрый старт

### Для новых пользователей
1. **[README.md](README.md)** - Начните отсюда! Общая информация и инструкции
2. **[quick-start.sh](quick-start.sh)** - Скрипт для быстрого запуска

### Для разработчиков
1. **[IMPLEMENTATION.md](IMPLEMENTATION.md)** - Как это реализовано
2. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Структура файлов
3. **[CHANGES.md](CHANGES.md)** - Что было изменено

---

## 📖 Полная документация

### Основная документация
| Файл | Описание |
|------|---------|
| [README.md](README.md) | 📄 Главный файл проекта, инструкции по запуску |
| [IMPLEMENTATION.md](IMPLEMENTATION.md) | 🔧 Техническое описание реализации |
| [SETUP_COMPLETE.md](SETUP_COMPLETE.md) | 📋 Полный гайд по интеграции компонентов |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | 📁 Подробная структура файлов проекта |

### Для операционной деятельности
| Файл | Описание |
|------|---------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | 🚀 Инструкции по развертыванию на production |
| [CHANGES.md](CHANGES.md) | 📝 Полный список всех изменений и улучшений |
| [COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md) | ✅ Резюме завершения проекта |
| [FINAL_CHECKLIST.md](FINAL_CHECKLIST.md) | ✓ Финальный чек-лист всех компонентов |

### Дополнительные материалы
| Файл | Описание |
|------|---------|
| [test_api.py](test_api.py) | 🧪 Python клиент для тестирования API |
| [quick-start.sh](quick-start.sh) | ⚡ Bash скрипт для быстрого старта |

---

## 🎯 Поиск нужной информации

### "Как начать работать с проектом?"
→ Прочитайте [README.md](README.md) и запустите [quick-start.sh](quick-start.sh)

### "Как устроен код?"
→ Посмотрите [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) и [IMPLEMENTATION.md](IMPLEMENTATION.md)

### "Как развернуть на production?"
→ Следуйте инструкциям в [DEPLOYMENT.md](DEPLOYMENT.md)

### "Какие изменения были сделаны?"
→ Смотрите [CHANGES.md](CHANGES.md)

### "Что нужно проверить перед релизом?"
→ Используйте [FINAL_CHECKLIST.md](FINAL_CHECKLIST.md)

### "Как тестировать API?"
→ Запустите [test_api.py](test_api.py)

### "Что было завершено?"
→ Прочитайте [COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md)

---

## 📊 Файлы по типам

### Python Code
- `app/main.py` - Точка входа
- `app/entities/user.py` - User models
- `app/use_cases/auth.py` - Authentication logic
- `app/interfaces/api/v1/auth_routes.py` - Auth endpoints
- `app/infra/security.py` - Security utilities
- `app/infra/repos_impl/user_repo_impl.py` - User repository
- `test_api.py` - API testing client

### Frontend Code
- `static/index.html` - HTML структура
- `static/style.css` - Стили и дизайн
- `static/script.js` - Логика и интерактивность

### Configuration
- `requirements` - Python зависимости
- `docker-compose.yml` - Docker конфигурация
- `Dockerfile` - Docker образ

### Documentation
- `README.md` - Главный readme
- `IMPLEMENTATION.md` - Техническое описание
- `SETUP_COMPLETE.md` - Гайд по интеграции
- `CHANGES.md` - Список изменений
- `DEPLOYMENT.md` - Гайд по deployment
- `PROJECT_STRUCTURE.md` - Структура проекта
- `COMPLETION_SUMMARY.md` - Резюме завершения
- `FINAL_CHECKLIST.md` - Чек-лист
- `INDEX.md` - Этот файл

---

## 🔍 Быстрые ссылки

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

### Endpoints
```
GET  /                              - Home
POST /api/v1/auth/register         - Регистрация
POST /api/v1/auth/verify-email     - Верификация
POST /api/v1/auth/login            - Вход
GET  /api/v1/auth/me               - Текущий пользователь
GET  /api/v1/mechanics/            - Список механик
POST /api/v1/mechanics/            - Создать механику
GET  /api/v1/mechanics/links       - Список связей
POST /api/v1/mechanics/links       - Создать связь
GET  /api/v1/mechanics/{id}/tree   - Дерево механики
```

### Frontend
```
http://localhost:8000/                    - Главная страница
http://localhost:8000/static/             - Статические файлы
```

---

## 📝 Структура документации

```
INDEX.md (этот файл)
├─ Быстрый старт
│  ├─ README.md
│  └─ quick-start.sh
│
├─ Полная документация
│  ├─ Основная
│  │  ├─ README.md
│  │  ├─ IMPLEMENTATION.md
│  │  ├─ SETUP_COMPLETE.md
│  │  └─ PROJECT_STRUCTURE.md
│  │
│  ├─ Операционная
│  │  ├─ DEPLOYMENT.md
│  │  ├─ CHANGES.md
│  │  ├─ COMPLETION_SUMMARY.md
│  │  └─ FINAL_CHECKLIST.md
│  │
│  └─ Тестирование
│     └─ test_api.py
│
└─ Ресурсы
   ├─ GitHub Repository
   ├─ Swagger API Docs
   └─ Frontend Interface
```

---

## 🎓 Образовательные материалы

### Архитектура
- Clean Architecture в Python: [IMPLEMENTATION.md](IMPLEMENTATION.md#архитектура)
- Repository Pattern: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md#repository-pattern)

### Безопасность
- JWT токены: [IMPLEMENTATION.md](IMPLEMENTATION.md#безопасность)
- Password Hashing: [security.py](app/infra/security.py)

### Best Practices
- Code organization: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- API design: [IMPLEMENTATION.md](IMPLEMENTATION.md#api-endpoints)

---

## 🔧 Troubleshooting

### Проблемы при запуске?
→ Посмотрите раздел в [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting)

### API не работает?
→ Проверьте [IMPLEMENTATION.md](IMPLEMENTATION.md) и [test_api.py](test_api.py)

### Проблемы с БД?
→ Смотрите инструкции в [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📞 Дополнительная информация

### Версии и совместимость
- Python: 3.9+
- PostgreSQL: 12+
- FastAPI: 0.100+
- SQLAlchemy: 2.0+
- Cytoscape.js: 3.28+

### Автор и контакты
**Разработчик:** MichaelSpace2005  
**GitHub:** https://github.com/MichaelSpace2005/BackendMireaCursovaya  
**Email:** [контакт через GitHub Issues]

### Лицензия
MIT License

---

## 📋 Таблица навигации по функциям

| Функция | README | IMPL | SETUP | DEPLOY | STRUCT | CHANGES |
|---------|--------|------|-------|--------|--------|---------|
| Регистрация | ✓ | ✓ | ✓ |  | ✓ | ✓ |
| Email верификация | ✓ | ✓ | ✓ |  | ✓ | ✓ |
| JWT аутентификация | ✓ | ✓ | ✓ |  | ✓ | ✓ |
| Управление механиками | ✓ | ✓ | ✓ |  | ✓ |  |
| Визуализация графа | ✓ | ✓ | ✓ |  | ✓ | ✓ |
| Drag-and-drop | ✓ |  |  |  | ✓ |  |
| Production deployment |  |  |  | ✓ |  |  |
| Тестирование | ✓ |  |  |  |  |  |
| Troubleshooting |  |  |  | ✓ |  |  |

---

## ✅ Рекомендуемый порядок чтения

### Для новых пользователей:
1. [README.md](README.md) - Обзор проекта
2. [quick-start.sh](quick-start.sh) - Запуск
3. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Понимание структуры

### Для разработчиков:
1. [IMPLEMENTATION.md](IMPLEMENTATION.md) - Архитектура
2. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Файлы
3. [CHANGES.md](CHANGES.md) - Что было изменено

### Для DevOps инженеров:
1. [DEPLOYMENT.md](DEPLOYMENT.md) - Развертывание
2. [FINAL_CHECKLIST.md](FINAL_CHECKLIST.md) - Проверка
3. [README.md](README.md) - Production notes

### Для QA тестировщиков:
1. [README.md](README.md) - Функциональность
2. [test_api.py](test_api.py) - API тестирование
3. [FINAL_CHECKLIST.md](FINAL_CHECKLIST.md) - Проверка покрытия

---

## 📚 Дополнительные ресурсы

### Библиотеки и фреймворки
- [FastAPI документация](https://fastapi.tiangolo.com/)
- [SQLAlchemy документация](https://docs.sqlalchemy.org/)
- [Cytoscape.js документация](https://js.cytoscape.org/)

### Стандарты и Best Practices
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [RESTful API Design](https://restfulapi.net/)

---

**Последнее обновление:** Декабрь 4, 2024  
**Версия документации:** 1.0.0  
**Статус:** ✅ Полностью завершено
