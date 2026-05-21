from typing import Any, Dict, List
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import K8sClientWrapper
from app.utils.logger import logger


class PersistentVolumeClaimService:
    @staticmethod
    async def list_persistent_volume_claims(namespace: str = None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取持久卷声明列表"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            if namespace:
                pvc_list = v1.list_namespaced_persistent_volume_claim(namespace)
                logger.info(f"获取{namespace}命名空间下持久卷声明列表成功")
            else:
                pvc_list = v1.list_persistent_volume_claim_for_all_namespaces()
                logger.info(f"获取持久卷声明列表成功")
            return [
                {
                    "name": pvc.metadata.name,
                    "status": pvc.status.phase,
                    "access_modes": pvc.spec.access_modes,
                    "storage_class": pvc.spec.storage_class_name,
                    "volume_name": pvc.spec.volume_name,
                    "creation_time": pvc.metadata.creation_timestamp
                } for pvc in pvc_list.items
            ]
        except ApiException as e:
            logger.error(f"获取持久卷声明失败{e}")
            raise

    @staticmethod
    async def get_persistent_volume_claim(pvc_name: str, namespace: str = None, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """获取指定持久卷声明"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            pvc = v1.read_namespaced_persistent_volume_claim(name=pvc_name, namespace=namespace)
            logger.info(f"获取{namespace}命名空间下持久卷声明{pvc_name}成功")
            return {
                "name": pvc.metadata.name,
                "status": pvc.status.phase,
                "access_modes": pvc.spec.access_modes,
                "storage_class": pvc.spec.storage_class_name,
                "volume_name": pvc.spec.volume_name,
                "creation_time": pvc.metadata.creation_timestamp
            }
        except ApiException as e:
            logger.error(f"获取持久卷声明{pvc_name}失败{e}")
            raise

    @staticmethod
    async def delete_persistent_volume_claim(pvc_name: str, namespace: str = None, k8s_wrapper: K8sClientWrapper = None) -> str:
        """删除指定持久卷声明"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            v1.delete_namespaced_persistent_volume_claim(name=pvc_name, namespace=namespace)
            logger.info(f"删除{namespace}命名空间下持久卷声明{pvc_name}成功")
            return f"删除持久卷声明{pvc_name}成功"
        except ApiException as e:
            logger.error(f"删除持久卷声明{pvc_name}失败{e}")
            raise
