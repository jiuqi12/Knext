from app.core.k8s_client import get_core_v1_api
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import List, Dict, Any


class SecretService:
    @staticmethod
    def list_secrets(namespace: str = None) -> List[Dict[str, Any]]:
        """
        获取 secrets 列表
        :param namespace: 命名空间，可选
        :return: secrets 列表
        """
        v1 = get_core_v1_api()
        secret_list = []
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
        except Exception as e:
            logger.error(f"获取 secrets 列表异常：{e}")
            raise