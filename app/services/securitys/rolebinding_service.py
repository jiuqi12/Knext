from app.core.k8s_client import get_core_v1_api
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import Dict, Any, List


class RoleBindingService:
    @staticmethod
    def get_role_bindings(namespace: str = "default") -> List[Dict[str, Any]]:
        """获取指定命名空间下的所有角色绑定"""
        try:
            v1 = get_core_v1_api()
            role_binding_list = v1.list_namespaced_role_binding(namespace=namespace).items
            return [
                {
                    "name": rb.metadata.name,
                    "namespace": rb.metadata.namespace,
                    "labels": rb.metadata.labels,
                    "annotations": rb.metadata.annotations,
                    "creation_time": rb.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                } for rb in role_binding_list
            ]
        except ApiException as e:
            logger.error(f"获取角色绑定列表失败：{e}")
            raise
        except Exception as e:
            logger.error(f"获取角色绑定列表失败：{e}")
            raise

    @staticmethod
    def delete_role_binding(name: str, namespace: str = "default") -> Dict[str, Any]:
        """删除指定角色绑定"""
        try:
            v1 = get_core_v1_api()
            status = v1.delete_namespaced_role_binding(name=name, namespace=namespace)
            logger.info(f"删除角色绑定 {name} 成功")
            return {"message": f"角色绑定 {name} 已删除", "status": status.status}
        except ApiException as e:
            logger.error(f"删除角色绑定失败：{e}")
            raise
        except Exception as e:
            logger.error(f"删除角色绑定失败：{e}")
            raise