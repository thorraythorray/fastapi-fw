from fastapi import Depends, APIRouter

from app.admin.dependencies import encrypt_passwd
from app.admin.models import User
from app.admin.schemas import LoginSchema, RegisterSchema, UserSchema
from app.admin.service import UserManger
from app.auth import security_auth, verify_user
from app.errors import DuplicatedError

router = APIRouter()


@router.post("/login")
async def login(data: LoginSchema = Depends()):
    username = data.username
    password = data.password

    await verify_user(username, password)
    token = security_auth.create_access_token(uid=username)
    return {"access_token": token}


@router.post("/user", response_model=UserSchema, dependencies=[Depends(security_auth.access_token_required)])
async def create_user(schema: RegisterSchema = Depends(encrypt_passwd)):
    flag, _ = await UserManger.find(schema.name)
    if flag:
        raise DuplicatedError('用户名重复')
    return await User.create(**schema.model_dump())
