import redis
from settings import settings
import logging

logger = logging.getLogger(__name__)

def get_redis_connection() -> redis.Redis:
    try:
        logger.debug(f"Connecting to Redis at {settings.get_redis_host()}:{settings.CACHE_PORT}")
        connection = redis.Redis(
            host=settings.get_redis_host(),
            port=settings.CACHE_PORT,
            db=settings.CACHE_DB,
        )
        connection.ping()  # Проверка соединения
        logger.info("Redis connection established")
        return connection
    except Exception as e:
        logger.error(f"Redis connection error: {str(e)}")
        raise