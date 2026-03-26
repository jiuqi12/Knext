from typing import List, Dict, Any
from app.core.k8s_client import get_core_v1_api
from app.utils.logger import logger


class NamespaceService:
    """命名空间服务类"""

    @staticmethod
    def get_namespaces() -> List[Dict[str, Any]]:
        # 获取所有命名空间
        try:
            v1 = get_core_v1_api()
            namespace_list = v1.list_namespace()
            logger.info(f"获取所有命名空间成功")
            return [
                {
                    "name": ns.metadata.name,
                    "status": ns.status.phase,
                    "labels": ns.metadata.labels,
                    "creation_time": ns.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "annotations": ns.metadata.annotations,
                }for ns in namespace_list.items
            ]
        except Exception as e:
            logger.error(f"获取所有命名空间失败：{e}")
            raise

    @staticmethod
    def create_namespace(yaml_content: str) -> Dict[str, Any]:
        """
        创建命名空间
        :param yaml_content: 要创建的命名空间的名字
        :return: 创建成功的信息
        """
        try:
            v1 = get_core_v1_api()
            namespace = v1.create_namespace()
            return namespace
        except Exception as e:
            logger.error(f"创建命名空间失败：{e}")
            raise

    @staticmethod
    def delete_namespace(namespace_name: str) -> Dict[str, Any]:
        # 删除命名空间
        """
        删除命名空间
        :param namespace_name: 命名空间名称
        :return: 返回被删除的命名空间名称
        """
        try:
            v1 = get_core_v1_api()
            status = v1.delete_namespace(name=namespace_name)
            logger.info(f"删除命名空间{status.status}")
            return status.status
        except Exception as e:
            logger.error(f"删除命名空间失败：{e}")
            raise
