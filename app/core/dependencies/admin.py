from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.services.admin import UserDaoMgr
from app.core.utils import authx

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/admin/login")


async def get_current_user(token: str = Depends(oauth2_schema)):
    payload = authx.auth_manager._decode_token(token)
    user_id = payload.sub
    user = await UserDaoMgr.find(int(user_id))
    return user
