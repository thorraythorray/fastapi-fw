from typing import Optional
from pydantic import BaseModel, EmailStr, Field, PositiveInt


class LoginRequest(BaseModel):
    username: str
    password: str
    code: Optional[str]  # Optional[X] is equivalent to Union[X, None].


class User(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    email: str = EmailStr
    phone: Optional[str]

    age: Optional[PositiveInt] = Field(ge=1, le=100)
    sex: Optional[PositiveInt] = Field(ge=0, le=2)
    avatar: Optional[str]
    role: int


class Role(BaseModel):
    name: str = Field(max_length=32)
