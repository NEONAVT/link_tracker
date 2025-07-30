import logging
import os
from logging.handlers import RotatingFileHandler
from settings import settings

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(settings.LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=100 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)