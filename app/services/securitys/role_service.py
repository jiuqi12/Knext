from app.core.k8s_client import get_core_v1_api
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import Dict, Any, List


class RoleService:
    @staticmethod
    def get_roles(namespace: str = "default") -> List[Dict[str, Any]]:
        """获取指定命名空间下的所有角色"""
        try:
            v1 = get_core_v1_api()
            role_list = v1.list_namespaced_role(namespace=namespace).items
            return [
                {
                    "name": role.metadata.name,
                    "namespace": role.metadata.namespace,
                    "labels": role.metadata.labels,
                    "annotations": role.metadata.annotations,
                    "creation_time": role.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                } for role in role_list
            ]
        except ApiException as e:
            logger.error(f"获取角色列表失败：{e}")
            raise
        except Exception as e:
            logger.error(f"获取角色列表失败：{e}")
            raise

    @staticmethod
    def delete_role(name: str, namespace: str = "default") -> Dict[str, Any]:
        """删除指定角色"""
        try:
            v1 = get_core_v1_api()
            status = v1.delete_namespaced_role(name=name, namespace=namespace)
            logger.info(f"删除角色 {name} 成功")
            return {"message": f"角色 {name} 已删除", "status": status.status}
        except ApiException as e:
            logger.error(f"删除角色失败：{e}")
            raise
        except Exception as e:
            logger.error(f"删除角色失败：{e}")
            raise