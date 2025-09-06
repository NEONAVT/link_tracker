"""
Входная точка приложения FastAPI.

Настраивает логирование, инициализирует приложение,
регистрирует маршруты и интегрирует Sentry при наличии DSN.
"""
from fastapi import FastAPI
from log_config.sentry_config import setup_sentry
from routers import link_tracker_router
from log_config import logging_config
from settings import settings

logging_config.setup_logging()

app = FastAPI()

app.include_router(link_tracker_router)

if settings.SENTRY_DSN:
    app = setup_sentry(app)
