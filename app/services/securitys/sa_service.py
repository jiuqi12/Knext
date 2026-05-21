from app.core.k8s_client import K8sClientWrapper
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import Dict, Any, List


class SaService:
    @staticmethod
    async def list_service_accounts(k8s_wrapper: K8sClientWrapper = None, namespace: str = None) -> List[Dict[str, Any]]:
        """获取服务账户列表"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            if namespace:
                sa_list = v1.list_namespaced_service_account(namespace)
                logger.info(f"获取{namespace}下的服务账户成功")
            else:
                sa_list = v1.list_service_account_for_all_namespaces()
                logger.info("获取服务账户成功")
            return [
                {
                    "name": sa.metadata.name,
                    "namespace": sa.metadata.namespace,
                    "labels": sa.metadata.labels,
                    "annotations": sa.metadata.annotations,
                    "creation_time": sa.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                } for sa in sa_list.items
            ]
        except ApiException as e:
            logger.error(f"获取服务账户列表失败：{e}")
            raise

    @staticmethod
    async def get_service_account(namespace: str, name: str, k8s_wrapper: K8sClientWrapper = None):
        """获取指定服务账户的详细信息"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            sa = v1.read_namespaced_service_account(name, namespace)
            return {
                "name": sa.metadata.name,
                "namespace": sa.metadata.namespace,
                "labels": sa.metadata.labels,
                "annotations": sa.metadata.annotations,
                "creation_time": sa.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
        except ApiException as e:
            logger.error(f"获取服务账户 {name} 详情失败：{e}")
            raise


    @staticmethod
    async def delete_service_account(namespace: str, name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """删除指定服务账户"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            status = v1.delete_namespaced_service_account(name=name, namespace=namespace)
            logger.info(f"删除服务账户 {name} 成功")
            return {"message": f"服务账户 {name} 已删除", "status": status.status}
        except ApiException as e:
            logger.error(f"删除服务账户失败：{e}")
            raise
