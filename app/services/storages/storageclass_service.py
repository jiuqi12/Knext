from typing import Any, Dict, List
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import K8sClientWrapper
from app.utils.logger import logger


class StorageClassService:
    @staticmethod
    async def list_storages(k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取存储类列表"""
        try:
            storage_v1 = await k8s_wrapper.get_storage_v1_api()
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

    @staticmethod
    async def get_storage(storage_name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """获取指定存储类"""
        try:
            storage_v1 = await k8s_wrapper.get_storage_v1_api()
            storage = storage_v1.read_storage_class(name=storage_name)
            return {
                "name": storage.metadata.name,
                "provisioner": storage.provisioner,
                "reclaim_policy": storage.reclaim_policy,
                "volume_binding_mode": storage.volume_binding_mode,
            }
        except ApiException as e:
            logger.error(f"获取存储{storage_name}失败：{e}")
            raise

    @staticmethod
    async def delete_storage(storage_name: str, k8s_wrapper: K8sClientWrapper = None) -> str:
        """删除指定存储类"""
        try:
            storage_v1 = await k8s_wrapper.get_storage_v1_api()
            storage_v1.delete_storage_class(name=storage_name)
            return f"删除{storage_name}存储类成功"
        except ApiException as e:
            logger.error(f"删除存储{storage_name}失败：{e}")
            raise
