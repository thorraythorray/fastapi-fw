from typing import List
from fastapi import Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth.crud import PermissionDaoMgr, RoleDaoMgr, UserDaoMgr
from app.api.auth.schemas import (
    PermCreateModel,
    RoleCreateModel,
    RoleQueryModel,
    UserCreateModel,
    UserEditModel,
    UserInfoModel,
    UserQueryModel,
)
from app.settings import oauth2_authentication
from app.settings import auth_manager

router = APIRouter(prefix='/api/admin', tags=["Auth"])


@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    user = await UserDaoMgr.authenticate(data.username, data.password)
    token = auth_manager.create_access_token(uid=str(user.id))
    return {"access_token": token}


@router.get("/me", dependencies=[Depends(oauth2_authentication)])
async def read_me(request: Request):
    user = request.state.user
    if isinstance(user, list):
        user = user[0]
    return await UserInfoModel.from_tortoise_orm(user)


@router.post("/user", dependencies=[Depends(oauth2_authentication)])
async def create_user(data: UserCreateModel):
    return await UserDaoMgr.create(data)


@router.patch("/user/{user_id}", dependencies=[Depends(oauth2_authentication)])
async def patch_user(user_id: int, data: UserEditModel):
    return await UserDaoMgr.patch(user_id, data)


@router.get("/users", dependencies=[Depends(oauth2_authentication)])
async def user_list(query_schema: UserQueryModel = Depends()):
    return await UserDaoMgr.list(query_schema)


@router.delete("/user/{user_id}", dependencies=[Depends(oauth2_authentication)])
async def user_list(user_id: int):
    return await UserDaoMgr.delete(user_id)


# Role
@router.post("/role", dependencies=[Depends(oauth2_authentication)])
async def create_role(data: RoleCreateModel):
    """创建角色"""
    return await RoleDaoMgr.create(data)


@router.get("/role/{role_id}/permissions", dependencies=[Depends(oauth2_authentication)])
async def role_permissions(role_id: int):
    """获取角色的权限列表"""
    return await RoleDaoMgr.get_permissions(role_id)


@router.get("/roles", dependencies=[Depends(oauth2_authentication)])
async def role_list(query: RoleQueryModel = Depends()):
    """获取角色列表"""
    return await RoleDaoMgr.list(query)


@router.put("/role/{role_id}/permissions", dependencies=[Depends(oauth2_authentication)])
async def update_role_permissions(role_id: int, permission_ids: List[int]):
    """更新角色的权限"""
    return await RoleDaoMgr.update_permissions(role_id, permission_ids)


@router.delete("/role/{role_id}", dependencies=[Depends(oauth2_authentication)])
async def delete_role(role_id: int):
    """删除角色"""
    return await RoleDaoMgr.delete(role_id)


# Permission
@router.post("/permission", dependencies=[Depends(oauth2_authentication)])
async def create_permission(data: PermCreateModel):
    """创建权限"""
    return await PermissionDaoMgr.create(data)


@router.get("/permissions", dependencies=[Depends(oauth2_authentication)])
async def permission_list():
    """获取权限列表"""
    return await PermissionDaoMgr.list()


@router.delete("/permission/{permission_id}", dependencies=[Depends(oauth2_authentication)])
async def delete_permission(permission_id: int):
    """删除权限"""
    return await PermissionDaoMgr.delete(permission_id)
