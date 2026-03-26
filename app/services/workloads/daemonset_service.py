from app.core.k8s_client import get_apps_v1_api
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import List, Dict, Any


class DaemonSetsService:
    @staticmethod
    def list_daemonsets(namespace: str = None) -> List[Dict[str, Any]]:
        try:
            apps_v1 = get_apps_v1_api()
            if namespace:
                ds_list = apps_v1.list_namespaced_daemon_set(namespace)
            else:
                ds_list = apps_v1.list_daemon_set_for_all_namespaces()

            return [{
                "name": ds.metadata.name,
                "namespace": ds.metadata.namespace,
                "desired_number_scheduled": ds.status.desired_number_scheduled or 0,
                "current_number_scheduled": ds.status.current_number_scheduled or 0,
                "created_at": ds.metadata.creation_timestamp
            } for ds in ds_list.items]
        except ApiException as e:
            logger.error(f"获取 deployments 列表失败：{e}")
            raise
        except Exception as e:
            logger.error(f"获取 deployments 列表失败：{e}")
            raise
