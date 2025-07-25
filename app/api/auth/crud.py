import traceback
from typing import Optional, Union, List

from tortoise.exceptions import DoesNotExist

from app.api.auth.models import User, Role, Permission
from app.api.auth.schemas import (
    RoleCreateModel,
    RoleInfoModel,
    RoleQueryModel,
    UserCreateModel,
    UserEditModel,
    UserInfoModel,
    UserQueryModel,
)
from app.settings import AuthError, AuthForbbiden, ConflictError, ResourceInUseError, NotFound
from app.settings import T
from app.settings import PaginatedResponse
from app.settings import hash_algorithm


class UserDaoMgr:

    @classmethod
    async def create(cls, user_model: UserCreateModel) -> User:
        user = await cls.find(user_model.name)
        if user:
            raise ConflictError('用户已存在')

        password = user_model.password
        user_model.password = hash_algorithm.hash(password)
        return await User.create(**user_model.model_dump())


    @classmethod
    async def patch(cls, user_id: int, user_model: UserEditModel):
        user = await cls.find(user_id)
        if not user:
            raise NotFound('用户不存在')

        if user_model.password:
            password = user_model.password
            user_model.password = hash_algorithm.hash(password)
        await user.update(**user_model.model_dump())

    @staticmethod
    async def find(query: Union[int, str]) -> Optional[User]:
        cond = {}
        if isinstance(query, int):
            cond["id"] = query
        else:
            cond["name"] = query
        return await User.filter(**cond).first()

    @staticmethod
    async def authenticate(username: str, password: str) -> User:
        user = await User.filter(name=username).first()
        if not user:
            raise AuthError('用户不存在')

        if not user.verify_password(password):
            raise AuthForbbiden('密码错误')
        return user

    @staticmethod
    async def list(query_schema: UserQueryModel) -> T:
        query_dict = query_schema.model_dump()
        page = query_dict.pop('page')
        per_page = query_dict.pop('per_page')
        queryset = User.filter(**query_dict).select_related('role').order_by('-id')
        return await PaginatedResponse.from_queryset(queryset, UserInfoModel, page=page, per_page=per_page)

    @classmethod
    async def delete(cls, user_id: int):
        user = await cls.find(user_id)
        if not user:
            raise NotFound('用户不存在')
        await user.delete()


class RoleDaoMgr:
    @staticmethod
    async def create(role_info: RoleCreateModel) -> Role:
        if await Role.filter(name=role_info.name).exists():
            raise ConflictError('角色名称已存在')

        role_dict = role_info.model_dump()
        permission_ids = role_dict.pop('permissions', [])
        role = await Role.create(**role_dict)
        if permission_ids:
            permissions = await Permission.filter(id__in=permission_ids)
            await role.permissions.add(*permissions)
        return role

    @staticmethod
    async def get_permissions(role_id: int) -> List:
        permissions = await Permission.filter(
            roles__id=role_id, parent=None
        ).prefetch_related('children').all()
        result = []
        for perm in permissions:
            result.append(await perm.trees())
        return result

    @staticmethod
    async def update_permissions(role_id: int, permission_ids: List[int]):
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
        await role.delete()

    @staticmethod
    async def list(query_schema: RoleQueryModel) -> T:
        query_dict = query_schema.model_dump()
        page = query_dict.pop('page')
        per_page = query_dict.pop('per_page')
        queryset = Role.filter(**query_dict).prefetch_related('permissions')
        return await PaginatedResponse.from_queryset(queryset, RoleInfoModel, page=page, per_page=per_page)


class PermissionDaoMgr:
    @staticmethod
    async def create(permission_info) -> Permission:
        if await Permission.filter(code=permission_info.code).exists():
            raise ConflictError('权限标识符已存在')
        return await Permission.create(**permission_info.model_dump())

    @staticmethod
    async def list() -> List:
        permissions = await Permission.filter(parent=None).prefetch_related('children').all()
        result = []
        for perm in permissions:
            result.append(await perm.trees())
        return result

    @staticmethod
    async def delete(permission_id: int) -> None:
        try:
            permission = await Permission.get(id=permission_id).prefetch_related('roles')
        except DoesNotExist:
            raise NotFound('权限不存在')

        if permission.roles:
            raise ResourceInUseError('无法删除权限：该权限仍被角色使用中')
        await permission.delete()
