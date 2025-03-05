from pydantic import BaseModel, Field
from tortoise.queryset import QuerySet

from app.model import T


class PageModel(BaseModel):
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=10, ge=1)


class PaginatedResponse(PageModel):
    total: int = 0
    items: list = []

    @classmethod
    async def from_queryset(
        cls,
        queryset: QuerySet,
        pydantic_model: BaseModel,
        page: int = 1,
        per_page: int = 10
    ) -> T:
        query_list = queryset.offset((page - 1) * per_page).limit(per_page).all()
        items = await pydantic_model.from_queryset(query_list)
        total = await queryset.count()
        return cls(total=total, items=items, page=page, per_page=per_page)
