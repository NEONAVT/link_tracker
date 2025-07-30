from fastapi import Depends
from redis import Redis, RedisError
from database import get_redis_connection
from exceptions import RedisConnectionError
from repository.link_repository import LinkRepository
from services.link_service import LinkService


def get_redis() -> Redis:
    """
    Получает соединение с Redis.

    Возвращает объект Redis из функции `get_redis_connection`.

    Raises:
        RedisConnectionError: При ошибке подключения к Redis.
    """
    try:
        return get_redis_connection()
    except RedisError:
        raise RedisConnectionError()


def get_link_repository(redis: Redis = Depends(get_redis)) -> LinkRepository:
    """
    Возвращает экземпляр LinkRepository.

    Args:
        redis (Redis): Клиент Redis, полученный через Depends.

    Returns:
        LinkRepository: Репозиторий для работы с доменами.
    """
    return LinkRepository(redis)


def get_link_service(
    repository: LinkRepository = Depends(get_link_repository),
) -> LinkService:
    """
    Возвращает экземпляр LinkService.

    Args:
        repository (LinkRepository): Репозиторий, полученный через Depends.

    Returns:
        LinkService: Сервис для обработки логики ссылок.
    """
    return LinkService(repository)
