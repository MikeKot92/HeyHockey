## О проекте
HeyHockey! — это полнофункциональный интернет-магазин на Django, ориентированный на продажу хоккейной экипировки,
формы и аксессуаров. Пользователи могут просматривать каталог товаров, оформлять заказы, проходить аутентификацию через социальные сети,
оплачивать покупки через YooKassa и получать уведомления о статусе заказа. 
Администраторы управляют товарами, заказами и рассылками через удобную панель Django Admin.

## Технологический стек
- Python / Django — основной бэкенд-фреймворк для бизнес-логики и API
- HTML / CSS / Bootstrap / JavaScript / HTMX — фронтенд с динамическим обновлением без перезагрузки страниц
- PostgreSQL — надежная реляционная СУБД для хранения данных
- Redis — кэширование запросов и брокер сообщений для Celery
- Celery — выполнение асинхронных задач (рассылки, уведомления, обработка заказов)
- Docker / docker-compose — контейнеризация и упрощение развёртывания
- Git / GitHub Actions — система контроля версий и CI/CD-пайплайн
- Nginx + SSL (Let’s Encrypt) — проксирование и безопасное HTTPS-соединение на продакшене
- OAuth 2.0 — вход через социальные сети
- YooKassa — интеграция платежной системы
- Telegram Bot API — уведомления менеджеров о новых заказах

## Локальный запуск проекта
Следуйте этим шагам, чтобы запустить проект для локальной разработки:

1. Клонируйте репозиторий:

> git clone https://github.com/MikeKot92/HeyHockey.git

2. Создайте файл .env в корне проекта и подставьте свои значения где их нет:

> SECRET_KEY=
> DEBUG=True
> DOMAIN_NAME='http://127.0.0.1:8000'
> YOOKASSA_SHOP_ID=
> YOOKASSA_SECRET_KEY=
> TELE_TOKEN=
> CHAT=
> EMAIL_HOST = 
> EMAIL_PORT = 
> EMAIL_HOST_USER = 
> EMAIL_HOST_PASSWORD = 
> REDIS_HOST='redis'
> REDIS_PORT='6379'
> DB_ENGINE='django.db.backends.postgresql_psycopg2'
> DB_NAME=
> DB_USER=
> DB_PASSWORD=
> DB_HOST='db'
> DB_PORT='5432'
> SOCIAL_AUTH_GITHUB_KEY= 
> SOCIAL_AUTH_GITHUB_SECRET=

3. Поднимите проект командой:

docker compose --env-file .env -f docker-compose.yml up -d --build

Теперь проект готов к работе! 
