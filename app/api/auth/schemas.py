from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, model_validator
from tortoise.contrib.pydantic import pydantic_model_creator

from app.api.auth.models import GENDER_TEXT_CONVERT, Permission, Role, User
from app.core.base import PaginationSchema


UserBaseModel = pydantic_model_creator(User, exclude=("password",))
RoleBaseModel = pydantic_model_creator(Role)
PermBaseModel = pydantic_model_creator(Permission, include=("id", "name", "code"))


class PermInfoModel(PermBaseModel):
    pass


class RoleInfoModel(RoleBaseModel):
    pass


class UserInfoModel(UserBaseModel):
    role: Optional[RoleInfoModel]
    sex_label: Optional[str]

    @model_validator(mode='before')
    def get_sex_label(cls, values):
        sex_label = GENDER_TEXT_CONVERT.get(values.sex)
        values.sex_label = sex_label
        return values


class UserEditModel(BaseModel):
    role_id: Optional[int] = None
    password: Optional[str] = None


class UserCreateModel(UserEditModel):
    name: str = Field(min_length=1, max_length=64)
    email: EmailStr = Field(..., example="default@example.com")
    phone: Optional[str] = '19811999911'


class UserQueryModel(PaginationSchema):
    pass


class RoleCreateModel(BaseModel):
    name: str = Field(max_length=32)
    is_admin: bool = False
    permissions: List[int] = []


class RoleQueryModel(PaginationSchema):
    pass


class PermCreateModel(BaseModel):
    name: str = Field(max_length=32)
    code: str = None
    parent_id: int = None


class PermQueryModel(PaginationSchema):
    pass
