FROM python:3.12-slim

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Установка переменных среды
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Создание рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY pyproject.toml poetry.lock* /app/

# Установка зависимостей
RUN poetry install --no-root

# Копирование исходников
COPY . /app

# Запуск Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
