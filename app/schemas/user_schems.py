from pydantic import BaseModel
from typing import Optional


# 登录请求体
class LoginRequest(BaseModel):
    username: str
    password: str


# 创建用户校验
class UserCreate(BaseModel):
    username: str
    password: str
    email: str


# 用户更新校验
class UserUpdate(BaseModel):
    username: str
    password: str




