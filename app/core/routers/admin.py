from fastapi import Depends, APIRouter

from app.core.dependencies.admin import encrypt_passwd
from app.core.models.admin import User
from app.core.schemas.admin import LoginSchema, RegisterSchema, UserSchema
from app.core.services.admin import UserManger
from app.core.errors import DuplicatedError
from app.core.utils.authx import auth_manager

router = APIRouter()


@router.post("/login")
async def login(data: LoginSchema = Depends()):
    username = data.username
    password = data.password

    await UserManger.verify_user(username, password)
    token = auth_manager.create_access_token(uid=username)
    return {"access_token": token}


@router.post("/user", response_model=UserSchema, dependencies=[Depends(auth_manager.access_token_required)])
async def create_user(schema: RegisterSchema = Depends(encrypt_passwd)):
    flag, _ = await UserManger.find(schema.name)
    if flag:
        raise DuplicatedError('用户名重复')
    return await User.create(**schema.model_dump())
