from typing import Any
from pydantic import BaseModel
from tortoise.queryset import QuerySet

from app.core.base import PaginationSchema
from app.core.types import T


class PaginatedResponse(PaginationSchema):
    total: int = 0
    items: list = []

    @classmethod
    async def from_queryset(
        cls,
        queryset: QuerySet,
        pydantic_model,
        page: int = 1,
        per_page: int = 10
    ) -> T:
        query_list = queryset.offset((page - 1) * per_page).limit(per_page).all()
        items = await pydantic_model.from_queryset(query_list)
        total = await queryset.count()
        return cls(total=total, items=items, page=page, per_page=per_page)


class SuccessResponseModel(BaseModel):
    code: int = 0
    msg: str = 'ok'
    data: Any = None


class FailedResponseModel(BaseModel):
    code: int = -1
    msg: str = 'failed'
