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

## Подготовка проекта

### 0.1 Создание структуры для GitHub Actions

Создайте директорию для workflows:

```bash
mkdir -p .github/workflows
```

### 0.2 Создание .gitignore

Создайте файл `.gitignore` в корне проекта:

```
*.pyc
__pycache__/
*.py[cod]
*$py.class
db.sqlite3
*.log
.env
staticfiles/
media/
.pytest_cache/
.coverage
```

### 0.3 Инициализация Git репозитория

```bash
git init
git add .
git commit -m "Initial commit"
```

### 0.4 Создание репозитория на GitHub

1. Перейдите на https://github.com/new
2. Создайте новый репозиторий
3. Свяжите локальный репозиторий с GitHub:

```bash
git remote add origin <URL_вашего_репозитория>
git branch -M main
git push -u origin main
```

---

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

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run migrations
        run: python manage.py migrate

      - name: Run tests
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

## 11. Работа с secrets (опционально)

### 11.1 GitHub Secrets

Для production окружения можно использовать секреты.

В репозитории:

`Settings → Secrets and variables → Actions`

Примеры:

* `DJANGO_SECRET_KEY`
* `DATABASE_URL`

Использование:

```yaml
env:
  SECRET_KEY: ${{ secrets.DJANGO_SECRET_KEY }}
```

**Для учебного проекта с SQLite это не требуется.**

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
3. Добавить pytest
4. Добавить Ruff + Black
5. Использовать secrets
6. Подготовить Docker‑build

---

## 16. Запуск CI/CD

### 16.1 Первый запуск

После создания `.github/workflows/ci.yml` и push в GitHub:

```bash
git add .
git commit -m "Add CI workflow"
git push origin main
```

GitHub Actions запустится автоматически.

### 16.2 Где наблюдать за выполнением

1. Откройте ваш репозиторий на GitHub
2. Перейдите на вкладку **Actions**
3. Увидите список всех запусков workflow
4. Кликните на конкретный запуск для просмотра деталей

### 16.3 Визуализация процесса

Во вкладке Actions вы увидите:

- **Список workflow runs** - все запуски с статусами:
  - 🟢 Зеленая галочка - успешно
  - 🔴 Красный крестик - ошибка
  - 🟡 Желтый кружок - выполняется

- **Детали запуска** (при клике на run):
  - Список jobs (test, build, deploy)
  - Время выполнения каждого job
  - Логи каждого step

- **Граф выполнения**:
  - Визуальное представление jobs
  - Зависимости между jobs
  - Статус каждого этапа

### 16.4 Просмотр логов

1. Кликните на нужный workflow run
2. Выберите job (например, "test")
3. Раскройте любой step для просмотра логов
4. Можно скачать полные логи через кнопку справа

### 16.5 Повторный запуск

Если тест упал:

1. Откройте failed workflow run
2. Нажмите **Re-run jobs** → **Re-run failed jobs**
3. Или **Re-run all jobs** для полного перезапуска

### 16.6 Бейдж статуса

Добавьте бейдж в README.md:

```markdown
![CI](https://github.com/ваш-username/ваш-repo/workflows/Django%20CI/badge.svg)
```

Бейдж покажет текущий статус CI:
- 🟢 passing - все тесты прошли
- 🔴 failing - есть ошибки

### 16.7 Уведомления

GitHub отправит email при:
- ❌ Падении workflow
- ✅ Восстановлении после ошибки

Настройка: **Settings** → **Notifications** → **Actions**

---

## 17. Результат

После прохождения методички у вас будет:

* полноценный CI pipeline;
* проверяемый Django + Ninja API;
* готовая база для production‑деплоя.
