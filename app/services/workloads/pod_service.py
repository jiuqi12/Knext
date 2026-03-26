from time import sleep

from app.core.k8s_client import get_core_v1_api
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import List, Dict, Any


class PodService:
    @staticmethod
    def get_pods(namespace: str = None) -> List[Dict[str, Any]]:
        """
        获取 pods 列表
        :param namespace: 命名空间
        :return: pods 列表
        """
        v1 = get_core_v1_api()
        try:
            if namespace:
                pod_list = v1.list_namespaced_pod(namespace).items
            else:
                pod_list = v1.list_pod_for_all_namespaces().items
            logger.info("获取pods容器组成功")
            sleep(2)
            return [
                {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "restart_count": pod.status.container_statuses[0].restart_count,
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
        except Exception as e:
            logger.error(f"获取 pods 列表失败：{e}")
            raise
