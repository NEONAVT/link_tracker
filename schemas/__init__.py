"""
Содержит Pydantic-схемы для сериализации и валидации данных,
используемых в API.

Экспортируемые объекты:
- `LinksRequest` — схема запроса для добавления ссылок.
- `DomainsResponse` — схема ответа со списком уникальных доменов.
- `StatusResponse` — схема ответа со статусом выполнения операции.
"""
from schemas.link_schemas import LinksRequest, DomainsResponse, StatusResponse

__all__ = ["LinksRequest", "DomainsResponse", "StatusResponse",]
