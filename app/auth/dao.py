from typing import Optional, Tuple, Union, List

from app.auth.models import User, Role, Permission
from app.auth.schemas import RegisterSchema, UserQuerySchema, PermissionSchema, RoleSchema
from app.exceptions import (
    AuthError,
    AuthForbbiden,
    DuplicatedError,
    ResourceInUseError,
    NotFound
)
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


class PermissionDaoMgr:
    @staticmethod
    async def create(permission_info: PermissionSchema) -> Permission:
        # 只检查code是否重复
        if await Permission.filter(code=permission_info.code).exists():
            raise DuplicatedError('权限标识符已存在')
        return await Permission.create(**permission_info.model_dump())

    @staticmethod
    async def list() -> List[Permission]:
        return await Permission.all()

    @staticmethod
    async def delete(permission_id: int) -> None:
        try:
            permission = await Permission.get(id=permission_id).prefetch_related('roles')
        except Permission.DoesNotExist:
            raise NotFound('权限不存在')

        if permission.roles:
            raise ResourceInUseError('无法删除权限：该权限仍被角色使用中')
        await permission.delete()


class RoleDaoMgr:
    @staticmethod
    async def create(role_info: RoleSchema) -> Role:
        # 检查角色名是否重复
        if await Role.filter(name=role_info.name).exists():
            raise DuplicatedError('角色名称已存在')

        role_dict = role_info.model_dump()
        permission_ids = role_dict.pop('permissions', [])
        role = await Role.create(**role_dict)
        if permission_ids:
            permissions = await Permission.filter(id__in=permission_ids)
            await role.permissions.add(*permissions)
        return role

    @staticmethod
    async def get_permissions(role_id: int) -> List[Permission]:
        role = await Role.get(id=role_id).prefetch_related('permissions')
        return role.permissions

    @staticmethod
    async def update_permissions(role_id: int, permission_ids: List[int]) -> None:
        role = await Role.get(id=role_id)
        permissions = await Permission.filter(id__in=permission_ids)
        await role.permissions.clear()
        if permissions:
            await role.permissions.add(*permissions)

    @staticmethod
    async def delete(role_id: int) -> None:
        try:
            role = await Role.get(id=role_id).prefetch_related('users')
        except Role.DoesNotExist:
            raise NotFound('角色不存在')

        if role.users:
            raise ResourceInUseError('无法删除角色：该角色仍被用户使用中')
        await role.permissions.clear()
        await role.delete()

    @staticmethod
    async def list() -> List[Role]:
        return await Role.all().prefetch_related('users', 'permissions')
