from typing import Any, Dict, List
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import K8sClientWrapper
from app.utils.logger import logger


class ServiceService:
    @staticmethod
    async def list_services(namespace: str = None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取网络列表"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            if namespace:
                service_list = v1.list_namespaced_service(namespace)
                logger.info(f"获取{namespace}下的service成功")
            else:
                service_list = v1.list_service_for_all_namespaces()
                logger.info("获取service成功")
            return [
                {
                    "name": svc.metadata.name,
                    "namespace": svc.metadata.namespace,
                    "type": svc.spec.type,
                    "cluster_ip": svc.spec.cluster_ip,
                    "external_name": svc.spec.external_name,
                    "ports": [f"{p.port}:{p.node_port}/{p.protocol}" for p in svc.spec.ports],
                    "selector": svc.spec.selector,
                    "creation_time": svc.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                } for svc in service_list.items
            ]
        except ApiException as e:
            logger.error(f"获取网络列表失败：{e}")
            raise

    @staticmethod
    async def get_service(namespace: str, service_name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """获取指定网络详情"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            service = v1.read_namespaced_service(service_name, namespace)
            logger.info(f"获取{namespace}/{service_name}下的service成功")
            return {
                "name": service.metadata.name,
                "namespace": service.metadata.namespace,
                "type": service.spec.type,
                "cluster_ip": service.spec.cluster_ip,
                "external_name": service.spec.external_name,
                "ports": [f"{p.port}:{p.node_port}/{p.protocol}" for p in service.spec.ports],
                "selector": service.spec.selector,
                "creation_time": service.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
        except ApiException as e:
            logger.error(f"获取{namespace}/{service_name}下的service失败：{e}")
            raise

    @staticmethod
    async def delete_service(namespace: str, service_name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """删除指定网络"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            v1.delete_namespaced_service(service_name, namespace)
            logger.info(f"删除{namespace}/{service_name}下的service成功")
            return {
                "message": f"{namespace}/{service_name}下的service删除成功"
            }
        except ApiException as e:
            logger.error(f"删除{namespace}/{service_name}下的service失败：{e}")
            raise
