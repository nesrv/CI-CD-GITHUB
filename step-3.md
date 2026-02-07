# Практическое занятие по изучению CI/CD

(часть 3)

## Улучшение качества кода: Линтинг и проверка типов

### Введение

После настройки базового CI (step-2.md) можно улучшить качество кода с помощью дополнительных инструментов.

### Зачем нужны эти инструменты?

- **Ruff** - быстрый линтер для проверки стиля кода (замена flake8, pylint)
- **Black** - автоматическое форматирование кода
- **mypy** - статическая проверка типов

**Преимущества:**
- Единый стиль кода в команде
- Автоматическое обнаружение ошибок
- Меньше багов в production
- Улучшение читаемости кода

---

## 1. Установка инструментов

### 1.1 Создание requirements-dev.txt

Создайте файл `requirements-dev.txt`:

```
ruff==0.8.4
black==24.10.0
mypy==1.13.0
django-stubs==5.1.1
```

### 1.2 Установка

```bash
pip install -r requirements-dev.txt
```

---

## 2. Ruff - линтер

### 2.1 Создание конфигурации

Создайте файл `ruff.toml`:

```toml
line-length = 88
target-version = "py313"

[lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
]
ignore = [
    "E501",  # line too long (handled by black)
]

[lint.per-file-ignores]
"__init__.py" = ["F401"]
"*/migrations/*.py" = ["E501", "N806"]
```

### 2.2 Запуск проверки

```bash
# Проверка всего проекта
ruff check .

# Автоматическое исправление
ruff check . --fix
```

### 2.3 Типичные ошибки и исправления

**Неиспользуемые импорты:**
```python
# До
import os
from django.db import models

# После
from django.db import models
```

**Неправильный порядок импортов:**
```python
# До
from shop.models import Product
import json
from django.test import TestCase

# После
import json

from django.test import TestCase

from shop.models import Product
```

---

## 3. Black - форматирование

### 3.1 Создание конфигурации

Создайте файл `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py313']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | venv
  | migrations
)/
'''
```

### 3.2 Запуск форматирования

```bash
# Проверка без изменений
black --check .

# Форматирование файлов
black .

# Форматирование конкретного файла
black shop/models.py
```

### 3.3 Что делает Black?

- Выравнивает отступы
- Добавляет/убирает пробелы
- Переносит длинные строки
- Форматирует строки и списки

**Пример:**

```python
# До
def create_order(request,order_data:OrderCreateSchema):
    total=Decimal('0')
    order=Order.objects.create(customer_name=order_data.customer_name,customer_email=order_data.customer_email,total=total)
    return order

# После
def create_order(request, order_data: OrderCreateSchema):
    total = Decimal("0")
    order = Order.objects.create(
        customer_name=order_data.customer_name,
        customer_email=order_data.customer_email,
        total=total,
    )
    return order
```

---

## 4. mypy - проверка типов

### 4.1 Создание конфигурации

Добавьте в `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.13"
plugins = ["mypy_django_plugin.main"]
exclude = ["venv", "migrations"]

[tool.django-stubs]
django_settings_module = "eshop.settings"

[[tool.mypy.overrides]]
module = "ninja.*"
ignore_missing_imports = true
```

### 4.2 Запуск проверки

```bash
# Проверка всего проекта
mypy .

# Проверка конкретного файла
mypy shop/models.py
```

### 4.3 Добавление типов в код

**models.py:**
```python
from django.db import models
from typing import Optional

class Product(models.Model):
    name: str = models.CharField(max_length=100)
    price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self) -> str:
        return self.name
```

**api.py:**
```python
from typing import List
from ninja import NinjaAPI
from .models import Product

api = NinjaAPI()

@api.get("/products", response=List[ProductSchema])
def list_products(request) -> List[Product]:
    return list(Product.objects.all())
```

---

## 5. Интеграция в CI/CD

### 5.1 Обновление requirements-dev.txt

Убедитесь, что файл создан и содержит все зависимости.

### 5.2 Обновление .github/workflows/ci.yml

```yaml
name: Django CI

on:
  push:
    branches: [ "main" ]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run Ruff
        run: ruff check .

      - name: Run Black
        run: black --check .

      - name: Run mypy
        run: mypy .

      - name: Run migrations
        run: python manage.py migrate

      - name: Run tests
        run: python manage.py test
```

### 5.3 Обновление .gitignore

Добавьте:

```
.mypy_cache/
.ruff_cache/
```

---

## 6. Локальная проверка перед commit

### 6.1 Создание скрипта проверки

Создайте файл `check.sh` (Linux/Mac):

```bash
#!/bin/bash
echo "Running Ruff..."
ruff check .

echo "Running Black..."
black --check .

echo "Running mypy..."
mypy .

echo "Running tests..."
python manage.py test
```

Или `check.bat` (Windows):

```batch
@echo off
echo Running Ruff...
ruff check .

echo Running Black...
black --check .

echo Running mypy...
mypy .

echo Running tests...
python manage.py test
```

### 6.2 Использование

```bash
# Linux/Mac
chmod +x check.sh
./check.sh

# Windows
check.bat
```

---

## 7. Исправление существующего кода

### 7.1 Пошаговое исправление

```bash
# 1. Форматирование кода
black .

# 2. Автоисправление Ruff
ruff check . --fix

# 3. Проверка оставшихся ошибок Ruff
ruff check .

# 4. Проверка типов (могут быть ошибки)
mypy .

# 5. Запуск тестов
python manage.py test
```

### 7.2 Игнорирование ошибок mypy

Если mypy выдает много ошибок, можно временно игнорировать:

```python
# type: ignore
```

Или в конфигурации:

```toml
[tool.mypy]
ignore_errors = true  # временно
```

---

## 8. Результат

После настройки у вас будет:

✅ Единый стиль кода (Black)
✅ Проверка на ошибки (Ruff)
✅ Проверка типов (mypy)
✅ Автоматическая проверка в CI/CD
✅ Меньше багов в production

---

## 9. Полезные команды

```bash
# Форматирование + исправление
black . && ruff check . --fix

# Полная проверка
ruff check . && black --check . && mypy . && python manage.py test

# Проверка только измененных файлов
git diff --name-only | grep '\.py$' | xargs black
```

---

## 10. Частые ошибки

❌ Забыть установить requirements-dev.txt
❌ Не добавить конфигурационные файлы в git
❌ Игнорировать все ошибки mypy
❌ Не запускать проверки локально перед push

✅ Всегда запускайте `black .` перед commit
✅ Исправляйте ошибки Ruff сразу
✅ Постепенно добавляйте типы в код
