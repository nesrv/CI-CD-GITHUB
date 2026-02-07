# Методичка по изучению CI/CD с помощью GitHub Actions

## 1. Цель методички

Эта методичка предназначена для поэтапного изучения **CI/CD (Continuous Integration / Continuous Delivery)** на примере реального backend‑проекта на базе:

* **Python 3.13+**
* **Django 5.1**
* **Django Ninja 1.3** (REST API)
* **PostgreSQL 17** (в Docker‑контейнере)
* **GitHub + GitHub Actions**

В результате вы:

* поймёте ключевые принципы CI/CD;
* настроите автоматическую проверку кода;
* добавите тестирование и линтеры;
* научитесь работать с secrets;
* подготовите основу для деплоя.

---

## 2. Базовые понятия CI/CD

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

---

## 3. Структура проекта (рекомендуемая)

```
project-root/
├── .github/
│   └── workflows/
│       └── ci.yml
├── backend/
│   ├── manage.py
│   ├── config/
│   ├── apps/
│   └── tests/
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── docker-compose.yml
└── Dockerfile
```

---

## 4. Подготовка проекта

### 4.1 Зависимости

**requirements.txt**

```
Django==5.1.*
django-ninja==1.3.*
psycopg[binary]
```

**requirements-dev.txt**

```
pytest
pytest-django
ruff
black
mypy
```

---

## 5. Docker для PostgreSQL 17

**docker-compose.yml**

```
version: "3.9"
services:
  db:
    image: postgres:17
    container_name: postgres_ci
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_pass
    ports:
      - "5432:5432"
```

В CI база будет подниматься автоматически как service.

---

## 6. Введение в GitHub Actions

### 6.1 Основные сущности

* **Workflow** — файл автоматизации
* **Job** — логический этап
* **Step** — отдельная команда
* **Runner** — среда выполнения

Workflow хранится в:

```
.github/workflows/ci.yml
```

---

## 7. Первый CI pipeline

### 7.1 Минимальный workflow

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
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run tests
        env:
          DATABASE_URL: postgres://test_user:test_pass@localhost:5432/test_db
        run: pytest
```

---

## 8. Настройка тестов

### 8.1 pytest-django

**pytest.ini**

```
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_tests.py
```

Пример теста:

```python
def test_healthcheck(client):
    response = client.get("/api/health")
    assert response.status_code == 200
```

---

## 9. Линтинг и форматирование

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
* проверять OpenAPI schema;
* добавлять контрактные тесты.

Пример:

```python
from ninja.testing import TestClient

client = TestClient(api)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
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

---

**Дальнейшие шаги:**

* GitHub Environments
* Review apps
* Canary deployments
* Monitoring + alerts
