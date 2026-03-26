from typing import Any, Dict, List
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import get_core_v1_api
from app.utils.logger import logger


class ConfigMapService:
    @staticmethod
    def list_configmaps(namespace: str = None) -> List[Dict[str, Any]]:
        """获取ConfigMap列表"""
        try:
            v1 = get_core_v1_api()
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
        except Exception as e:
            logger.info(f"获取ConfigMap列表失败：{e}")
            raise
