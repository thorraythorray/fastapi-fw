from typing import Optional
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str
    code: Optional[str]  # Optional[X] is equivalent to Union[X, None].
