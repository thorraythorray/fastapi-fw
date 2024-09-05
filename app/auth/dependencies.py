from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

from app.auth.dao import UserDaoMgr
from app.utils.security import auth_manager


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):

    async def __call__(self, request: Request):
        payload = await auth_manager._auth_required(request)
        user_id = payload.sub
        user = await UserDaoMgr.find(int(user_id))
        request.state.user = user


oauth2_authentication = CustomOAuth2PasswordBearer(tokenUrl="/admin/login")
