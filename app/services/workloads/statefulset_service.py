from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import get_apps_v1_api
from typing import Dict, Any, List
from app.utils.logger import logger


class StatefulSetService:
    @staticmethod
    def list_statefulsets(namespace: str = None) -> List[Dict[str, Any]]:
        try:
            apps_v1 = get_apps_v1_api()
            if namespace:
                sts_list = apps_v1.list_namespaced_stateful_set(namespace)
            else:
                sts_list = apps_v1.list_stateful_set_for_all_namespaces()

            return [{
                "name": sts.metadata.name,
                "namespace": sts.metadata.namespace,
                "replicas": sts.spec.replicas,
                "ready_replicas": sts.status.ready_replicas or 0,
                "created_at": sts.metadata.creation_timestamp
            } for sts in sts_list.items]
        except ApiException as e:
            logger.error(f"列出工作负载失败：{e}")
            raise
        except Exception as e:
            logger.error(f"列出工作负载失败：{e}")
            raise
