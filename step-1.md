# Практическое занятие по изучению CI/CD

(часть 1)

## 1. Настройка стенда

### Требования

- Python 3.13+ установлен
- Git установлен
- Аккаунт на GitHub

### Клонирование проекта

```bash
git clone <ваш-репозиторий>
cd CI-CD-GITHUB
```

## 2. Запуск проекта

### Создание виртуального окружения

```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (Linux/Mac)
source venv/bin/activate
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Создание базы данных

```bash
# Применение миграций
python manage.py migrate

# Загрузка тестовых товаров
python load_products.py
```

### Создание администратора

```bash
python manage.py createsuperuser
```

### Запуск сервера

```bash
python manage.py runserver
```

## 3. Проверка работы

### Доступные URL

- Главная страница: http://localhost:8000/
- API документация: http://localhost:8000/api/docs
- Админ-панель: http://localhost:8000/admin/

### Тестирование API

```bash
# Список товаров
curl http://localhost:8000/api/products

# Проверка здоровья
curl http://localhost:8000/api/health
```

## 4. Функционал приложения

### Модели данных

- **Product** - товары (название, цена, описание)
- **Order** - заказы (имя клиента, email, сумма)
- **OrderItem** - позиции заказа (товар, количество, цена)

### Работа с корзиной

1. Откройте http://localhost:8000/
2. Нажмите "Добавить в корзину" на любом товаре
3. Корзина обновится автоматически (HTMX)
4. Заполните форму заказа и нажмите "Оформить заказ"

### HTMX - динамика без JavaScript

Проект использует HTMX для динамического обновления страницы без написания JavaScript:

- `hx-get` - загрузка контента
- `hx-post` - отправка форм
- `hx-target` - куда вставить результат
- `hx-swap` - как вставить (innerHTML, outerHTML)

## 5. Запуск тестов

```bash
python manage.py test
```

## 6. Полезные команды

```bash
# Создание новых миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Запуск shell Django
python manage.py shell

# Сбор статических файлов
python manage.py collectstatic
```

---

---

## Технологии проекта

- **Python 3.13+**
- **Django 5.1**
- **Django Ninja 1.3** (API)
- **SQLite** (база данных)

## Структура проекта

```
CI-CD-GITHUB/
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
├── load_products.py   # Скрипт загрузки товаров
└── manage.py          # Django CLI
```

## API Endpoints

- `GET /api/products` - список товаров
- `GET /api/products/{id}` - товар по ID
- `POST /api/orders` - создать заказ
- `GET /api/orders` - список заказов
- `GET /api/health` - проверка здоровья
