from fastapi import APIRouter, Depends, status
from app.services.overview_service import OverviewService
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.api.deps import get_current_user
from app.core.k8s_client import get_k8s_client_wrapper, K8sClientWrapper

overview_router = APIRouter()


# 获取 overview 统计信息
@overview_router.get("", response_model=BaseResponse, summary="获取集群概览")
async def get_overview(
    current_user=Depends(get_current_user),
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """获取集群概览信息，包括节点、Pod、Deployment 等的统计"""
    print(current_user)
    if not current_user['is_admin']:
        return ResponseUtil.error(msg="无权限", code=status.HTTP_403_FORBIDDEN)
    overview = await OverviewService.get_overview(k8s_wrapper)
    return ResponseUtil.success(data=overview, msg="获取概览成功")

