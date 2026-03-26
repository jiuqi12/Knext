from typing import Any, Dict, List
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import get_core_v1_api
from app.utils.logger import logger


class ServiceService:
    @staticmethod
    def list_services(namespace: str = None) -> List[Dict[str, Any]]:
        """获取网络列表"""
        try:
            v1 = get_core_v1_api()
            services_list = []
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
                    "selector": svc.spec.selector
                } for svc in service_list.items
            ]
        except ApiException as e:
            logger.error(f"获取网络列表失败：{e}")
            raise
        except Exception as e:
            logger.error(f"获取网络列表失败：{e}")
            raise
