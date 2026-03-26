# 用户service层
import logging

from fastapi import HTTPException
from app.models.user import User
from app.core.security import get_password_hash, verify_password


class UserService:
    # 创建用户，成功则返回用户数据
    @staticmethod
    async def create_user(user):
        logging.info(f"创建用户信息为{user.password}")
        logging.info(f"密码字节长度: {len(user.password.encode('utf-8'))}")
        hash_pwd = get_password_hash(user.password)
        user = await User.create(username=user.username, password=hash_pwd,
                                 email=user.email, department=user.department)
        return user

    # 更新用户信息
    @staticmethod
    async def update_user(user_id, user):
        user = await User.filter(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

    # 删除用户,成功则返回更改行数
    @staticmethod
    async def delete_user(user_id):
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        number = await user.delete()
        return number
