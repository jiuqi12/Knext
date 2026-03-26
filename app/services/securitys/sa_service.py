from app.core.k8s_client import get_core_v1_api
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import Dict, Any, List


class SaService:
    @staticmethod
    def get_service_accounts(namespace: str = "default") -> List[Dict[str, Any]]:
        """获取指定命名空间下的所有服务账户"""
        try:
            v1 = get_core_v1_api()
            sa_list = v1.list_namespaced_service_account(namespace=namespace).items
            return [
                {
                    "name": sa.metadata.name,
                    "namespace": sa.metadata.namespace,
                    "labels": sa.metadata.labels,
                    "annotations": sa.metadata.annotations,
                    "creation_time": sa.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                } for sa in sa_list
            ]
        except ApiException as e:
            logger.error(f"获取服务账户列表失败：{e}")
            raise
        except Exception as e:
            logger.error(f"获取服务账户列表失败：{e}")
            raise

    @staticmethod
    def delete_service_account(name: str, namespace: str = "default") -> Dict[str, Any]:
        """删除指定服务账户"""
        try:
            v1 = get_core_v1_api()
            status = v1.delete_namespaced_service_account(name=name, namespace=namespace)
            logger.info(f"删除服务账户 {name} 成功")
            return {"message": f"服务账户 {name} 已删除", "status": status.status}
        except ApiException as e:
            logger.error(f"删除服务账户失败：{e}")
            raise
        except Exception as e:
            logger.error(f"删除服务账户失败：{e}")
            raise