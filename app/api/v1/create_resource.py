from fastapi import APIRouter, Depends, Request
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.services.resource_service import ResourceService
from app.api.deps import get_current_user
from app.core.k8s_client import get_k8s_client_wrapper, K8sClientWrapper

create_resource_router = APIRouter(dependencies=[Depends(get_current_user)])


# 通过yaml创建资源
@create_resource_router.post("", response_model=BaseResponse, summary="通过yaml创建资源，前端提供资源模板")
async def create_resource_from_yaml(
    request: Request,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    通过yaml创建资源
    -- **request**: yaml文件
    -- **return**:
    """
    yaml_body = await request.body()
    result = await ResourceService.create_resource_yaml(yaml_body, k8s_wrapper)
    return ResponseUtil.success(data=result, msg="创建资源成功")

