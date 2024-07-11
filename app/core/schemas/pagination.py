from fastapi import Query
from pydantic import BaseModel, Field


class PaginationSchema(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1)


class PaginateQuerySchema(BaseModel):
    page: int = Query(1, ge=1)
    size: int = Query(10, ge=1)
