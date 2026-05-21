from app.core.k8s_client import K8sClientWrapper
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import Dict, Any, List


class RoleService:
    @staticmethod
    async def list_roles(namespace: str =  None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取命名空间下的所有角色"""
        try:
            rbac_v1 = await k8s_wrapper.get_rbac_v1_api()
            if namespace:
                role_list = rbac_v1.list_namespaced_role(namespace=namespace).items
            else:
                role_list = rbac_v1.list_role_for_all_namespaces().items
            return [
                {
                    "name": role.metadata.name,
                    "namespace": role.metadata.namespace,
                    "labels": role.metadata.labels,
                    "annotations": role.metadata.annotations,
                    "creation_time": role.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                } for role in role_list
            ]
        except ApiException as e:
            logger.error(f"获取角色列表失败：{e}")
            raise

    @staticmethod
    async def get_role(name: str, namespace: str, k8s_wrapper: K8sClientWrapper = None):
        """获取指定的角色"""
        try:
            rbac_v1 = await k8s_wrapper.get_rbac_v1_api()
            role = rbac_v1.read_namespaced_role(name=name, namespace=namespace)
            return {
                "name": role.metadata.name,
                "namespace": role.metadata.namespace,
                "labels": role.metadata.labels,
                "annotations": role.metadata.annotations,
                "creation_time": role.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
        except ApiException as e:
            logger.error(f"获取角色失败：{e}")
            raise

    @staticmethod
    async def delete_role(name: str, namespace: str = "default", k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """删除指定角色"""
        try:
            rbac_v1 = await k8s_wrapper.get_rbac_v1_api()
            status = rbac_v1.delete_namespaced_role(name=name, namespace=namespace)
            logger.info(f"删除角色 {name} 成功")
            return {"message": f"角色 {name} 已删除", "status": status.status}
        except ApiException as e:
            logger.error(f"删除角色失败：{e}")
            raise
