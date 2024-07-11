from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, PositiveInt

from app.core.base.enum import Gender
from app.core.schemas.pagination import PaginationSchema


class UserSchema(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    email: EmailStr = Field(..., example="default@example.com")
    phone: Optional[str] = None

    age: PositiveInt = 1
    sex: Gender = Gender.unkown

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
