# 资源请求逻辑
from typing import Any, Dict
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import get_api_client
from kubernetes.dynamic import DynamicClient
from kubernetes.dynamic.exceptions import ResourceNotFoundError
from app.utils.logger import logger
import yaml


class ResourceService:
    """创建资源类"""

    @staticmethod
    def create_resource_yaml(yaml_content: dict):
        # 创建动态客户端
        v1 = get_api_client()
        dyn_client = DynamicClient(v1)
        # 提取必要字段
        api_version = yaml_content.get("apiVersion")
        kind = yaml_content.get("kind")
        metadata = yaml_content.get("metadata", {})
        name = metadata.get("name")
        namespace = metadata.get("namespace", "default")  # 如果未指定默认使用default

        if not api_version or not kind or not name:
            raise ValueError("资源缺少核心字段，请检查")

        try:
            resource = dyn_client.resources.get(api_version=api_version, kind=kind)
        except ResourceNotFoundError as e:
            logger.info(f"资源创建失败，未找到该资源类型：{api_version}/{kind}")
            raise ValueError(f"资源创建失败未找到该资源类型：{api_version}/{kind}")
        except Exception as e:
            logger.info(f"资源创建失败")
            raise

        # 创建资源
        resp = dyn_client.server_side_apply(resource=resource,
                                            body=yaml_content,
                                            name=name,
                                            field_manager="admin",
                                            namespace=namespace)
        return {
            "kind": kind,
            "name": name,
            "status": "success"
        }
