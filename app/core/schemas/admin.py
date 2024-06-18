from typing import Optional
from pydantic import BaseModel, EmailStr, Field, PositiveInt


class LoginSchema(BaseModel):
    username: str
    password: str
    code: Optional[str] = None  # Optional[X] is equivalent to Union[X, None].


class UserSchema(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    email: str = EmailStr

    age: PositiveInt = 1
    sex: int = Field(ge=0, le=2, default=0)

    avatar: Optional[str] = None
    role: Optional[int] = None
    phone: Optional[str] = None


class RegisterSchema(UserSchema):
    passwd: Optional[str] = None


class RoleSchema(BaseModel):
    name: str = Field(max_length=32)
