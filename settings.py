import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CACHE_HOST: str
    CACHE_PORT: int
    CACHE_DB: int

    # Автоматическое определение Docker-окружения
    @property
    def is_docker(self) -> bool:
        return os.path.exists("/.dockerenv")

    def get_redis_host(self):
        return "redis" if self.is_docker else self.CACHE_HOST

    # Логирование
    APP_NAME: str = "link-tracker"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


    # Sentry
    SENTRY_DSN: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()


