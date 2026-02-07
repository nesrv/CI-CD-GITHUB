
![CI](https://github.com/nesrv/CI-CD-GITHUB/workflows/Django%20CI/badge.svg)

# Simple E-Shop для изучения CI/CD

Простой интернет-магазин на Django с Ninja API, PostgreSQL и Docker для изучения CI/CD с GitHub Actions.

## Технологии

- **Python 3.13+**
- **Django 5.1**
- **Django Ninja 1.3** (API)
- **PostgreSQL 17**
- **psycopg 3** (PostgreSQL adapter)
- **Docker & Docker Compose**

## Структура проекта

```
CI-CD-GIT/
├── eshop/              # Django проект
│   ├── settings.py     # Настройки
│   ├── urls.py         # URL маршруты
│   └── wsgi.py         # WSGI конфигурация
├── shop/               # Django приложение
│   ├── models.py       # Модели (Product, Order, OrderItem)
│   ├── api.py          # API endpoints (Ninja)
│   ├── admin.py        # Админка
│   └── tests.py        # Тесты
├── requirements.txt    # Python зависимости
├── Dockerfile         # Docker образ
├── docker-compose.yml # Docker Compose для разработки
└── manage.py          # Django CLI
```

## API Endpoints

- `GET /api/products` - список товаров
- `GET /api/products/{id}` - товар по ID
- `POST /api/orders` - создать заказ
- `GET /api/orders` - список заказов
- `GET /api/health` - проверка здоровья

## Быстрый старт

```bash
# Запуск через Docker
docker-compose up --build

# Миграции
docker-compose exec web python manage.py makemigrations shop
docker-compose exec web python manage.py migrate

# Загрузка тестовых товаров
docker-compose exec web python load_products.py

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Тесты
docker-compose exec web python manage.py test
```

## Доступ

- API: http://localhost:8000/api/
- Админка: http://localhost:8000/admin/
- Swagger: http://localhost:8000/api/docs

## Готов для CI/CD! 🚀
