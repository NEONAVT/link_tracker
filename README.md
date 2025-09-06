# Link Tracker (FastAPI + Redis)

Небольшой сервис на FastAPI для трекинга посещённых ссылок.  
Хранит домены в Redis и предоставляет два HTTP-эндпоинта:  
добавление ссылок и получение уникальных доменов за указанный интервал времени.

## Основные возможности

- **POST `/links-tracker/visited_links`** — принимает список ссылок и сохраняет их домены с отметкой времени.  
- **GET `/links-tracker/visited_domains?from=...&to=...`** — возвращает список уникальных доменов за интервал Unix-времени `[from, to]`.  
- Валидация URL → извлекается домен, игнорируется порт и путь.  
- Хранение в **Redis Sorted Set**: score = Unix-timestamp, value = домен.  
- Логирование в консоль и файл (`logs/app.log`), опциональная интеграция **Sentry**.


### Технические особенности

- Python 3.12, FastAPI, Uvicorn  
- Redis  
- Pydantic Settings для конфигурации из `.env`  
- Poetry для управления зависимостями  
- Flake8, Pytest
- Pdoc (генерация документации)
- Sentry SDK (опционально)  

## Структура проекта

```
link_tracker/
├── main.py              # Точка входа FastAPI-приложения
├── settings.py          # Конфигурация через Pydantic Settings
├── dependency.py        # DI-провайдеры (Redis, репозитории, сервисы)
├── exceptions.py        # Кастомные HTTP-исключения (400/422/503)
├── docker-compose.yml   # Конфиг для запуска Redis (и опционально приложения)
├── Makefile             # Утилитарные команды (run, run-prod, install, uninstall)
├── pyproject.toml       # Poetry и список зависимостей
├── poetry.lock          # Зафиксированные версии зависимостей
│
├── database/            # Работа с Redis
│   └── redis_accessor.py  # Подключение и проверка соединения
│
├── repository/          # Доступ к данным
│   └── link_repository.py # Репозиторий: хранение доменов в Redis Sorted Set
│
├── services/            # Бизнес-логика
│   └── link_service.py    # Обработка ссылок, нормализация доменов, выборка по времени
│
├── routers/             # Маршруты FastAPI
│   └── link_tracker.py    # POST /visited_links, GET /visited_domains
│
├── schemas/             # Pydantic-схемы
│   └── link_schemas.py    # LinksRequest, DomainsResponse, StatusResponse
│
├── log_config/          # Логирование и мониторинг
│   ├── logging_config.py  # Настройка логирования (консоль + файл)
│   └── sentry_config.py   # Интеграция с Sentry
│
├── logs/                # Директория для логов
│   └── app.log
│
└── README.md            # Документация проекта
```

### Взаимодействие слоев:
Запрос → Routers → Services → Repository → Redis  
Ответ ← Routers ← Services ← Repository ← Redis

## Установка и запуск

### Локальная разработка

1.  Клонировать репозиторий:

``` bash
https://github.com/NEONAVT/link_tracker
cd link_tracker
```

2.  Установить Poetry (если не установлен):

``` bash
pip install poetry
```

3.  Установить зависимости:

``` bash
poetry install
```

4.  Настроить окружение — создать в корневой директории `.env` и
    заполнить переменные [**(см. раздел “Переменные окружения” ниже)**](#переменные-окружения).

5.  Установить и запустить сервер Redis локально 
https://redis-doc.netlify.app/docs/install/install-redis/  

Для Windows: https://redis-doc.netlify.app/docs/install/install-redis/install-redis-on-windows/  
Для MacOS: https://redis-doc.netlify.app/docs/install/install-redis/install-redis-on-mac-os/  

6. Запустить проект:
``` bash
make run
```
7. Откройте Swagger UI:
- http://127.0.0.1:8000/docs  

### Запуск Redis в Docker

1.  Создать файл `.env` и заполнить настройки [**(см. раздел “Переменные окружения” ниже)**](#переменные-окружения)

2.  Запустить контейнер:

``` bash
docker-compose up redis
```

3. Запустить проект:

``` bash
make run
```
4. Откройте Swagger UI:
- http://127.0.0.1:8000/docs  

Приложение будет запущено и готово к работе.

## Переменные окружения:

Для запуска бота необходимо создать в корневой директории проекта файл
`.env` со следующими переменными:

```
# Redis
CACHE_HOST=0.0.0.0
CACHE_PORT=6379
CACHE_DB=0

# Логирование
LOG_LEVEL=DEBUG
APP_NAME=link-tracker
ENVIRONMENT=development

# Sentry
SENTRY_DSN=your-SENTRY_DSN
```

## API

Базовый префикс роутера: **`/links-tracker`**.

### POST `/visited_links`

Добавляет ссылки. Сервер извлекает домены и сохраняет их с текущим Unix-временем.

**Request body**
```json
{
  "links": [
    "https://ya.ru",
    "https://ya.ru?q=123",
    "funbox.ru",
    "google.com/search?q=123",
    "http://example.com:8080/path"
  ]
}
```

**Response**
```json
{ "status": "ok" }
```

### GET `/visited_domains`

Возвращает уникальные домены за интервал.

**Query параметры**
- `from` *(int, required)* — начало интервала (Unix time, включительно)
- `to` *(int, required)* — конец интервала (Unix time, включительно)

**Пример**
```bash
curl "http://127.0.0.1:8000/links-tracker/visited_domains?from=1700000000&to=1800000000"
```

**Response**
```json
{
  "domains": ["example.com", "funbox.ru", "google.com", "ya.ru"],
  "status": "ok"
}
```

## Документация

С документацией проекта можно ознакомиться по команде:

``` bash
make open-docs
```

Это сгенерирует и откроет полную документацию по всем модулям проекта,
созданную с помощью pdoc.

## Контакты

Разработчик: Клим Клушин  
Email: klim.klushin@gmail.com  
Телефон: +7 978 661 59 23  
Telegram: [@klim_klushin](http://t.me/klim_klushin)  

