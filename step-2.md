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

**Что тестируем:**

1. **Создание товара** - проверка корректности сохранения данных
2. **API получения списка товаров** - GET /api/products
3. **API создания заказа** - POST /api/orders с расчетом суммы
4. **Health check endpoint** - GET /api/health

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

**Результат выполнения:**

```
Found 4 test(s).
Creating test database...
....
----------------------------------------------------------------------
Ran 4 tests in 0.123s

OK
```

---

---

## 9. Работа с secrets (опционально)

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

## 10. CI для Django Ninja API

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

## 11. CD (базовый уровень)

Варианты:

* сборка Docker‑образа;
* push в GitHub Container Registry;
* деплой на VPS.

(Рекомендуется изучать после уверенного CI)

---

## 12. Частые ошибки

* ❌ не ждать готовности PostgreSQL
* ❌ хранить пароли в репозитории
* ❌ запускать миграции без тестов
* ❌ отсутствие кэша pip

---

## 13. Когда workflow падает с ошибками

### 13.1 Ошибка установки зависимостей

**Симптом:**
```
ERROR: Could not find a version that satisfies the requirement
```

**Причины:**
- Неправильная версия пакета в requirements.txt
- Несовместимость версий Python
- Опечатка в названии пакета

**Решение:**
```bash
# Проверьте локально
pip install -r requirements.txt

# Обновите версии
pip freeze > requirements.txt
```

### 13.2 Ошибка миграций

**Симптом:**
```
django.db.utils.OperationalError: no such table
```

**Причины:**
- Не выполнены миграции перед тестами
- Отсутствует шаг `python manage.py migrate` в workflow

**Решение:**
Добавьте в workflow перед тестами:
```yaml
- name: Run migrations
  run: python manage.py migrate
```

### 13.3 Падение тестов

**Симптом:**
```
FAILED shop/tests.py::ProductTestCase::test_api_create_order
AssertionError: 200 != 500
```

**Причины:**
- Ошибка в коде
- Неправильные данные в тесте
- Отсутствие тестовых данных

**Решение:**
```bash
# Запустите тесты локально
python manage.py test

# Запустите конкретный тест
python manage.py test shop.tests.ProductTestCase.test_api_create_order

# Посмотрите детали ошибки
python manage.py test --verbosity=2
```

### 13.4 Ошибка импорта модулей

**Симптом:**
```
ModuleNotFoundError: No module named 'ninja'
```

**Причины:**
- Пакет не указан в requirements.txt
- Опечатка в названии

**Решение:**
```bash
# Добавьте пакет
echo "django-ninja==1.3.0" >> requirements.txt
```

### 13.5 Ошибка Python версии

**Симптом:**
```
SyntaxError: invalid syntax
```

**Причины:**
- Используется синтаксис новой версии Python
- В workflow указана старая версия

**Решение:**
Проверьте версию в workflow:
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.13"  # Должна совпадать с локальной
```

### 13.6 Ошибка прав доступа

**Симптом:**
```
Permission denied
```

**Причины:**
- Попытка записи в защищенную директорию
- Отсутствие прав на выполнение скрипта

**Решение:**
```yaml
# Для скриптов
- name: Make script executable
  run: chmod +x script.sh
```

### 13.7 Timeout ошибка

**Симптом:**
```
Error: The operation was canceled.
```

**Причины:**
- Тесты выполняются слишком долго (>6 часов по умолчанию)
- Зависание процесса

**Решение:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10  # Установите разумный лимит
```

### 13.8 Как отладить workflow

**1. Добавьте отладочный вывод:**
```yaml
- name: Debug info
  run: |
    python --version
    pip list
    ls -la
    env
```

**2. Используйте act для локального запуска:**
```bash
# Установите act (https://github.com/nektos/act)
act -j test
```

**3. Включите debug логи:**
В репозитории: Settings → Secrets → New repository secret
- Name: `ACTIONS_STEP_DEBUG`
- Value: `true`

### 13.9 Чеклист при ошибке

✅ Проверьте логи в GitHub Actions
✅ Запустите тесты локально
✅ Проверьте requirements.txt
✅ Убедитесь, что миграции выполняются
✅ Проверьте версию Python
✅ Посмотрите предыдущие успешные запуски
✅ Проверьте последние изменения в коде

---

## 13.10 Практические примеры для самостоятельной работы

### Пример 1: Сломать установку зависимостей

**Задание:** Увидеть ошибку установки пакета

**Действия:**
1. Откройте `requirements.txt`
2. Добавьте несуществующий пакет:
```
Django==5.1.4
django-ninja==1.3.0
nonexistent-package==1.0.0
```
3. Закоммитьте и запушьте:
```bash
git add requirements.txt
git commit -m "Test: break dependencies"
git push
```

**Ожидаемый результат:**
- Workflow упадет на шаге "Install dependencies"
- В логах увидите: `ERROR: Could not find a version that satisfies the requirement nonexistent-package`
- Статус: 🔴 Failed

**Как исправить:**
```bash
# Удалите строку с nonexistent-package
git add requirements.txt
git commit -m "Fix: remove invalid package"
git push
```

### Пример 2: Сломать тест

**Задание:** Увидеть падение теста

**Действия:**
1. Откройте `shop/tests.py`
2. Измените ожидаемый статус код:
```python
def test_health_check(self):
    response = self.client.get('/api/health')
    self.assertEqual(response.status_code, 404)  # Было 200
    self.assertEqual(response.json()['status'], 'ok')
```
3. Закоммитьте и запушьте:
```bash
git add shop/tests.py
git commit -m "Test: break health check test"
git push
```

