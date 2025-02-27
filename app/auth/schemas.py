from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, PositiveInt, model_validator

from app.auth.models import User, Role
from app.const import GENDER_TEXT_CONVERT, GenderEnum
from app.base import PaginationSchema


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


class PermissionSchema(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    code: str = Field(min_length=1, max_length=64)
    description: Optional[str] = None


class RoleSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=32)
    is_admin: bool = False
    permissions: List[int] = []  # permission ids
    user_count: Optional[int] = 0

    @model_validator(mode='before')
    def get_related_info(cls, values):
        if isinstance(values, Role):
            # 如果users已预加载，直接计算长度
            if hasattr(values, 'users'):
                values.user_count = len(values.users)
            # 如果permissions已预加载，提取权限ID列表
            if hasattr(values, 'permissions'):
                values.permissions = [p.id for p in values.permissions]
        return values
