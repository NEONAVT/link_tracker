from fastapi import APIRouter, Depends, Query
from exceptions import InvalidTimeRangeError
from schemas import LinksRequest, DomainsResponse, StatusResponse
from services.link_service import LinkService
from dependency import get_link_service


router = APIRouter(
    prefix="/links-tracker",
    tags=["Links Tracker"],
)


@router.post("/visited_links", response_model=StatusResponse)
def add_visited_links(
    request: LinksRequest,
    service: LinkService = Depends(get_link_service),
):
    service.add_visited_links(request.links)
    return {"status": "ok"}


@router.get("/visited_domains", response_model=DomainsResponse)
def get_visited_domains(
    from_time: int = Query(..., alias="from"),
    to_time: int = Query(...),
    service: LinkService = Depends(get_link_service),
):
    if from_time > to_time:
        raise InvalidTimeRangeError()
    domains = service.get_visited_domains(from_time, to_time)
    return {"domains": domains, "status": "ok"}
