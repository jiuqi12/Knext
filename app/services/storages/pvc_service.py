from typing import Any, Dict, List
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import get_core_v1_api
from app.utils.logger import logger


class PersistentVolumeClaimService:
    @staticmethod
    def list_persistent_volume_claims(namespace: str = None) -> List[Dict[str, Any]]:
        """获取持久卷声明列表"""
        try:
            v1 = get_core_v1_api()
            pvcs = []
            if namespace:
                pvc_list = v1.list_namespaced_persistent_volume_claim(namespace)
                for pvc in pvc_list.items:
                    pvcs.append({
                        "name": pvc.metadata.name,
                        "namespace": pvc.metadata.namespace,
                        "status": pvc.metadata.phase,
                        "volume": pvc.spec.volume_name,
                        "capacity": pvc.status.capacity,
                        "access_modes": pvc.spec.access_modes,
                        "storage_class": pvc.spec.storage_class_name,
                        "created_at": pvc.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    })
                logger.info(f"获取持久卷声明列表成功")
                return pvcs
            else:
                pvc_list = v1.list_persistent_volume_claim_for_all_namespaces()
                for pvc in pvc_list.items:
                    pvcs.append({
                        "name": pvc.metadata.name,
                        "namespace": pvc.metadata.namespace,
                        "status": pvc.metadata.phase,
                        "volume": pvc.spec.volume_name,
                        "capacity": pvc.status.capacity,
                        "access_modes": pvc.spec.access_modes,
                        "storage_class": pvc.spec.storage_class_name,
                        "created_at": pvc.metadata.creation_timestamp.strftime()
                    })
                logger.info(f"获取持久卷声明列表成功")
                return pvcs
        except ApiException as e:
            logger.error(f"获取持久卷声明失败{e}")
            raise
        except Exception as e:
            logger.error(f"获取持久卷声明失败{e}")
            raise