**Ожидаемый результат:**
- Workflow упадет на шаге "Run tests"
- В логах увидите:
```
FAILED shop/tests.py::ProductTestCase::test_health_check
AssertionError: 200 != 404
```
- Статус: 🔴 Failed

**Как исправить:**
```python
# Верните правильное значение
self.assertEqual(response.status_code, 200)
```

### Пример 3: Забыть миграции

**Задание:** Увидеть ошибку отсутствия таблиц

**Действия:**
1. Откройте `.github/workflows/ci.yml`
2. Закомментируйте шаг миграций:
```yaml
# - name: Run migrations
#   run: python manage.py migrate

- name: Run tests
  run: python manage.py test
```
3. Закоммитьте и запушьте

**Ожидаемый результат:**
- Workflow упадет на шаге "Run tests"
- В логах увидите: `django.db.utils.OperationalError: no such table: shop_product`
- Статус: 🔴 Failed

**Как исправить:**
Раскомментируйте шаг миграций

### Пример 4: Неправильная версия Python

**Задание:** Увидеть несовместимость версий

**Действия:**
1. Откройте `.github/workflows/ci.yml`
2. Измените версию Python:
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.8"  # Было 3.13
```
3. Закоммитьте и запушьте

**Ожидаемый результат:**
- Workflow может упасть на установке зависимостей или тестах
- В логах увидите ошибки совместимости
- Статус: 🔴 Failed

**Как исправить:**
Верните версию 3.13

### Пример 5: Синтаксическая ошибка в коде

**Задание:** Увидеть ошибку синтаксиса

**Действия:**
1. Откройте `shop/models.py`
2. Добавьте синтаксическую ошибку:
```python
class Product(models.Model):
    name = models.CharField(max_length=100
    # Забыли закрывающую скобку
```
3. Закоммитьте и запушьте

**Ожидаемый результат:**
- Workflow упадет на шаге "Run tests"
- В логах увидите: `SyntaxError: invalid syntax`
- Статус: 🔴 Failed

**Как исправить:**
Добавьте закрывающую скобку

### Визуализация в GitHub Actions

**Где смотреть:**
1. Перейдите в репозиторий на GitHub
2. Откройте вкладку **Actions**
3. Увидите список запусков:

```
✅ Fix: remove invalid package        main  #5  2m 15s
❌ Test: break health check test     main  #4  1m 45s
❌ Test: break dependencies          main  #3  0m 30s
✅ Add CI workflow                   main  #2  2m 10s
✅ Initial commit                    main  #1  2m 05s
```

4. Кликните на ❌ Failed запуск
5. Увидите детали:

```
test
  ✅ Set up job                    5s
  ✅ Run actions/checkout@v4       2s
  ✅ Set up Python                 8s
  ❌ Install dependencies          15s  ← Здесь упало
  ⚪ Run migrations                -
  ⚪ Run tests                     -
  ✅ Post Run actions/checkout@v4  1s
  ✅ Complete job                  1s
```

6. Раскройте ❌ шаг для просмотра логов

### Рекомендации

1. **Пробуйте каждый пример** - это лучший способ понять CI/CD
2. **Смотрите логи** - они подскажут причину ошибки
3. **Исправляйте сразу** - не накапливайте сломанные коммиты
4. **Тестируйте локально** - перед push запускайте `python manage.py test`

---

## 14. План обучения (рекомендуемый)

1. Понять CI концептуально
2. Запустить простой workflow
3. Добавить pytest
4. Добавить Ruff + Black
5. Использовать secrets
6. Подготовить Docker‑build

---

## 15. Запуск CI/CD

### 15.1 Первый запуск

После создания `.github/workflows/ci.yml` и push в GitHub:

```bash
git add .
git commit -m "Add CI workflow"
git push origin main
```

GitHub Actions запустится автоматически.

### 15.2 Где наблюдать за выполнением

1. Откройте ваш репозиторий на GitHub
2. Перейдите на вкладку **Actions**
3. Увидите список всех запусков workflow
4. Кликните на конкретный запуск для просмотра деталей

### 15.3 Визуализация процесса

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

### 15.4 Просмотр логов

1. Кликните на нужный workflow run
2. Выберите job (например, "test")
3. Раскройте любой step для просмотра логов
4. Можно скачать полные логи через кнопку справа

### 15.5 Повторный запуск

Если тест упал:

1. Откройте failed workflow run
2. Нажмите **Re-run jobs** → **Re-run failed jobs**
3. Или **Re-run all jobs** для полного перезапуска

### 15.6 Бейдж статуса

Добавьте бейдж в README.md:

```markdown
![CI](https://github.com/ваш-username/ваш-repo/workflows/Django%20CI/badge.svg)
```

Бейдж покажет текущий статус CI:
- 🟢 passing - все тесты прошли
- 🔴 failing - есть ошибки

### 15.7 Уведомления

GitHub отправит email при:
- ❌ Падении workflow
- ✅ Восстановлении после ошибки

Настройка: **Settings** → **Notifications** → **Actions**

---

## 16. Результат

---

## 17. Следующий шаг

Для улучшения качества кода см. **step-3.md**:
- Линтинг с Ruff
- Форматирование с Black
- Проверка типов с mypy

После прохождения методички у вас будет:

* полноценный CI pipeline;
* проверяемый Django + Ninja API;
* готовая база для production‑деплоя.
