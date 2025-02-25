from typing import Optional, Tuple, Union

from app.auth.models import User
from app.auth.schemas import RegisterSchema, UserQuerySchema
from app.exceptions import AuthError, AuthForbbiden, DuplicatedError
from app.utils.crypto import hash_algorithm


class UserDaoMgr:

    @classmethod
    async def create(cls, user_info: RegisterSchema) -> User:
        user_dict = user_info.model_dump()
        password = user_dict.pop('password')
        user_dict["password"] = hash_algorithm(password)
        user = await cls.find(user_info.name)
        if user:
            raise DuplicatedError('用户重复')
        return await User.create(**user_dict)

    @staticmethod
    async def find(sth: Union[int, str]) -> Tuple[bool, Optional[User]]:
        query = {}
        if isinstance(sth, int):
            query["id"] = sth
        else:
            query["name"] = sth
        try:
            user = await User.filter(**query)
        except User.DoesNotExist:
            return None
        return user

    @staticmethod
    async def verify_user(username: str, password: str) -> User:
        user = await User.filter(name=username).first()
        if not user:
            raise AuthError('用户不存在')

        if not user.verify_password(password):
            raise AuthForbbiden('密码错误')
        return user

    @staticmethod
    async def list(query_schema: UserQuerySchema) -> dict:
        query_dict = query_schema.model_dump()
        page = query_dict.pop('page')
        size = query_dict.pop('size')
        users = await User.filter(**query_dict).all().limit(size).offset((page - 1) * size)
        return dict(items=users, page=page, size=size)
