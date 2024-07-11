from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, PositiveInt, model_validator

from app.core.base.enum import GENDER_TEXT_CONVERT, GenderEnum
from app.core.models.admin import User
from app.core.schemas.pagination import PaginationSchema
from app.core.log import logger


class UserBaseSchema(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    email: EmailStr = Field(..., example="default@example.com")
    phone: Optional[str] = None
    sex: GenderEnum = GenderEnum.unkown.value
    age: PositiveInt = 18
    avatar: Optional[str] = None


class UserInfoSchema(UserBaseSchema):
    sex_text: Optional[str] = None
    role_info: dict = {}

    @model_validator(mode='after')
    def get_sex_text(cls, values):
        sex_text = GENDER_TEXT_CONVERT.get(values.sex)
        values.sex_text = sex_text
        return values

    @model_validator(mode='before')
    def get_role_info(cls, values):
        if isinstance(values, User):
            if values.role:
                values.role_info = RoleSchema(name=values.role.name).model_dump()
        return values


class RegisterSchema(UserBaseSchema):
    role: Optional[int] = None
    password: str


class UserQuerySchema(PaginationSchema):
    pass


class UsersPagitionSchema(PaginationSchema):
    items: List[UserInfoSchema] = []


class RoleSchema(BaseModel):
    name: str = Field(max_length=32)
