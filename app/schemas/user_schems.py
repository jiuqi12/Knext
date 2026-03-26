# 登录请求验证

from pydantic import BaseModel
from typing import Optional


# 登录请求体
class LoginRequest(BaseModel):
    username: str
    password: str


# 登陆成功返回的信息
class LoginResponse(BaseModel):
    msg: str
    username: str

# 用户功能校验

from pydantic import BaseModel


# 创建用户校验
class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    department: str

    #
    # class Config:
    #     from_attributes = True


# 用户更新校验
class UserUpdate(BaseModel):
    userid: str
    username: str
    password: str


# 用户信息返回
class UserOut(BaseModel):
    id: int
    username: str
    is_active: int
    email: str
    department: str




