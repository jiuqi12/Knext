from fastapi import APIRouter, Depends, HTTPException
from app.services.users.users_service import UserService
from app.schemas.user_schems import LoginRequest
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil

user_router = APIRouter()


# 登录
@user_router.post("/login", response_model=BaseResponse)
async def user_login(request: LoginRequest):
    """
    用户登录请求
    :param request: 用户名和密码
    :return: 登录token
    """
    # try:
    #     result = await UserService.user_login(request.username, request.password)
    #     return ResponseUtil.success(data=result, msg="登录成功")
    # except HTTPException as e:
    #     raise HTTPException(status_code=e.status_code, detail=e.detail)
    return ResponseUtil.success(data=None, msg="登录成功")


# 退出登录
@user_router.post("/logout", response_model=BaseResponse)
async def user_logout():
    """
    用户退出登录
    :return: 退出登录成功
    """
    return ResponseUtil.success(data=None, msg="退出登录成功")
