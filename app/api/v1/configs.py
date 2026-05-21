from fastapi import APIRouter, Query, Depends
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.services.configs.configmap_service import ConfigMapService
from app.services.configs.secret_service import SecretService
from app.api.deps import get_current_user
from app.core.k8s_client import get_k8s_client_wrapper, K8sClientWrapper

config_router = APIRouter(dependencies=[Depends(get_current_user)])


# configmap相关接口
@config_router.get("/configmaps", response_model=BaseResponse, summary="获取configmaps列表")
async def list_configmaps(
    namespace: str = Query(None, description="名称空间"),
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    获取ConfigMap列表
    - **namespace**: 命名空间（可选）
    """
    configmaps = await ConfigMapService.list_configmaps(namespace, k8s_wrapper)
    return ResponseUtil.success(data=configmaps, msg="获取configmaps成功")


@config_router.get("/configmaps/{namespace}/{configmap_name}", response_model=BaseResponse, summary="获取指定configmap")
async def get_configmap(
    namespace: str,
    configmap_name: str,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    获取configmap的详细信息
    - **configmap_name**: configmap名称
    - **namespace**: 命名空间名称
    - **return**的：configmap的详细信息
    """
    configmap = await ConfigMapService.get_configmap(namespace, configmap_name, k8s_wrapper)
    return ResponseUtil.success(data=configmap, msg="获取configmap成功")


@config_router.delete("/configmaps/{namespace}/{configmap_name}", response_model=BaseResponse, summary="删除指定configmap")
async def delete_configmap(
    namespace: str,
    configmap_name: str,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    删除configmap
    - **configmap_name**: configmap名称
    - **namespace**: 命名空间名称
    - **return**: 被删除的confmgpa名称
    """
    status = await ConfigMapService.delete_configmap(namespace, configmap_name, k8s_wrapper)
    return ResponseUtil.success(data=status, msg="删除configmap成功")


# secret相关接口
@config_router.get("/secrets", response_model=BaseResponse, summary="获取secrets列表")
async def list_secrets(
    namespace: str = Query(None, description="名称空间"),
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    获取Secret列表
    - **namespace**: 命名空间（可选）
    """
    secrets = await SecretService.list_secrets(namespace, k8s_wrapper)
    return ResponseUtil.success(data=secrets, msg="获取secrets成功")


@config_router.get("/secrets/{namespace}/{secret_name}", response_model=BaseResponse, summary="获取指定secret")
async def get_secret(
    namespace: str,
    secret_name: str,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    获取secret详细信息
    - **secret_name**: secret名称
    - **namespace**: 命名空间名称
    - **return**: secret的详细信息
    """
    secret = await SecretService.get_secret(namespace, secret_name, k8s_wrapper)
    return ResponseUtil.success(data=secret, msg="获取secret成功")


@config_router.delete("/secrets/{namespace}/{secret_name}", response_model=BaseResponse, summary="删除指定secret")
async def delete_secret(
    namespace: str,
    secret_name: str,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    删除secret
    - **param**：secret_name: secret名称
    - **param**：namespace: 命名空间名称
    - **return**: 删除结果
    """
    status = await SecretService.delete_secret(secret_name, namespace, k8s_wrapper)
    return ResponseUtil.success(data=status, msg="删除secret成功")
