from typing import Optional, Tuple, Union

from app.core.errors import AuthError, AuthForbbiden
from app.core.models.admin import User


class UserManger:

    @staticmethod
    async def find(sth: Union[int, str]) -> Tuple[bool, Optional[User]]:
        query = {}
        if isinstance(sth, int):
            query["id"] = sth
        elif isinstance(sth, str):
            query["name"] = sth
        else:
            raise ValueError
        try:
            user = await User.filter(**query)
        except User.DoesNotExist:
            return False, None
        return True, user

    @staticmethod
    async def verify_user(username: str, password: str):
        user = await User.filter(name=username).first()
        if not user:
            raise AuthError('用户不存在')

        if not user.verify_password(password):
            raise AuthForbbiden('密码错误')
