from app.models.user import User
from typing import Dict
from fastapi import HTTPException

# 定义常量
MAX_LOGIN_ATTEMPTS = 5


async def login(username: str, password: str) -> Dict:
    # 查找用户
    user = await User.get(username=username)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 检查用户状态
    if user.is_active:
        raise HTTPException(status_code=403, detail="账户已经被锁定，请联系管理员解锁")

    # 校验密码