from app.core.k8s_client import K8sClientWrapper
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import Dict, Any, List


class ClusterRoleBindingService:
    @staticmethod
    async def list_cluster_role_bindings(k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取所有集群角色绑定"""
        try:
            rbac_v1 = await k8s_wrapper.get_rbac_v1_api()
            cluster_role_binding_list = rbac_v1.list_cluster_role_binding().items
            return [
                {
                    "name": crb.metadata.name,
                    "labels": crb.metadata.labels,
                    "annotations": crb.metadata.annotations,
                    "creation_time": crb.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                } for crb in cluster_role_binding_list
            ]
        except ApiException as e:
            logger.error(f"获取集群角色绑定列表失败：{e}")
            raise

    @staticmethod
    async def get_cluster_role_binding(name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """获取指定集群角色绑定详情"""
        try:
            rbac_v1 = await k8s_wrapper.get_rbac_v1_api()
            cluster_role_binding = rbac_v1.read_cluster_role_binding(name=name)
            return {
                "name": cluster_role_binding.metadata.name,
                "labels": cluster_role_binding.metadata.labels,
                "annotations": cluster_role_binding.metadata.annotations,
            }
        except ApiException as e:
            logger.error(f"获取集群角色绑定详情失败：{e}")
            raise

    @staticmethod
    async def delete_cluster_role_binding(name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """删除指定集群角色绑定"""
        try:
            rbac_v1 = await k8s_wrapper.get_rbac_v1_api()
            status = rbac_v1.delete_cluster_role_binding(name=name)
            logger.info(f"删除集群角色绑定 {name} 成功")
            return {"message": f"集群角色绑定 {name} 已删除", "status": status.status}
        except ApiException as e:
            logger.error(f"删除集群角色绑定失败：{e}")
            raise
