from fastapi import Depends, APIRouter, Request, logger
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import PlainTextResponse
from typing import List

from app.auth.dao import UserDaoMgr, PermissionDaoMgr, RoleDaoMgr
from app.auth.schemas import RegisterSchema, UserInfoSchema, UserQuerySchema, UsersPagitionSchema, PermissionSchema, RoleSchema
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


@router.post("/permission",
    response_model=PermissionSchema,
    dependencies=[Depends(oauth2_authentication)]
)
async def create_permission(data: PermissionSchema):
    """创建权限"""
    return await PermissionDaoMgr.create(data)


@router.get("/permissions",
    response_model=List[PermissionSchema],
    dependencies=[
        Depends(oauth2_authentication),
    ]
)
async def permission_list():
    """获取权限列表"""
    return await PermissionDaoMgr.list()


@router.post("/role",
    response_model=RoleSchema,
    dependencies=[Depends(oauth2_authentication)],
)
async def create_role(data: RoleSchema):
    """创建角色"""
    return await RoleDaoMgr.create(data)


@router.get("/role/{role_id}/permissions",
    response_model=List[PermissionSchema],
    dependencies=[Depends(oauth2_authentication)]
)
async def role_permissions(role_id: int):
    """获取角色的权限列表"""
    return await RoleDaoMgr.get_permissions(role_id)


@router.put("/role/{role_id}/permissions", dependencies=[Depends(oauth2_authentication)])
async def update_role_permissions(role_id: int, permission_ids: List[int]):
    """更新角色的权限"""
    return await RoleDaoMgr.update_permissions(role_id, permission_ids)


@router.delete("/role/{role_id}", dependencies=[Depends(oauth2_authentication)])
async def delete_role(role_id: int):
    """删除角色"""
    await RoleDaoMgr.delete(role_id)
    return {"message": "角色删除成功"}


@router.delete("/permission/{permission_id}", dependencies=[Depends(oauth2_authentication)])
async def delete_permission(permission_id: int):
    """删除权限"""
    await PermissionDaoMgr.delete(permission_id)
    return {"message": "权限删除成功"}


@router.get("/roles", response_model=List[RoleSchema], dependencies=[Depends(oauth2_authentication)])
async def role_list():
    """获取角色列表"""
    return await RoleDaoMgr.list()
