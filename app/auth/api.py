from fastapi import Depends, APIRouter, Request, logger
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import PlainTextResponse

from app.auth.dao import UserDaoMgr
from app.auth.schemas import RegisterSchema, UserInfoSchema, UserQuerySchema, UsersPagitionSchema
from app.auth.dependencies import oauth2_authentication
from app.utils.security import auth_manager

router = APIRouter(tags=["Auth"])


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


@router.post("/user", response_model=UserInfoSchema, dependencies=[Depends(oauth2_authentication)])
async def create_user(data: RegisterSchema):
    return await UserDaoMgr.create(data)


@router.get("/users", response_model=UsersPagitionSchema, dependencies=[Depends(oauth2_authentication)])
async def user_list(query_schema: UserQuerySchema = Depends()):
    return await UserDaoMgr.list(query_schema)
