from typing import Any, Dict, List
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import K8sClientWrapper
from app.utils.logger import logger


class PersistentVolumeService:
    @staticmethod
    async def list_persistent_volumes(k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取持久卷列表"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            pv_list = v1.list_persistent_volume()
            pvs = []
            for pv in pv_list.items:
                pvs.append({
                    "name": pv.metadata.name,
                    "status": pv.status.phase,
                    "capacity": pv.spec.capacity,
                    "access_modes": pv.spec.access_modes,
                    "reclaim_policy": pv.spec.persistent_volume_reclaim_policy,
                    "storage_class": pv.spec.storage_class_name,
                    "creation_time": pv.metadata.creation_timestamp
                })
            logger.info(f"获取持久卷列表成功")
            return pvs
        except ApiException as e:
            logger.error(f"获取持久卷列表失败：{e}")
            raise

    @staticmethod
    async def get_persistent_volume(pv_name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """获取指定持久卷"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            pv = v1.read_persistent_volume(name=pv_name)
            logger.info(f"获取持久卷{pv_name}成功")
            return {
                "name": pv.metadata.name,
                "status": pv.status.phase,
                "capacity": pv.spec.capacity,
                "access_modes": pv.spec.access_modes,
                "reclaim_policy": pv.spec.persistent_volume_reclaim_policy,
                "storage_class": pv.spec.storage_class_name,
                "creation_time": pv.metadata.creation_timestamp
            }
        except ApiException as e:
            logger.error(f"获取持久卷{pv_name}失败：{e}")
            raise

    @staticmethod
    async def delete_persistent_volume(pv_name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """删除指定持久卷"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            v1.delete_persistent_volume(name=pv_name)
            logger.info(f"删除持久卷{pv_name}成功")
            return pv_name
        except ApiException as e:
            logger.error(f"删除持久卷{pv_name}失败：{e}")
