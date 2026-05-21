from typing import Any, Dict, List
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import K8sClientWrapper
from app.utils.logger import logger


class DeploymentService:
    @staticmethod
    async def list_deployments(namespace: str = None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """列出工作负载"""
        try:
            apps_v1 = await k8s_wrapper.get_apps_v1_api()
            if namespace:
                deploy_list = apps_v1.list_namespaced_deployment(namespace)
            else:
                deploy_list = apps_v1.list_deployment_for_all_namespaces()

            result = []
            for deploy in deploy_list.items:
                # 容器信息
                containers = []
                if deploy.spec.template.spec.containers:
                    containers = [
                        {
                            "name": c.name,
                            "image": c.image,
                        }
                        for c in deploy.spec.template.spec.containers
                    ]

                # 更新策略
                strategy_type = "RollingUpdate"
                if deploy.spec.strategy:
                    strategy_type = deploy.spec.strategy.type or "RollingUpdate"

                # 状态条件
                conditions = []
                if deploy.status.conditions:
                    conditions = [
                        {
                            "type": c.type,
                            "status": c.status,
                            "reason": c.reason,
                            "message": c.message,
                        }
                        for c in deploy.status.conditions
                    ]

                result.append({
                    "name": deploy.metadata.name,
                    "namespace": deploy.metadata.namespace,
                    "uid": deploy.metadata.uid,
                    "labels": deploy.metadata.labels or {},
                    "replicas": {
                        "desired": deploy.spec.replicas or 0,
                        "ready": deploy.status.ready_replicas or 0,
                        "available": deploy.status.available_replicas or 0,
                        "updated": deploy.status.updated_replicas or 0,
                        "unavailable": deploy.status.unavailable_replicas or 0,
                    },
                    "status": f"{deploy.status.ready_replicas or 0} / {deploy.spec.replicas or 0}",
                    "strategy": strategy_type,
                    "containers": containers,
                    "selector": deploy.spec.selector.match_labels if deploy.spec.selector else {},
                    "conditions": conditions,
                    "created_at": deploy.metadata.creation_timestamp,
                })
            return result
        except ApiException as e:
            logger.error(f"列出工作负载失败：{e}")
            raise

    @staticmethod
    async def scale_deployment(deploy_name: str, namespace: str, replicas: int, k8s_wrapper: K8sClientWrapper = None) -> dict:
        """扩缩容工作负载"""
        try:
            apps_v1 = await k8s_wrapper.get_apps_v1_api()
            body = {"spec": {"replicas": replicas}}
            deploy = apps_v1.patch_namespaced_deployment_scale(
                name=deploy_name,
                namespace=namespace,
                body=body
            )
            logger.info(f"扩缩容成功：{deploy_name} -> {replicas} 副本")
            return {
                "name": deploy.metadata.name,
                "namespace": deploy.metadata.namespace,
                "replicas": {
                    "desired": deploy.spec.replicas or 0,
                    "ready": deploy.status.ready_replicas or 0,
                    "available": deploy.status.available_replicas or 0,
                    "updated": deploy.status.updated_replicas or 0,
                },
            }
        except ApiException as e:
            logger.error(f"扩缩容工作负载失败：{e}")
            raise

    @staticmethod
    async def delete_deployment(deploy_name: str, namespace: str, k8s_wrapper: K8sClientWrapper = None) -> str:
        """删除工作负载"""
        try:
            apps_v1 = await k8s_wrapper.get_apps_v1_api()
            apps_v1.delete_namespaced_deployment(deploy_name, namespace)
            return deploy_name
        except ApiException as e:
            logger.error(f"删除工作负载失败：{e}")
            raise
