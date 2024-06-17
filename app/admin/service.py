from typing import Optional, Tuple, Union

from app.admin.models import User


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
