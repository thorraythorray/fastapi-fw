from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, PositiveInt, model_validator

from app.core.base.enum import GenderEnum
from app.core.schemas.pagination import PaginationSchema
from app.core.log import logger


class UserSchema(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    email: EmailStr = Field(..., example="default@example.com")
    phone: Optional[str] = None

    age: PositiveInt = 1
    sex: GenderEnum = GenderEnum.unkown.value

    avatar: Optional[str] = None


class RegisterSchema(UserSchema):
    role: Optional[int] = None
    password: str


class UserQuerySchema(PaginationSchema):
    pass


class UsersPagitionSchema(PaginationSchema):
    items: List[UserSchema] = []


class RoleSchema(BaseModel):
    name: str = Field(max_length=32)
