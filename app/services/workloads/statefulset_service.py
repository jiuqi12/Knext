from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import K8sClientWrapper
from typing import Dict, Any, List
from app.utils.logger import logger
from fastapi import Query


class StatefulSetService:
    @staticmethod
    async def list_statefulsets(namespace: Query = None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        try:
            apps_v1 = await k8s_wrapper.get_apps_v1_api()
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

    @staticmethod
    async def delete_statefulset(sts_name: str, namespace: str, k8s_wrapper: K8sClientWrapper = None):
        try:
            apps_v1 = await k8s_wrapper.get_apps_v1_api()
            apps_v1.delete_namespaced_stateful_set(sts_name, namespace)
            logger.info(f"删除 StatefulSet {sts_name} 成功")
            return sts_name
        except ApiException as e:
            logger.error(f"删除 StatefulSet 失败：{e}")
            raise
