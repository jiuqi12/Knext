from typing import Dict, Any, List
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.utils.logger import logger
from app.utils.exceptions import ValidationException, NotFoundException, AuthException
from datetime import datetime

# 定义常量
MAX_LOGIN_ATTEMPTS = 3


class UserService:
    @staticmethod
    async def user_login(request) -> Dict[str, Any]:
        """
        登录流程：
        1、校验参数 2、查询用户 3、检验状态 4、校验密码 5、生成token 6、返回结果
        """
        # 校验参数
        if not request.username or not request.password:
            logger.error("用户名或密码不能为空")
            raise ValidationException("用户名或密码不能为空")
        # 查找用户
        user = await User.get_or_none(username=request.username)
        if not user:
            logger.error("用户不存在，请检查输入内容")
            raise NotFoundException("用户不存在，请检查输入内容")
        # 检查用户状态
        if user.login_attempts > MAX_LOGIN_ATTEMPTS or user.is_active is False:
            logger.error("账号已被禁用，请联系管理员解锁")
            raise AuthException("账号已被禁用，请联系管理员解锁")
        # 校验密码
        if not verify_password(request.password, user.hash_password):
            await User.filter(username=request.username).update(login_attempts=user.login_attempts + 1)
            await User.filter(username=request.username).update(last_login_attempt=datetime.now())
            logger.error("用户或密码错误")
            raise AuthException("用户名或密码错误")
        # 登录成功，刷新登录时间，生成token（包含用户信息）
        await User.filter(username=request.username)\
            .update(last_login_attempt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), login_attempts=0)
        token_data = {"username": request.username}
        logger.info("用户登录成功")
        return {
            "access_token": create_access_token(data=token_data),
            "token_type": "bearer",
            "user": {
                "uuid": user.id,
                "username": user.username,
                "role_id": user.role_id,
                "is_admin": user.is_admin,
                "last_login_time": user.last_login_attempt,
            }
        }

    @staticmethod
    async def get_users() -> List[Dict[str, Any]]:
        """
        获取全部用户信息
        """
        users = await User.all()
        user_list = []
        for user in users:
            user_list.append({
                "username": user.username,
                "user_id": user.id,
                "email": user.email,
                "is_active": user.is_active,
                "is_admin": user.is_admin,
                "created_at": user.created_at,
                "last_login_time": user.last_login_attempt,
            })
        logger.info("获取用户列表成功")
        return user_list

    @staticmethod
    async def get_user(user_id):
        """
        获取单个用户信息
        """
        user = await User.get_or_none(user_id=user_id)
        if not user:
            raise NotFoundException("用户不存在")
        return {
            "username": user.username,
            "user_id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "last_login_time": user.last_login_attempt,
            "created_at": user.created_at,
        }

    @staticmethod
    async def create_user(user_info):
        """
        创建或更新用户，如果携带id，则是修改用户数据，如果没有id，则是修改用户数据
        """
        if not user_info.id:
            # id不存在，创建用户
            hash_pwd = get_password_hash(user_info.password)
            print(user_info.model_dump())
            user = await User.create(username=user_info.username, hash_password=hash_pwd,
                                     is_admin=user_info.is_admin, email=user_info.email,
                                     role_id=user_info.user_role_id)
            logger.info(f"创建用户{user.username}成功")
            return user.username
        else:
            # id存在，修改用户
            user = await User.get_or_none(id=user_info.id)
            if user_info.password:
                hash_pwd = get_password_hash(user_info.password)
                user.hash_password = hash_pwd
            user.username = user_info.username
            user.is_admin = user_info.is_admin
            user.email = user_info.email
            await user.save()
            logger.info(f"修改用户{user.username}成功")
            return user.username

    @staticmethod
    async def delete_user(user_id):
        """
        删除用户
        """
        user = await User.filter(id=user_id)
        if not user:
            raise NotFoundException("用户不存在")
        await User.filter(id=user_id).delete()
        logger.info(f"删除用户{user[0].username}成功")
        return user[0].username

    @staticmethod
    async def change_user(user_id):
        """
        修改用户状态
        """
        user = await User.get_or_none(id=user_id)
        if not user:
            raise NotFoundException("用户不存在")
        new_status = not user.is_active
        await User.filter(id=user_id).update(is_active=new_status, login_attempts=0)
        logger.info(f"修改用户{user.username}状态成功,状态为{user.is_active}")
        return user.username
