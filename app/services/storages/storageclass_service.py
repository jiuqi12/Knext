from typing import Any, Dict, List
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import get_storage_v1_api
from app.utils.logger import logger


class StorageClassService:
    @staticmethod
    def list_storages() -> List[Dict[str, Any]]:
        """获取存储列表"""
        try:
            storage_v1 = get_storage_v1_api()
            storages_list = storage_v1.list_storage_class()
            return [
                {
                    "name": storage.metadata.name,
                    "provisioner": storage.provisioner,
                    "reclaim_policy": storage.reclaim_policy,
                    "volume_binding_mode": storage.volume_binding_mode,
                    "allow_volume_expansion": storage.allow_volume_expansion,
                    "parameters": storage.parameters,
                    "creation_time": storage.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                } for storage in storages_list.items
            ]
        except ApiException as e:
            logger.error(f"获取存储列表失败：{e}")
            raise
        except Exception as e:
            logger.error(f"获取存储列表异常：{e}")
            raise
