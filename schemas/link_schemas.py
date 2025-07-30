from pydantic import BaseModel
from typing import List


class LinksRequest(BaseModel):
    """
    Запрос для POST /visited_links.

    Attributes:
        links (List[str]): Список посещённых ссылок.
    """
    links: List[str]


class DomainsResponse(BaseModel):
    """
    Ответ для GET /visited_domains.

    Attributes:
        domains (List[str]): Список доменов.
        status (str): Статус выполнения, по умолчанию "ok".
    """
    domains: List[str]
    status: str = "ok"


class StatusResponse(BaseModel):
    """
    Универсальный ответ с информацией о статусе.

    Attributes:
        status (str): Статус выполнения, по умолчанию "ok".
    """
    status: str = "ok"
