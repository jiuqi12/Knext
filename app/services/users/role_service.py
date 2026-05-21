from typing import Dict, Any, List
from app.utils.logger import logger
from app.models.user_role import UserRoles


class RoleService:
    @staticmethod
    async def get_user_role() -> List[Dict[str, Any]]:
        """
        获取当前全部的用户角色
        """
        user_role_list = []
        user_roles = await UserRoles.all()
        print(user_roles)
        for user_role in user_roles:
            user_role_list.append({
                "user_role_id": user_role.id,
                "user_role_name": user_role.name,
                "user_role_sa": user_role.service_accounts,
                "user_role_namespace": user_role.namespace
            })
        logger.info("获取用户角色成功")
        return user_role_list
    
    @staticmethod
    async def create_user_role(user_role_info) -> str:
        """
        创建或修改用户角色，如果存在ID则修改，如果不存在ID则创建
        """
        if not user_role_info.id:
            await UserRoles.create(name=user_role_info.name,
                                                service_accounts=user_role_info.service_accounts,
                                                namespace=user_role_info.namespace)
            logger.info(f"创建用户角色{user_role_info.name}成功")
            return user_role_info.name
        else:
            user_role = await UserRoles.get_or_none(id = user_role_info.id)
            user_role.username = user_role_info.username
            user_role.is_admin = user_role_info.is_admin
            user_role.email = user_role_info.email
            await user_role.save()
            logger.info(f"修改用户角色{user_role_info.name}成功")
            return user_role_info.name
