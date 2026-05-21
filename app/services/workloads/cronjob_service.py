from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import K8sClientWrapper
from typing import Dict, Any, List
from app.utils.logger import logger


class CronjobService:
    @staticmethod
    async def list_cronjobs(namespace: str = None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取 cronjob 列表"""
        batch_v1 = await k8s_wrapper.get_batch_v1_api()
        try:
            if namespace:
                cronjob_list = batch_v1.list_namespaced_cron_job(namespace).items
            else:
                cronjob_list = batch_v1.list_cron_job_for_all_namespaces().items
                logger.info(f"获取cronjob列表成功共：{len(cronjob_list)}")
            return [
                {
                    "name": cronjob.metadata.name,
                    "namespace": cronjob.metadata.namespace,
                    "status": cronjob.status.active,
                    "labels": cronjob.metadata.labels,
                    "creation_time": cronjob.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                } for cronjob in cronjob_list
            ]
        except ApiException as e:
            logger.error(f"获取 cronjob 列表失败：{e}")
            raise

    @staticmethod
    async def delete_cronjob(cronjob_name: str, namespace: str, k8s_wrapper: K8sClientWrapper = None) -> str:
        """删除 cronjob"""
        batch_v1 = await k8s_wrapper.get_batch_v1_api()
        try:
            batch_v1.delete_namespaced_cron_job(cronjob_name, namespace)
            logger.info(f"删除 cronjob {cronjob_name} 成功")
            return f"删除cronjob{cronjob_name}成功"
        except ApiException as e:
            logger.error(f"删除 cronjob {cronjob_name} 失败：{e}")
            raise
