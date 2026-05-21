from app.core.k8s_client import K8sClientWrapper
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import Dict, Any, List


class ClusterRoleService:
    @staticmethod
    async def list_cluster_roles(k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取所有集群角色"""
        try:
            rbac_v1 = await k8s_wrapper.get_rbac_v1_api()
            cluster_role_list = rbac_v1.list_cluster_role().items
            return [
                {
                    "name": cr.metadata.name,
                    "labels": cr.metadata.labels,
                    "annotations": cr.metadata.annotations,
                    "creation_time": cr.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                } for cr in cluster_role_list
            ]
        except ApiException as e:
            logger.error(f"获取集群角色列表失败：{e}")
            raise

    @staticmethod
    async def get_cluster_role(name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """获取指定的集群角色"""
        try:
            rbac_v1 = await k8s_wrapper.get_rbac_v1_api()
            cluster_role = rbac_v1.read_cluster_role(name=name)
            return {
                "name": cluster_role.metadata.name,
                "labels": cluster_role.metadata.labels,
                "annotations": cluster_role.metadata.annotations,
                "creation_time": cluster_role.metadata.creation_timestamp.strftime
            }
        except ApiException as e:
            logger.error(f"获取集群角色失败：{e}")
            raise

    @staticmethod
    async def delete_cluster_role(name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """删除指定集群角色"""
        try:
            rbac_v1 = await k8s_wrapper.get_rbac_v1_api()
            status = rbac_v1.delete_cluster_role(name=name)
            logger.info(f"删除集群角色 {name} 成功")
            return {"message": f"集群角色 {name} 已删除", "status": status.status}
        except ApiException as e:
            logger.error(f"删除集群角色失败：{e}")
            raise
