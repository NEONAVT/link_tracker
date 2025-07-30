from fastapi import APIRouter, Depends, Query
from exceptions import InvalidTimeRangeError
from schemas import LinksRequest, DomainsResponse, StatusResponse
from services.link_service import LinkService
from dependency import get_link_service


router = APIRouter(
    prefix="/links-tracker",
    tags=["Links Tracker"],
)
"""
API маршруты для трекера посещённых ссылок.

- POST /visited_links: добавление посещённых ссылок.
- GET /visited_domains: получение посещённых доменов за интервал времени.
"""


@router.post("/visited_links", response_model=StatusResponse)
def add_visited_links(
    request: LinksRequest,
    service: LinkService = Depends(get_link_service),
):
    """
    Добавляет посещённые ссылки.

    Args:
        request (LinksRequest): Входные данные с ссылками.
        service (LinkService): Сервис для обработки логики.

    Returns:
        dict: Статус выполнения.
    """
    service.add_visited_links(request.links)
    return {"status": "ok"}


@router.get("/visited_domains", response_model=DomainsResponse)
def get_visited_domains(
    from_time: int = Query(..., alias="from"),
    to_time: int = Query(...),
    service: LinkService = Depends(get_link_service),
):
    """
    Возвращает посещённые домены за заданный интервал.

    Args:
        from_time (int): Начало временного интервала.
        to_time (int): Конец временного интервала.
        service (LinkService): Сервис для получения данных.

    Raises:
        InvalidTimeRangeError: Если from_time больше to_time.

    Returns:
        dict: Список доменов и статус.
    """
    if from_time > to_time:
        raise InvalidTimeRangeError()
    domains = service.get_visited_domains(from_time, to_time)
    return {"domains": domains, "status": "ok"}
