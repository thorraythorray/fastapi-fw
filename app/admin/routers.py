from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_login import LoginManager
from fastapi import APIRouter
from tortoise import Tortoise

from app import settings
from app.admin.dependencies import register_user
from app.admin.models import User
from app.admin.schemas import UserRegisterSchema, UserSchema

router = APIRouter()


@router.post("/user", response_model=UserSchema)
async def create_user(data: dict = Depends(register_user)):
    print(data)
    user = await User.create(**data)
    return user


@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    # user = query_user(email)
    # if not user:
    #     # you can return any response or error of your choice
    #     raise InvalidCredentialsException
    # elif password != user["password"]:
    #     raise InvalidCredentialsException

    access_token = LoginManager.create_access_token(data={"username": username})
    return {"access_token": access_token}
