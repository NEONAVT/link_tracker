import redis
from exceptions import RedisConnectionError
from settings import settings
import logging


logger = logging.getLogger(__name__)


def get_redis_connection() -> redis.Redis:
    """
    Устанавливает и возвращает соединение с Redis.

    Использует параметры хоста, порта и номера базы данных из конфигурации
    `settings`. Выполняет команду PING для проверки соединения.

    Returns:
        redis.Redis: Объект соединения с Redis.

    Raises:
        RedisConnectionError: Если не удалось подключиться к Redis.
    """
    try:
        logger.debug(f"Connecting to Redis at "
                     f"{settings.get_redis_host()}:{settings.CACHE_PORT}")
        connection = redis.Redis(
            host=settings.get_redis_host(),
            port=settings.CACHE_PORT,
            db=settings.CACHE_DB,
        )
        connection.ping()  # Проверка соединения
        logger.info("Redis connection established")
        return connection
    except Exception as e:
        raise RedisConnectionError() from e
