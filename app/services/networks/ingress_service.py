from typing import Any, Dict, List
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import K8sClientWrapper
from app.utils.logger import logger


class IngressService:
    @staticmethod
    async def list_ingresses(namespace: str = None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取所有ingress列表"""
        try:
            ingres_v1 = await k8s_wrapper.get_networking_v1_api()
            ingress_list = ingres_v1.list_ingress_for_all_namespaces().items
            return [
                {
                    "name": ingress.metadata.name,
                    "namespace": ingress.metadata.namespace,
                    "class": ingress.spec.ingress_class_name,
                    "hosts": [host.hostname for host in ingress.spec.rules],
                    "rules": [
                        {
                            "host": rule.host.hostname,
                            "paths": [path.path for path in rule.http.paths],
                        }for rule in ingress.spec.rules
                    ],
                    "labels": ingress.metadata.labels,
                    "annotations": ingress.metadata.annotations,
                    "create_time": ingress.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }for ingress in ingress_list
            ]
        except ApiException as e:
            logger.error(f"获取ingress列表失败：{e}")
            raise

    @staticmethod
    async def get_ingress(namespace: str, ingress_name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """获取指定ingress"""
        try:
            ingres_v1 = await k8s_wrapper.get_networking_v1_api()
            ingress = ingres_v1.read_namespaced_ingress(ingress_name, namespace)
            return {
                "name": ingress.metadata.name,
                "namespace": ingress.metadata.namespace,
                "labels": ingress.metadata.labels,
            }
        except ApiException as e:
            logger.error(f"获取ingress失败：{e}")
            raise

    @staticmethod
    async def delete_ingress(namespace: str, ingress_name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """删除指定ingress"""
        try:
            ingres_v1 = await k8s_wrapper.get_networking_v1_api()
            ingress = ingres_v1.delete_namespaced_ingress(ingress_name, namespace)
            return {
                "message": f"{namespace}/{ingress_name}下的ingress删除成功"
            }
        except ApiException as e:
            logger.error(f"删除ingress失败：{e}")