# 🚀 Deployment Guide

Гайд по развертыванию Evolution Tree на production сервере.

## Требования к серверу

- OS: Ubuntu 20.04+ или CentOS 8+
- Python: 3.9+
- Database: PostgreSQL 12+
- Memory: минимум 2GB
- Storage: минимум 10GB

## 1️⃣ Подготовка сервера

### Обновить систему
```bash
sudo apt update && sudo apt upgrade -y
```

### Установить зависимости
```bash
sudo apt install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib nginx curl git
```

### Создать пользователя для приложения
```bash
sudo useradd -m -s /bin/bash appuser
sudo usermod -aG sudo appuser
```

## 2️⃣ Настройка PostgreSQL

```bash
# Подключиться к PostgreSQL
sudo -u postgres psql

# Создать БД
CREATE DATABASE evolution_db;

# Создать пользователя
CREATE USER evolutionuser WITH PASSWORD 'strong_password_here';

# Выдать права
GRANT ALL PRIVILEGES ON DATABASE evolution_db TO evolutionuser;

# Выход
\q
```

## 3️⃣ Подготовка приложения

```bash
# Перейти в папку приложения
cd /home/appuser
git clone https://github.com/MichaelSpace2005/BackendMireaCursovaya.git
cd BackendMireaCursovaya

# Создать виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## 4️⃣ Конфигурация

### Создать файл .env
```bash
cat > .env << EOF
# Database
DB_USER=evolutionuser
DB_PASS=strong_password_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=evolution_db

# Security
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')

# Debug (отключить в production)
DEBUG=False

# Email (для отправки писем)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EOF
```

### Обновить app/infra/config.py
```python
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASS: str = os.getenv("DB_PASS", "postgres")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "evolution_db")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Обновить app/infra/security.py
```python
from app.infra.config import settings

SECRET_KEY = settings.SECRET_KEY  # Вместо hardcoded значения
```

## 5️⃣ Systemd Service

### Создать сервис
```bash
sudo tee /etc/systemd/system/evolution-tree.service > /dev/null << EOF
[Unit]
Description=Evolution Tree API
After=network.target postgresql.service

[Service]
Type=notify
User=appuser
WorkingDirectory=/home/appuser/BackendMireaCursovaya
Environment="PATH=/home/appuser/BackendMireaCursovaya/venv/bin"
ExecStart=/home/appuser/BackendMireaCursovaya/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

### Активировать сервис
```bash
sudo systemctl daemon-reload
sudo systemctl enable evolution-tree
sudo systemctl start evolution-tree
sudo systemctl status evolution-tree
```

## 6️⃣ Nginx Reverse Proxy

### Создать конфиг
```bash
sudo tee /etc/nginx/sites-available/evolution-tree > /dev/null << EOF
upstream evolution_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://evolution_backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket support (если понадобится)
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Статические файлы
    location /static {
        alias /home/appuser/BackendMireaCursovaya/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF
```

### Активировать конфиг
```bash
sudo ln -s /etc/nginx/sites-available/evolution-tree /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 7️⃣ SSL Certificate (Let's Encrypt)

```bash
# Установить Certbot
sudo apt install certbot python3-certbot-nginx -y

# Получить сертификат
sudo certbot --nginx -d your-domain.com

# Автоматическое обновление
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## 8️⃣ Мониторинг и Логи

### Просмотреть логи приложения
```bash
sudo journalctl -u evolution-tree -f
```

### Просмотреть логи Nginx
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Установить логирование приложения

В `app/main.py` добавить:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/appuser/BackendMireaCursovaya/logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
```

## 9️⃣ Backup и восстановление

### Backup БД
```bash
#!/bin/bash
BACKUP_DIR="/home/appuser/backups"
mkdir -p $BACKUP_DIR

pg_dump -U evolutionuser evolution_db | \
    gzip > $BACKUP_DIR/db_$(date +%Y%m%d_%H%M%S).sql.gz

# Удалить старые backup'ы (старше 7 дней)
find $BACKUP_DIR -type f -mtime +7 -delete
```

### Восстановление из backup'а
```bash
gunzip < backup.sql.gz | psql -U evolutionuser evolution_db
```

## 🔟 Оптимизация Production

### app/main.py
```python
# Отключить автоматическую перезагрузку
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",  # Только localhost
        port=8000,
        reload=False,  # Отключить reload
        workers=4,     # Несколько рабочих процессов
        log_level="info"
    )
```

### Nginx
```nginx
# Включить compression
gzip on;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript;
gzip_min_length 1000;

# Включить кэширование
expires 1h;
```

## 1️⃣1️⃣ Мониторинг производительности

### Установить Prometheus + Grafana (опционально)
```bash
# Это расширенная настройка для production мониторинга
docker run -d -p 9090:9090 prom/prometheus
docker run -d -p 3000:3000 grafana/grafana
```

## 1️⃣2️⃣ Безопасность

✅ Рекомендации:
```bash
# Правила брандмауэра
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Регулярные обновления
sudo apt autoremove
sudo apt autoclean

# Мониторинг безопасности
sudo apt install fail2ban
```

## Проверочный лист

- [ ] Сервер обновлён
- [ ] PostgreSQL установлен и настроен
- [ ] Приложение развёрнуто
- [ ] .env файл создан
- [ ] Systemd сервис активирован
- [ ] Nginx настроен как reverse proxy
- [ ] SSL сертификат установлен
- [ ] Backup скрипт работает
- [ ] Логирование настроено
- [ ] Мониторинг включен
- [ ] Брандмауэр настроен

## Troubleshooting

### Приложение не запускается
```bash
# Проверить логи
sudo journalctl -u evolution-tree -n 50

# Проверить синтаксис Python
python3 -m py_compile app/main.py

# Проверить подключение к БД
psql -U evolutionuser -h localhost -d evolution_db
```

### Nginx ошибка 502 Bad Gateway
```bash
# Проверить, что приложение слушает
netstat -tlnp | grep 8000

# Проверить конфиг Nginx
sudo nginx -t

# Перезагрузить Nginx
sudo systemctl restart nginx
```

### SSL сертификат просрочен
```bash
# Обновить вручную
sudo certbot renew --dry-run

# Или просто обновить
sudo certbot renew
```

## Полезные команды

```bash
# Перезагрузить приложение
sudo systemctl restart evolution-tree

# Посмотреть статус
sudo systemctl status evolution-tree

# Включить сервис в автозапуск
sudo systemctl enable evolution-tree

# Отключить из автозапуска
sudo systemctl disable evolution-tree

# Посмотреть логи в реальном времени
sudo journalctl -u evolution-tree -f

# Перезагрузить Nginx
sudo systemctl restart nginx

# Проверить статус Nginx
sudo systemctl status nginx
```

---

**Версия:** 1.0.0  
**Последнее обновление:** Декабрь 2024  
**Автор:** MichaelSpace2005
