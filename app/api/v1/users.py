from re import A

from fastapi import APIRouter, Depends, status
from app.services.users.users_service import UserService
from app.services.users.role_service import RoleService
from app.schemas.user_schems import LoginRequest, UserCreateOrUpdate, UserRoleCreateOrUpdate
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.core.security import get_password_hash
from time import sleep
from app.api.deps import get_current_user
user_router = APIRouter()


@user_router.post("/login", response_model=BaseResponse, summary="用户登录")
async def user_login(request: LoginRequest):
    """
    用户登录
    - **login_request**: 用户名和密码
    - **return**: 用户信息和token
    """
    result = await UserService.user_login(request)
    sleep(1)
    return ResponseUtil.success(data=result, msg="登录成功")


@user_router.post("/hash", response_model=BaseResponse, summary="查看hash密码")
async def hash_password(password: str):
    """
    查看hash密码，测试接口
    """
    return ResponseUtil.success(data=get_password_hash(password), msg="密码已加密")


@user_router.get("", response_model=BaseResponse, summary="获取用户列表")
async def get_users(current_user=Depends(get_current_user)):
    """
    获取用户列表
    :return: 用户列表
    """
    if not current_user['is_admin']:
        return ResponseUtil.error(msg="无权限", code=status.HTTP_403_FORBIDDEN)
    users = await UserService.get_users()
    return ResponseUtil.success(data=users, msg="获取用户列表成功")


@user_router.post("", response_model=BaseResponse, summary="创建或修改用户")
async def create_user(user_info: UserCreateOrUpdate, current_user=Depends(get_current_user)):
    """
    创建或修改用户信息
    - **user_info**: 用户信息
    - **return**: 创建成功
    """
    if not current_user:
        return ResponseUtil.error(msg="请登录", code=status.HTTP_403_FORBIDDEN)
    username = await UserService.create_user(user_info)
    return ResponseUtil.success(data=username, msg="成功")


@user_router.delete("/{user_id}", response_model=BaseResponse, summary="删除用户")
async def delete_user(user_id: str, current_user=Depends(get_current_user)):
    """
    删除用户
    :param user_id: 用户id
    :return: 删除成功
    """
    if not current_user['is_admin']:
        return ResponseUtil.error(msg="无权限", code=status.HTTP_403_FORBIDDEN)
    username = await UserService.delete_user(user_id)
    return ResponseUtil.success(data=username, msg="删除用户成功")


@user_router.patch("/{user_id}", response_model=BaseResponse, summary="修改用户状态")
async def update_user(user_id: str, current_user=Depends(get_current_user)):
    """
    修改用户状态，启用或者禁用
    :param user_id: 用户id
    :return: 更新成功
    """
    if not current_user['is_admin']:
        return ResponseUtil.error(msg="无权限", code=status.HTTP_403_FORBIDDEN)
    username = await UserService.change_user(user_id)
    return ResponseUtil.success(data=username, msg="更新用户状态成功")

@user_router.get("/userroles", response_model=BaseResponse, summary="获取用户角色")
async def list_user_roles(current_user=Depends(get_current_user)):
    """
    获取当前的用户角色
    """
    if not current_user['is_admin']:
        return ResponseUtil.error(msg="无权限", code=status.HTTP_403_FORBIDDEN)
    user_roles = await RoleService.get_user_role()
    return ResponseUtil.success(user_roles)

@user_router.post("/userroles", response_model=BaseResponse, summary="创建用户角色")
async def create_user_role(user_role_info: UserRoleCreateOrUpdate, current_user=Depends(get_current_user)):
    """
    创建或修改用户角色，，如果存在ID则修改，如果不存在ID则创建
    """
    if not current_user['is_admin']:
        return ResponseUtil.error(msg="无权限", code=status.HTTP_403_FORBIDDEN)
    user_role_name = await RoleService.create_user_role(user_role_info)
    return ResponseUtil.success(msg=f"创建用户{user_role_name}成功")