import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CACHE_HOST: str
    CACHE_PORT: int
    CACHE_DB: int

    @property
    def is_docker(self) -> bool:
        """
        Определяет, запущено ли приложение в Docker.

        Returns:
            bool: True если в Docker, иначе False.
        """
        return os.path.exists("/.dockerenv")

    def get_redis_host(self) -> str:
        """
        Возвращает хост Redis с учётом среды выполнения.

        Если в Docker — возвращает 'redis', иначе значение из
        CACHE_HOST.

        Returns:
            str: Хост Redis.
        """
        return "redis" if self.is_docker else self.CACHE_HOST

    # Логирование
    APP_NAME: str = "link-tracker"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    # Sentry
    SENTRY_DSN: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
