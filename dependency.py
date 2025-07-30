from fastapi import Depends
from redis import Redis, RedisError
from database import get_redis_connection
from exceptions import RedisConnectionError
from repository.link_repository import LinkRepository
from services.link_service import LinkService


def get_redis() -> Redis:
    try:
        return get_redis_connection()
    except RedisError:
        raise RedisConnectionError()


def get_link_repository(redis: Redis = Depends(get_redis)) -> LinkRepository:
    return LinkRepository(redis)


def get_link_service(
    repository: LinkRepository = Depends(get_link_repository),
) -> LinkService:
    return LinkService(repository)
