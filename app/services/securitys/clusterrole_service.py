from app.core.k8s_client import get_core_v1_api
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import Dict, Any, List


class ClusterRoleService:
    @staticmethod
    def get_cluster_roles() -> List[Dict[str, Any]]:
        """获取所有集群角色"""
        try:
            v1 = get_core_v1_api()
            cluster_role_list = v1.list_cluster_role().items
            return [
                {
                    "name": cr.metadata.name,
                    "labels": cr.metadata.labels,
                    "annotations": cr.metadata.annotations,
                    "creation_time": cr.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                } for cr in cluster_role_list
            ]
        except ApiException as e:
            logger.error(f"获取集群角色列表失败：{e}")
            raise
        except Exception as e:
            logger.error(f"获取集群角色列表失败：{e}")
            raise

    @staticmethod
    def delete_cluster_role(name: str) -> Dict[str, Any]:
        """删除指定集群角色"""
        try:
            v1 = get_core_v1_api()
            status = v1.delete_cluster_role(name=name)
            logger.info(f"删除集群角色 {name} 成功")
            return {"message": f"集群角色 {name} 已删除", "status": status.status}
        except ApiException as e:
            logger.error(f"删除集群角色失败：{e}")
            raise
        except Exception as e:
            logger.error(f"删除集群角色失败：{e}")
            raise