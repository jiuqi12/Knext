from typing import Any, Dict, List
from datetime import datetime
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import get_core_v1_api, get_apps_v1_api
from app.utils.logger import logger


class DeploymentService:
    @staticmethod
    def list_deployments(namespace: str = None) -> List[Dict[str, Any]]:
        """列出工作负载"""
        try:
            apps_v1 = get_apps_v1_api()
            if namespace:
                deploy_list = apps_v1.list_namespaced_deployment(namespace)
            else:
                deploy_list = apps_v1.list_deployment_for_all_namespaces()

            return [{
                "name": deploy.metadata.name,
                "namespace": deploy.metadata.namespace,
                "replicas": deploy.spec.replicas,
                "ready_replicas": deploy.status.ready_replicas or 0,
                "created_at": deploy.metadata.creation_timestamp
            } for deploy in deploy_list.items]
        except ApiException as e:
            logger.error(f"列出工作负载失败：{e}")
            raise
        except Exception as e:
            logger.error(f"列出工作负载失败：{e}")
            raise
