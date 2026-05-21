from typing import List, Dict, Any
from app.core.k8s_client import K8sClientWrapper
from app.utils.logger import logger
from kubernetes.client.exceptions import ApiException


class NamespaceService:
    """命名空间服务类"""

    @staticmethod
    async def get_namespaces(k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取所有命名空间"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            namespace_list = v1.list_namespace()
            logger.info(f"获取所有命名空间成功")
            return [
                {
                    "name": ns.metadata.name,
                    "status": ns.status.phase,
                    "labels": ns.metadata.labels,
                    "creation_time": ns.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "annotations": ns.metadata.annotations,
                }for ns in namespace_list.items
            ]
        except ApiException as e:
            logger.error(f"获取所有命名空间失败：{e}")
            raise

    @staticmethod
    async def delete_namespace(namespace_name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """删除命名空间"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            v1.delete_namespace(name=namespace_name)
            logger.info(f"删除命名空间{namespace_name}")
            return namespace_name
        except ApiException as e:
            logger.error(f"删除命名空间失败：{e}")
            raise
