from app.core.k8s_client import K8sClientWrapper
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import List, Dict, Any
from fastapi import Query


class DaemonSetsService:
    @staticmethod
    async def list_daemonsets(namespace: Query = None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        try:
            apps_v1 = await k8s_wrapper.get_apps_v1_api()
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

    @staticmethod
    async def delete_daemonset(ds_name: str, namespace: str, k8s_wrapper: K8sClientWrapper = None):
        try:
            apps_v1 = await k8s_wrapper.get_apps_v1_api()
            apps_v1.delete_namespaced_daemon_set(ds_name, namespace)
            logger.info(f"删除 DaemonSet {ds_name} 成功")
            return ds_name
        except ApiException as e:
            logger.error(f"删除 DaemonSet 失败：{e}")
            raise
