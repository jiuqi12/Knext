import logging
from typing import Dict, Any
from fastapi import HTTPException
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.utils.logger import logger
from datetime import datetime


# 定义常量
MAX_LOGIN_ATTEMPTS = 5

class UserService:
    @staticmethod
    async def user_login(username: str, password: str) -> Dict[str, Any]:
        """
        登录流程：
        1、校验参数 2、查询用户 3、检验状态 4、校验密码 5、生成token 6、返回结果
        """
        # 校验参数
        if not username or not password:
            logger.error("用户名或密码不能为空")
            raise HTTPException(status_code=400, detail="用户名或密码不能为空")
        # 查找用户
        user = await User.get_or_none(username=username)
        if not user:
            logger.error("用户不存在，请检查输入内容")
            raise HTTPException(status_code=404, detail="用户不存在，请检查输入内容")
        # 检查用户状态
        if user.login_attempts >= MAX_LOGIN_ATTEMPTS:
            logger.error("账户已经被锁定，请联系管理员解锁")
            raise HTTPException(status_code=401, detail="失败次数已达上限，请联系管理员解锁")
        # 校验密码
        if not verify_password(password, user.hash_password):
            await User.filter(username=username).update(login_attempts = user.login_attempts + 1)
            await User.filter(username=username).update(last_login_attempt = datetime.now())
            logger.error("用户或密码错误")
            raise HTTPException(status_code=401, detail="用户名或密码错误")
        # 登录成功，生成token（包含用户信息）
        token_data = {"username": username}
        logger.info("用户登录成功")
        return {
            "access_token": create_access_token(data=token_data),
            "user": username
        }

    # 创建用户，成功则返回用户数据
    @staticmethod
    async def create_user(user):
        logging.info(f"创建用户信息为{user.password}")
        logging.info(f"密码字节长度: {len(user.password.encode('utf-8'))}")
        hash_pwd = get_password_hash(user.password)
        user = await User.create(username=user.username, password=hash_pwd, email=user.email, department=user.department)
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
