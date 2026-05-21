from app.core.k8s_client import K8sClientWrapper
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import Dict, Any, List


class RoleBindingService:
    @staticmethod
    async def list_role_bindings(namespace: str = None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取命名空间下的所有角色绑定"""
        try:
            rbac_v1 = await k8s_wrapper.get_rbac_v1_api()
            if namespace:
                role_binding_list = rbac_v1.list_namespaced_role_binding(namespace=namespace).items
                logger.info(f"获取命名空间 {namespace} 下的角色绑定列表")
            else:
                logger.info("获取所有命名空间下的角色绑定列表")
                role_binding_list = rbac_v1.list_role_binding_for_all_namespaces().items
            return [
                {
                    "name": rb.metadata.name,
                    "namespace": rb.metadata.namespace,
                    "labels": rb.metadata.labels,
                    "annotations": rb.metadata.annotations,
                    "creation_time": rb.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                } for rb in role_binding_list
            ]
        except ApiException as e:
            logger.error(f"获取角色绑定列表失败：{e}")
            raise

    @staticmethod
    async def get_role_binding(name: str, namespace: str, k8s_wrapper: K8sClientWrapper = None):
        """获取指定的角色绑定"""
        try:
            rbac_v1 = await k8s_wrapper.get_rbac_v1_api()
            role_binding = rbac_v1.read_namespaced_role_binding(name=name, namespace=namespace)
            return {
                "name": role_binding.metadata.name,
                "namespace": role_binding.metadata.namespace,
                "labels": role_binding.metadata.labels,
                "annotations": role_binding.metadata.annotations,
            }
        except ApiException as e:
            logger.error(f"获取角色绑定失败：{e}")
            raise

    @staticmethod
    async def delete_role_binding(name: str, namespace: str = "default", k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """删除指定角色绑定"""
        try:
            rbac_v1 = await k8s_wrapper.get_rbac_v1_api()
            status = rbac_v1.delete_namespaced_role_binding(name=name, namespace=namespace)
            logger.info(f"删除角色绑定 {name} 成功")
            return {"message": f"角色绑定 {name} 已删除", "status": status.status}
        except ApiException as e:
            logger.error(f"删除角色绑定失败：{e}")
            raise
