from typing import Optional
from pydantic import BaseModel, EmailStr, Field, PositiveInt, SecretStr


class LoginRequest(BaseModel):
    username: str
    password: str
    code: Optional[str]  # Optional[X] is equivalent to Union[X, None].


class UserSchema(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    email: str = EmailStr

    age: PositiveInt = 1
    sex: int = Field(ge=0, le=2, default=0)

    avatar: Optional[str] = None
    role: Optional[int] = None
    phone: Optional[str] = None
    passwd: Optional[str] = None


class UserRegisterSchema(UserSchema):
    pass


class RoleSchema(BaseModel):
    name: str = Field(max_length=32)
