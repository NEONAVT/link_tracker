# schemas/link_schemas.py
from pydantic import BaseModel
from typing import List


class LinksRequest(BaseModel):
    """
    Схема для POST /visited_links
    """
    links: List[str]


class DomainsResponse(BaseModel):
    """
    Схема для ответа GET /visited_domains
    """
    domains: List[str]
    status: str = "ok"


class StatusResponse(BaseModel):
    """
    Универсальный ответ об успехе
    """
    status: str = "ok"
