# Практическое занятие по изучению CI/CD

(часть 2)

## Базовые понятия CI/CD

### CI — Continuous Integration

Непрерывная интеграция — это автоматическая проверка кода при каждом:

* `push`
* `pull request`

Обычно включает:

* установку зависимостей;
* запуск тестов;
* линтинг;
* проверку форматирования.

### CD — Continuous Delivery / Deployment

Непрерывная доставка — автоматическая:

* сборка приложения;
* публикация образов;
* деплой на сервер (опционально).

## Введение в GitHub Actions

### 1.1 Основные сущности

* **Workflow** — файл автоматизации
* **Job** — логический этап
* **Step** — отдельная команда
* **Runner** — среда выполнения

Workflow хранится в:

```
.github/workflows/ci.yml
```

---

## Первый CI pipeline

### Минимальный workflow

```yaml
name: Django CI

on:
  push:
    branches: [ "main" ]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:17
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        env:
          DB_NAME: test_db
          DB_USER: test_user
          DB_PASSWORD: test_pass
          DB_HOST: localhost
          DB_PORT: 5432
        run: python manage.py test
```

---

## 8. Настройка тестов

### 8.1 Django TestCase

Тесты находятся в `shop/tests.py`

Пример теста:

```python
from django.test import TestCase, Client

class ProductTestCase(TestCase):
    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')
```

Запуск тестов:

```bash
python manage.py test
```

---

## Линтинг и форматирование

### 9.1 Ruff

```yaml
- name: Ruff lint
  run: ruff check .
```

### 9.2 Black

```yaml
- name: Black check
  run: black --check .
```

---

## 10. Проверка типов (mypy)

```yaml
- name: MyPy
  run: mypy .
```

---

## 11. Работа с secrets

### 11.1 GitHub Secrets

В репозитории:

`Settings → Secrets and variables → Actions`

Примеры:

* `DJANGO_SECRET_KEY`
* `POSTGRES_PASSWORD`

Использование:

```yaml
env:
  SECRET_KEY: ${{ secrets.DJANGO_SECRET_KEY }}
```

---

## 12. CI для Django Ninja API

* тестировать API через Django test client;
* проверять создание заказов;
* проверять получение списка товаров.

Пример:

```python
from django.test import TestCase, Client
import json

class ProductTestCase(TestCase):
    def test_api_get_products(self):
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
```

---

## 13. CD (базовый уровень)

Варианты:

* сборка Docker‑образа;
* push в GitHub Container Registry;
* деплой на VPS.

(Рекомендуется изучать после уверенного CI)

---

## 14. Частые ошибки

* ❌ не ждать готовности PostgreSQL
* ❌ хранить пароли в репозитории
* ❌ запускать миграции без тестов
* ❌ отсутствие кэша pip

---

## 15. План обучения (рекомендуемый)

1. Понять CI концептуально
2. Запустить простой workflow
3. Добавить PostgreSQL service
4. Подключить pytest
5. Добавить Ruff + Black
6. Использовать secrets
7. Подготовить Docker‑build

---

## 16. Результат

После прохождения методички у вас будет:

* полноценный CI pipeline;
* проверяемый Django + Ninja API;
* готовая база для production‑деплоя.
