"""
Собирает и предоставляет доступ к роутерам FastAPI,
которые описывают HTTP-эндпоинты сервиса.

Экспортируемые объекты:
- `link_tracker_router` — роутер с обработчиками запросов
  для работы со ссылками (добавление и получение доменов).
"""
from routers.link_tracker import router as link_tracker_router

__all__ = ["link_tracker_router"]
