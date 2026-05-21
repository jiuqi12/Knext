from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import K8sClientWrapper
from typing import Dict, Any, List
from app.utils.logger import logger


class JobService:
    @staticmethod
    async def list_jobs(namespace: str = None, k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取 job 列表"""
        batch_v1 = await k8s_wrapper.get_batch_v1_api()
        try:
            if namespace:
                job_list = batch_v1.list_namespaced_job(namespace).items
            else:
                job_list = batch_v1.list_job_for_all_namespaces().items
            logger.info(f"获取job列表成功共：{len(job_list)}")
            return [
                {
                    "name": job.metadata.name,
                    "namespace": job.metadata.namespace,
                    "status": job.status.succeeded,
                    "labels": job.metadata.labels,
                    "creation_time": job.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                } for job in job_list
            ]
        except ApiException as e:
            logger.error(f"获取 job 列表失败：{e}")
            raise

    @staticmethod
    async def delete_job(job_name: str, namespace: str, k8s_wrapper: K8sClientWrapper = None) -> str:
        """删除 job"""
        batch_v1 = await k8s_wrapper.get_batch_v1_api()
        try:
            batch_v1.delete_namespaced_job(job_name, namespace)
            logger.info(f"删除 job {job_name} 成功")
            return f"删除job{job_name}成功"
        except ApiException as e:
            logger.error(f"删除 job {job_name} 失败：{e}")
