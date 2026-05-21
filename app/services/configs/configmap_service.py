from typing import Any, Dict, List
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import K8sClientWrapper
from app.utils.logger import logger


class ConfigMapService:
    @staticmethod
    async def list_configmaps(namespace: str = None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取ConfigMap列表"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            if namespace:
                configmap_list = v1.list_namespaced_config_map(namespace)
            else:
                configmap_list = v1.list_config_map_for_all_namespaces()
            return [
                {
                    "name": configmap.metadata.name,
                    "namespace": configmap.metadata.namespace,
                    "labels": configmap.metadata.labels,
                    "creation_time": configmap.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                } for configmap in configmap_list.items
            ]
        except ApiException as e:
            logger.info(f"获取ConfigMap列表失败：{e}")
            raise

    @staticmethod
    async def get_configmap(namespace: str, configmap_name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """获取指定ConfigMap的详细信息"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            configmap = v1.read_namespaced_config_map(configmap_name, namespace)
            return {
                "name": configmap.metadata.name,
                "namespace": configmap.metadata.namespace,
                "labels": configmap.metadata.labels,
                "creation_time": configmap.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "data": configmap.data
            }
        except ApiException as e:
            logger.info(f"获取ConfigMap失败：{e}")
            raise

    @staticmethod
    async def delete_configmap(namespace: str, configmap_name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """删除指定ConfigMap"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            v1.delete_namespaced_config_map(configmap_name, namespace)
            return {
                "message": f"ConfigMap {configmap_name} 删除成功"
            }
        except ApiException as e:
            logger.info(f"删除ConfigMap失败：{e}")
            raise
