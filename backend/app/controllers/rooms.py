from datetime import date
from typing import Annotated, Literal

from litestar import Controller, get
from litestar.exceptions import HTTPException
from litestar.params import Parameter

from app.config import settings
from app.schema.booking import RoomsWithStatusResponse
from app.schema.list_query import RoomListFilter, RoomListQuery, RoomListSort
from app.services.room_catalog_service import RoomCatalogService


class RoomsController(Controller):
    path = "/rooms"

    @get("/", sync_to_thread=False)
    def list(
        self,
        room_catalog_service: RoomCatalogService,
        date: Annotated[
            date | None,
            Parameter(query="date", required=False),
        ] = None,
        sort_by: Annotated[
            Literal["sort_order", "room_number", "name"],
            Parameter(query="sort_by", required=False),
        ] = "sort_order",
        sort_dir: Annotated[
            Literal["asc", "desc"],
            Parameter(query="sort_dir", required=False),
        ] = "asc",
    ) -> RoomsWithStatusResponse:
        query = RoomListQuery(
            filter=RoomListFilter(booking_date=date),
            sort=RoomListSort(sort_by=sort_by, sort_order=sort_dir),
        )
        try:
            day, rooms = room_catalog_service.list(query)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return RoomsWithStatusResponse(date=day, timezone=settings.app_timezone, rooms=rooms)
