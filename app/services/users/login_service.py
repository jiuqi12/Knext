# 登录逻辑

from app.models.user import User
from fastapi import HTTPException


async def login(username: str, password: str):
    # 查找用户
    user = await User.get(username=username)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 检查用户状态
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账户已经被锁定，请联系管理员解锁")

    # 校验密码
    if user and user.password == password:
        raise HTTPException(status_code=200, detail=f"登录成功，登录用户为{user.username}")
        User.is_active == 3
