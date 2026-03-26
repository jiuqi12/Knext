from typing import Any, Dict, List
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import get_core_v1_api
from app.utils.logger import logger


class PersistentVolumeService:
    @staticmethod
    def list_persistent_volumes() -> List[Dict[str, Any]]:
        """获取持久卷列表"""
        try:
            v1 = get_core_v1_api()
            pvs = []
            pv_list = v1.list_persistent_volume()
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
        except Exception as e:
            logger.error(f"获取持久卷列表失败：{e}")
            raise
