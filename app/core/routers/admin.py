from fastapi import Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import PlainTextResponse

from app.core.dependencies.auth import oauth2_authentication
from app.core.schemas.admin import RegisterSchema, UserQuerySchema, UserSchema, \
    UsersPagitionSchema
from app.core.services.admin import UserDaoMgr
from app.core.security import auth_manager
from app.core.log import logger

router = APIRouter()


@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = await UserDaoMgr.verify_user(username, password)
    token = auth_manager.create_access_token(uid=str(user.id))
    return {"access_token": token}


@router.get("/me", dependencies=[Depends(oauth2_authentication)])
async def read_me(request: Request):
    logger.info(request.state.user)
    return PlainTextResponse('ok')


@router.post("/user", response_model=UserSchema, dependencies=[Depends(oauth2_authentication)])
async def create_user(data: RegisterSchema):
    return await UserDaoMgr.create(data)


@router.get("/users", response_model=UsersPagitionSchema, dependencies=[Depends(oauth2_authentication)])
async def user_list(query_schema: UserQuerySchema = Depends()):
    user_list = await UserDaoMgr.list(query_schema)
    return {"items": user_list}
