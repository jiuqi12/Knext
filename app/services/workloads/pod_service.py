from time import sleep
from fastapi import Query
from app.core.k8s_client import K8sClientWrapper
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import List, Dict, Any


class PodService:
    @staticmethod
    async def list_pods(namespace: Query = None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取 pods 列表"""
        v1 = await k8s_wrapper.get_core_v1_api()
        try:
            if namespace:
                pod_list = v1.list_namespaced_pod(namespace).items
            else:
                pod_list = v1.list_pod_for_all_namespaces().items
            sleep(1)
            logger.info(f"获取pod列表成功共：{len(pod_list)}")
            return [
                {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "restart_count": pod.status.container_statuses[0].restart_count if pod.status.container_statuses else 0,
                    "labels": pod.metadata.labels,
                    "pod_ip": pod.status.pod_ip,
                    "node_name": pod.spec.node_name,
                    "images": [container.image for container in pod.spec.containers],
                    "creation_time": pod.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                } for pod in pod_list
            ]
        except ApiException as e:
            logger.error(f"获取 pods 失败：{e}")
            raise e

    @staticmethod
    async def delete_pod(pod_name: str, namespace: str, k8s_wrapper: K8sClientWrapper = None) -> str:
        """删除 pods"""
        v1 = await k8s_wrapper.get_core_v1_api()
        try:
            v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
            logger.info(f"删除 pods {pod_name} 成功")
            return f"删除Pod{pod_name}成功"
        except ApiException as e:
            logger.error(f"删除 pods {pod_name} 失败：{e}")
            raise
