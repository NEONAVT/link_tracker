from fastapi import HTTPException
from fastapi import status
import logging

logger = logging.getLogger(__name__)


class InvalidTimeRangeError(HTTPException):
    """
    Исключение для некорректного временного интервала.

    Возвращает HTTP 400 Bad Request с сообщением, что 'from' должен быть
    меньше либо равен 'to'.
    """
    def __init__(self):
        logger.warning("Invalid time range provided")
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parameter 'from' must be less than or equal to 'to'"
        )


class DomainValidationError(HTTPException):
    """
    Исключение для недопустимого формата URL.

    Возвращает HTTP 422 Unprocessable Entity с указанием неверного URL.
    """
    def __init__(self, invalid_url: str):
        logger.warning(f"Invalid URL format: {invalid_url}")
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid URL format: {invalid_url}"
        )


class RedisConnectionError(HTTPException):
    """
    Исключение при ошибке подключения к Redis.

    Возвращает HTTP 503 Service Unavailable с сообщением о недоступности Redis.
    """
    def __init__(self):
        logger.error("Redis connection failed")
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not connect to Redis database"
        )
