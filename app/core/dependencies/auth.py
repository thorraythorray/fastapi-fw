from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

from app.core.services.admin import UserDaoMgr
from app.core.security import auth_manager
from app.core.log import logger


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):

    async def __call__(self, request: Request):
        payload = await auth_manager._auth_required(request)
        user_id = payload.sub
        logger.info(user_id)
        user = await UserDaoMgr.find(int(user_id))
        request.state.user = user


oauth2_authentication = CustomOAuth2PasswordBearer(tokenUrl="/admin/login")
