from fastapi import APIRouter, Query, Depends
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.services.workloads.pod_service import PodService
from app.services.workloads.deployment_service import DeploymentService
from app.services.workloads.daemonset_service import DaemonSetsService
from app.services.workloads.statefulset_service import StatefulSetService
from app.services.workloads.job_service import JobService
from app.services.workloads.cronjob_service import CronjobService
from app.api.deps import get_current_user
from app.core.k8s_client import get_k8s_client_wrapper, K8sClientWrapper

workload_router = APIRouter(dependencies=[Depends(get_current_user)])


@workload_router.get("/pods", response_model=BaseResponse, summary="获取Pod列表")
async def list_pods(
    namespace: str = Query(None, description="名称空间"),
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    获取Pod容器组
    - **namespace**: 命名空间（可选）
    """
    pod_list = await PodService.list_pods(namespace, k8s_wrapper)
    return ResponseUtil.success(data=pod_list, msg="获取Pods列表成功")


@workload_router.delete("/pods/{namespace}/{pod_name}", response_model=BaseResponse, summary="删除Pod容器组")
async def delete_pod(
    pod_name: str,
    namespace: str,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    删除Pod容器组
    - **pod_name**: Pod名称
    - **namespace**: 命名空间
    """
    pod_name = await PodService.delete_pod(pod_name, namespace, k8s_wrapper)
    return ResponseUtil.success(data=pod_name, msg="删除Pod成功")


@workload_router.get("/deployments", response_model=BaseResponse, summary="获取Deployment列表")
async def list_deployments(
    namespace: str = Query(None, description="名称空间"),
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    获取Deployment列表
    - **namespace**: 命名空间（可选）
    """
    deploy_list = await DeploymentService.list_deployments(namespace, k8s_wrapper)
    return ResponseUtil.success(data=deploy_list, msg="获取Deployments列表成功")


@workload_router.patch("/deployments/{namespace}/{deploy_name}/scale", response_model=BaseResponse, summary="扩缩容Deployment")
async def scale_deployment(
    deploy_name: str,
    namespace: str,
    replicas: int = Query(..., description="目标副本数"),
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    扩缩容 Deployment
    - **deploy_name**: Deployment 名称
    - **namespace**: 命名空间
    - **replicas**: 目标副本数
    """
    result = await DeploymentService.scale_deployment(deploy_name, namespace, replicas, k8s_wrapper)
    return ResponseUtil.success(data=result, msg=f"扩缩容成功，当前副本数：{result['replicas']}")


@workload_router.delete("/deployments/{namespace}/{deploy_name}", response_model=BaseResponse, summary="删除Deployment")
async def delete_deployment(
    deploy_name: str,
    namespace: str,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    删除Deployment
    - **deploy_name**: Deployment名称
    - **namespace**: 命名空间
    """
    deploy_name = await DeploymentService.delete_deployment(deploy_name, namespace, k8s_wrapper)
    return ResponseUtil.success(data=deploy_name, msg="删除Deployment成功")


@workload_router.get("/daemonsets", response_model=BaseResponse, summary="获取DaemonSet列表")
async def list_daemonsets(
    namespace: str = Query(None, description="名称空间"),
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    获取DaemonSet列表
    - **namespace**: 命名空间（可选）
    """
    ds_list = await DaemonSetsService.list_daemonsets(namespace, k8s_wrapper)
    return ResponseUtil.success(data=ds_list, msg="获取Daemonsets列表成功")


@workload_router.delete("/daemonsets/{namespace}/{ds_name}", response_model=BaseResponse, summary="删除DaemonSet")
async def delete_daemonset(
    ds_name: str,
    namespace: str,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    删除DaemonSet
    - **ds_name**: DaemonSet名称
    - **namespace**: 命名空间
    """
    ds_name = await DaemonSetsService.delete_daemonset(ds_name, namespace, k8s_wrapper)
    return ResponseUtil.success(data=ds_name, msg="删除DaemonSet成功")


@workload_router.get("/statefulsets", response_model=BaseResponse, summary="获取statefuleset列表")
async def list_statefulsets(
    namespace: str = Query(None, description="名称空间"),
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    获取statefuleset列表
    - **namespace**: 命名空间（可选）
    """
    sts_list = await StatefulSetService.list_statefulsets(namespace, k8s_wrapper)
    return ResponseUtil.success(data=sts_list, msg="获取StatefulSets列表成功")


@workload_router.delete("/statefulsets/{namespace}/{sts_name}", response_model=BaseResponse, summary="删除statefuleset")
async def delete_statefulset(
    sts_name: str,
    namespace: str,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    删除statefuleset
    - **sts_name**: statefuleset名称
    - **namespace**: 命名空间
    """
    sts_name = await StatefulSetService.delete_statefulset(sts_name, namespace, k8s_wrapper)
    return ResponseUtil.success(data=sts_name, msg="删除statefuleset成功")


@workload_router.get("/jobs/", response_model=BaseResponse, summary="获取Job详情")
async def list_jobs(
    namespace: str = Query(None, description="名称空间"),
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    获取Job列表
    - **namespace**: 命名空间
    """
    job = await JobService.list_jobs(namespace, k8s_wrapper)
    return ResponseUtil.success(data=job, msg="获取Job成功")


@workload_router.delete("/jobs/{namespace}/{job_name}", response_model=BaseResponse, summary="删除Job")
async def delete_job(
    job_name: str,
    namespace: str,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    删除Job
    - **job_name**: Job名称
    - **namespace**: 命名空间
    """
    job_name = await JobService.delete_job(job_name, namespace, k8s_wrapper)
    return ResponseUtil.success(data=job_name, msg="删除Job成功")


@workload_router.get("/cronjobs", response_model=BaseResponse, summary="获取CronJob列表")
async def list_cronjobs(
    namespace: str = Query(None, description="名称空间"),
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    获取CronJob列表
    - **namespace**: 命名空间（可选）
    """
    cron_job_list = await CronjobService.list_cronjobs(namespace, k8s_wrapper)
    return ResponseUtil.success(data=cron_job_list, msg="获取CronJob成功")


@workload_router.delete("/cronjobs/{namespace}/{cron_job_name}", response_model=BaseResponse, summary="删除CronJob")
async def delete_cronjob(
    cron_job_name: str,
    namespace: str,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    删除CronJob
    - **cron_job_name**: CronJob名称
    - **namespace**: 命名空间
    """
    cron_job_name = await CronjobService.delete_cronjob(cron_job_name, namespace, k8s_wrapper)
    return ResponseUtil.success(data=cron_job_name, msg="删除CronJob成功")
