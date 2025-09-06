"""
Содержит функции и объекты, предоставляющие доступ к базам данных.
В текущей реализации экспортируется:

- `get_redis_connection` — фабричная функция для подключения к Redis.
"""
from database.redis_accessor import get_redis_connection

__all__ = ["get_redis_connection",]
