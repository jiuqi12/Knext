from app.services.namespace_service import NamespaceService
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.core.k8s_client import get_k8s_client_wrapper, K8sClientWrapper

namespace_router = APIRouter(dependencies=[Depends(get_current_user)])


@namespace_router.get("", response_model=BaseResponse, summary="获取全部的命名空间")
async def get_namespaces(k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)):
    """获取全部命名空间"""
    namespaces = await NamespaceService.get_namespaces(k8s_wrapper)
    return ResponseUtil.success(data=namespaces, msg="获取命名空间成功")


@namespace_router.delete("/{namespace_name}", response_model=BaseResponse, summary="删除命名空间")
async def delete_namespace(
    namespace_name: str,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    删除命名空间
    - **namespace_name**: 命名空间名称:
    - **return**: 删除状态
    """
    status = await NamespaceService.delete_namespace(namespace_name, k8s_wrapper)
    return ResponseUtil.success(data=status, msg="删除命名空间成功")
