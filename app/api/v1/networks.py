from fastapi import APIRouter, Query, Depends
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.services.networks.service_service import ServiceService
from app.services.networks.ingress_service import IngressService
from app.api.deps import get_current_user
from app.core.k8s_client import get_k8s_client_wrapper, K8sClientWrapper


network_router = APIRouter(dependencies=[Depends(get_current_user)])


# service相关
@network_router.get("/services", response_model=BaseResponse, summary="列出Service列表")
async def list_services(namespace: str = Query(None, description="名称空间"),
                        k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)):
    """
    列出Service列表
    - **namespace**: 命名空间（可选）
    - **return**: services列表
    """
    services = await ServiceService.list_services(namespace, k8s_wrapper)
    return ResponseUtil.success(data=services, msg="获取service列表成功")


@network_router.get("/services/{namespace}/{service_name}", response_model=BaseResponse, summary="获取指定Service")
async def get_service(namespace: str, service_name: str,
                      k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)):
    """
    获取指定service的详细信息
    - **namespace**: 命名空间
    - **service_name**: service名称
    :return:
    """
    service = await ServiceService.get_service(namespace, service_name, k8s_wrapper)
    return ResponseUtil.success(data=service, msg=f"获取{service_name}成功")


@network_router.delete("/services/{namespace}/{service_name}", response_model=BaseResponse, summary="删除指定Service")
async def delete_service(namespace: str, service_name: str,
                         k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)):
    """
    删除指定的service
    - **namespace**: 命名空间
    - **service_name**: service名字
    - **return**: 指定service的名称
    """
    data = await ServiceService.delete_service(namespace, service_name, k8s_wrapper)
    return ResponseUtil.success(data=data, msg=f"删除{service_name}成功")


# ingress相关
@network_router.get("/ingresses", response_model=BaseResponse, summary="列出Ingress列表")
async def list_ingresses(namespace: str = Query(None, description="名称空间")):
    """
    列出ingress的列表
    - **namespace**: 命名空间（可选）
    - **return**: 命名空间列表
    """
    ingresses = await IngressService.list_ingresses(namespace)
    return ResponseUtil.success(data=ingresses, msg="获取ingress列表成功")


@network_router.get("/ingresses/{namespace}/{ingress_name}", response_model=BaseResponse, summary="获取指定Ingress")
async def get_ingress(namespace: str, ingress_name: str):
    """
    获取指定的Ingress
    - **namespace**: 命名空间
    - **ingress_name**: ingress的名称
    - **return**: Ingress详细信息
    """
    ingress = await IngressService.get_ingress(namespace, ingress_name)
    return ResponseUtil.success(data=ingress, msg=f"获取{ingress_name}成功")


@network_router.delete("/ingresses/{namespace}/{ingress_name}", response_model=BaseResponse, summary="删除指定Ingress")
async def delete_ingress(namespace: str, ingress_name: str):
    """
    删除指定的Ingress
    - **namespace**: 命名空间
    - **ingress_name**: ingress的名称
    - **return**: Ingress的名称
    """
    data = await IngressService.delete_ingress(namespace, ingress_name)
    return ResponseUtil.success(data=data, msg=f"删除{ingress_name}成功")


# # gateway相关
# @network_router.get("/gateways", response_model=BaseResponse, summary="列出Gateway列表")
# async def list_gateways(namespace: str = Query(None, description="名称空间")):
#     """
#     列出gateway的列表
#     - **namespace**: 命名空间（可选）
#     - **return**: 命名空间列表
#     """
#     gateways = ServiceService.list_gateways(namespace)
#     return ResponseUtil.success(data=gateways, msg="获取网络成功")
#
#
# @network_router.get("/gateways/{namespace}/{gateway_name}", response_model=BaseResponse, summary="获取指定Gateway")
# async def get_gateway(namespace: str, gateway_name: str):
#     """
#     获取指定的Gateway
#     - **namespace**: 命名空间
#     - **gateway_name**: gateway的名称
#     - **return**: Gateway详细信息
#     """
#     gateway = ServiceService.get_gateway(namespace, gateway_name)
#     return ResponseUtil.success(data=gateway, msg="获取网络成功")
#
#
# @network_router.delete("/gateways/{namespace}/{gateway_name}", response_model=BaseResponse, summary="删除指定Gateway")
# async def delete_gateway(namespace: str, gateway_name: str):
#     """
#     删除指定的Gateway
#     - **namespace**: 命名空间
#     - **gateway_name**: gateway的名称
#     - **return**: Gateway的名称
#     """
#     data = ServiceService.delete_gateway(namespace, gateway_name)
#     return ResponseUtil.success(data=data, msg="删除网络成功")