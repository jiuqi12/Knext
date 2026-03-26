from fastapi import APIRouter, HTTPException, Query
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.utils.logger import logger
from app.services.workloads.pod_service import PodService
from app.services.workloads.deployment_service import DeploymentService
from app.services.workloads.daemonset_service import DaemonSetsService
from app.services.workloads.statefulset_service import StatefulSetService

workload_router = APIRouter()


# pod容器组相关
# 获取Pod容器组列表
@workload_router.get("/pods", response_model=BaseResponse, summary="获取Pod列表")
async def list_workloads( namespace: str = Query(None, description="名称空间")):
    """
    获取Pod容器组
    - **namespace**: 命名空间（可选）
    """
    try:
        pod_list = PodService.get_pods(namespace)
        return ResponseUtil.success(data=pod_list, msg="获取工作负载成功")
    except ValueError as e:
        logger.error(f"列出工作负载失败：{e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取工作负载失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取工作负载失败：{str(e)}")

# 删除Pod容器组


# 获取Deployment列表
@workload_router.get("/deployments", response_model=BaseResponse, summary="获取Deployment列表")
async def list_deployments( namespace: str = Query(None, description="名称空间")):
    """
    获取Deployment列表
    - **namespace**: 命名空间（可选）
    """
    try:
        deploy_list = DeploymentService.list_deployments(namespace)
        return ResponseUtil.success(data=deploy_list, msg="获取工作负载成功")
    except ValueError as e:
        logger.error(f"列出工作负载失败：{e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取工作负载失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取工作负载失败：{str(e)}")

# 删除deployment

# 获取DaemonSet列表
@workload_router.get("/daemonsets", response_model=BaseResponse, summary="获取DaemonSet列表")
async def list_daemonsets( namespace: str = Query(None, description="名称空间")):
    """
    获取DaemonSet列表
    - **namespace**: 命名空间（可选）
    """
    try:
        ds_list = DaemonSetsService.list_daemonsets(namespace)
        return ResponseUtil.success(data=ds_list, msg="获取工作负载成功")
    except ValueError as e:
        logger.error(f"列出工作负载失败：{e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取工作负载失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取工作负载失败：{str(e)}")

# 删除DaemonSet

# 获取statefuleset列表
@workload_router.get("/statefulsets", response_model=BaseResponse, summary="获取statefuleset列表")
async def list_statefulsets( namespace: str = Query(None, description="名称空间")):
    """
    获取statefuleset列表
    - **namespace**: 命名空间（可选）
    """
    try:
        sts_list = StatefulSetService.list_statefulsets(namespace)
        return ResponseUtil.success(data=sts_list, msg="获取工作负载成功")
    except ValueError as e:
        logger.error(f"列出工作负载失败：{e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取工作负载失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取工作负载失败：{str(e)}")

# 删除statefulset
