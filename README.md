# Автоматизированное тестирование API микросервиса объявлений

## Автор: Прель Александр
## Описание проекта

Этот проект содержит автоматизированные тесты для API микросервиса объявлений Avito.

**Host**: https://qa-internship.avito.com

## Задания

### Задание 1: Тестирование карьерного сайта Авито

Перед вами скриншот страницы карьерного сайта Авито. Изучите его, перечислите все имеющиеся баги, и укажите их приоритет (high, medium, low). Объясните, почему багам присвоены именно они.

**Результаты задания 1**: Все найденные баги задокументированы в файле `BUGS.md`.

### Задание 2: Автоматизированное тестирование API микросервиса объявлений

## Структура проекта

```
project/
├── tests/                      # Директория с тестами
│   ├── __init__.py
│   ├── test_create_ad.py           # Тесты создания объявлений
│   ├── test_get_ad_by_id.py        # Тесты получения объявления по ID
│   ├── test_get_ads_by_seller.py   # Тесты получения объявлений продавца
│   └── test_get_ad_stats.py        # Тесты получения статистики
├── conftest.py                     # Конфигурация pytest и фикстуры
├── img1.png                        # Скрин для 1 задания
├── TESTCASES.md                    # Тест-кейсы
├── BUGS.md                         # Баг-репорты
└── README.md                       # Этот файл
```


## Запуск тестов

### Запуск тестов с подробным выводом

```bash
pytest -v
```

### Запуск тестов с очень подробным выводом

```bash
pytest -vv
```

### Запуск конкретного файла с тестами

```bash
pytest tests/test_create_ad.py
```

### Запуск конкретного теста

```bash
pytest tests/test_create_ad.py::TestCreateAd::test_create_ad_success
```

### Запуск тестов с выводом print-ов

```bash
pytest -s
```

## Описание тестов

### 1. Тесты создания объявления (test_create_ad.py)

- `test_create_ad_success` - успешное создание объявления
- `test_create_ad_missing_required_fields` - создание без обязательных полей
- `test_create_ad_invalid_price_type` - невалидный тип данных для цены
- `test_create_ad_negative_price` - отрицательная цена
- `test_create_ad_empty_title` - пустой заголовок
- `test_create_ad_unique_ids` - проверка уникальности ID

### 2. Тесты получения объявления по ID (test_get_ad_by_id.py)

- `test_get_existing_ad` - получение существующего объявления
- `test_get_nonexistent_ad` - получение несуществующего объявления
- `test_get_ad_invalid_id_format` - невалидный формат ID
- `test_get_ad_data_persistence` - проверка сохранения данных

### 3. Тесты получения объявлений продавца (test_get_ads_by_seller.py)

- `test_get_ads_existing_seller` - получение объявлений существующего продавца
- `test_get_ads_nonexistent_seller` - получение объявлений несуществующего продавца
- `test_get_ads_seller_without_ads` - получение объявлений продавца без объявлений
- `test_get_ads_different_sellers` - проверка работы с разными продавцами

### 4. Тесты получения статистики (test_get_ad_stats.py)

- `test_get_stats_existing_ad` - получение статистики существующего объявления
- `test_get_stats_nonexistent_ad` - получение статистики несуществующего объявления
- `test_get_stats_invalid_id_format` - невалидный формат ID

## Фикстуры

Проект использует следующие фикстуры pytest (определены в `conftest.py`):

- `base_url` - базовый URL API
- `session` - HTTP сессия для запросов
- `unique_seller_id` - уникальный ID продавца (111111-999999)
- `sample_ad_data` - пример данных для создания объявления
- `created_ad` - созданное объявление (автоматически создается перед тестом)
- `multiple_ads` - несколько объявлений одного продавца