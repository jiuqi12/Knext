from app.core.k8s_client import K8sClientWrapper
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import List, Dict, Any


class SecretService:
    @staticmethod
    async def list_secrets(namespace: str = None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取 secrets 列表"""
        v1 = await k8s_wrapper.get_core_v1_api()
        try:
            if namespace:
                secret_list = v1.list_namespaced_secret(namespace).items
            else:
                secret_list = v1.list_secret_for_all_namespaces().items
            logger.info(f"获取命名空间 {namespace} 下的 secrets")
            return [
                {
                    "name": secret.metadata.name,
                    "namespace": secret.metadata.namespace,
                    "type": secret.type,
                    "labels": secret.metadata.labels,
                    "creation_time": secret.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for secret in secret_list
            ]
        except ApiException as e:
            logger.error(f"获取 secrets 列表失败：{e}")
            raise

    @staticmethod
    async def get_secret(namespace: str, secret_name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """获取指定Secret的详细信息"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            secret = v1.read_namespaced_secret(secret_name, namespace)
            return {
                "name": secret.metadata.name,
                "namespace": secret.metadata.namespace,
                "labels": secret.metadata.labels,
                "creation_time": secret.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
        except ApiException as e:
            logger.info(f"获取Secret失败：{e}")
            raise

    @staticmethod
    async def delete_secret(secret_name: str, namespace: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """删除指定Secret"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            v1.delete_namespaced_secret(secret_name, namespace)
            return {
                "message": f"Secret {secret_name} 删除成功"
            }
        except ApiException as e:
            logger.info(f"删除Secret失败：{e}")
            raise
