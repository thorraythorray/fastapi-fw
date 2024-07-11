from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies.admin import get_current_user
from app.core.schemas.admin import RegisterSchema, UserQuerySchema, UserSchema, \
    UsersPagitionSchema
from app.core.services.admin import UserDaoMgr
from app.core.utils.authx import auth_manager

router = APIRouter()


@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = await UserDaoMgr.verify_user(username, password)
    token = auth_manager.create_access_token(uid=str(user.id))
    return {"access_token": token}


@router.get("/me", dependencies=[Depends(auth_manager.access_token_required)])
async def read_me(current_user: UserSchema = Depends(get_current_user)):
    return 'ok'


@router.post("/user", response_model=UserSchema, dependencies=[Depends(auth_manager.access_token_required)])
async def create_user(data: RegisterSchema):
    return await UserDaoMgr.create(data)


@router.get("/users", response_model=UsersPagitionSchema, dependencies=[Depends(auth_manager.access_token_required)])
async def user_list(query_schema: UserQuerySchema = Depends()):
    user_list = await UserDaoMgr.list(query_schema)
    return {"items": user_list}
