from app.core.k8s_client import get_core_v1_api
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import Dict, Any, List


class ClusterRoleBindingService:
    @staticmethod
    def get_cluster_role_bindings() -> List[Dict[str, Any]]:
        """获取所有集群角色绑定"""
        try:
            v1 = get_core_v1_api()
            cluster_role_binding_list = v1.list_cluster_role_binding().items
            return [
                {
                    "name": crb.metadata.name,
                    "labels": crb.metadata.labels,
                    "annotations": crb.metadata.annotations,
                    "creation_time": crb.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                } for crb in cluster_role_binding_list
            ]
        except ApiException as e:
            logger.error(f"获取集群角色绑定列表失败：{e}")
            raise
        except Exception as e:
            logger.error(f"获取集群角色绑定列表失败：{e}")
            raise

    @staticmethod
    def delete_cluster_role_binding(name: str) -> Dict[str, Any]:
        """删除指定集群角色绑定"""
        try:
            v1 = get_core_v1_api()
            status = v1.delete_cluster_role_binding(name=name)
            logger.info(f"删除集群角色绑定 {name} 成功")
            return {"message": f"集群角色绑定 {name} 已删除", "status": status.status}
        except ApiException as e:
            logger.error(f"删除集群角色绑定失败：{e}")
            raise
        except Exception as e:
            logger.error(f"删除集群角色绑定失败：{e}")
            raise