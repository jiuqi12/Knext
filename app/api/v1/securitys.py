from fastapi import APIRouter, Depends
from app.services.securitys.sa_service import SaService
from app.services.securitys.role_service import RoleService
from app.services.securitys.clusterrole_service import ClusterRoleService
from app.services.securitys.rolebinding_service import RoleBindingService
from app.services.securitys.clusterrolebinding_service import ClusterRoleBindingService
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.api.deps import get_current_user
from app.core.k8s_client import get_k8s_client_wrapper, K8sClientWrapper

security_router = APIRouter(dependencies=[Depends(get_current_user)])


# ==================== ServiceAccount 相关接口 ====================
@security_router.get("/sas", response_model=BaseResponse, summary="获取服务账户列表")
async def get_service_accounts(namespace: str = None, k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)):
    """:return: 获取指定命名空间下的服务账户列表"""
    service_accounts = await SaService.list_service_accounts(k8s_wrapper, namespace=namespace)
    return ResponseUtil.success(data=service_accounts, msg="获取服务账户列表成功")


@security_router.get("/sas/{namespace}/{name}", response_model=BaseResponse, summary="获取服务账户详情")
async def get_service_account(namespace: str, name: str,
                              k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)):
    """:return: 获取指定命名空间下的指定服务账户详情"""
    service_account = await SaService.get_service_account(k8s_wrapper, name=name, namespace=namespace)
    return ResponseUtil.success(data=service_account, msg="获取服务账户详情成功")


@security_router.delete("/sas/{namespace}/{name}", response_model=BaseResponse, summary="删除服务账户")
async def delete_service_account(namespace: str, name: str,
                                 k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)):
    """:return: 删除指定的服务账户"""
    result = await SaService.delete_service_account(k8s_wrapper ,name=name, namespace=namespace)
    return ResponseUtil.success(data=result, msg="删除服务账户成功")


# ==================== Role 相关接口 ====================
@security_router.get("/roles", response_model=BaseResponse, summary="获取角色列表")
async def list_roles(namespace: str = None, k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)):
    """:return: 获取指定命名空间下的角色列表"""
    roles = await RoleService.list_roles(namespace=namespace)
    return ResponseUtil.success(data=roles, msg="获取角色列表成功")


@security_router.get("/roles/{namespace}/{name}", response_model=BaseResponse, summary="获取角色详情")
async def get_role(namespace: str, name: str):
    """:return: 获取指定命名空间下的指定角色详情"""
    role = RoleService.get_role(name=name, namespace=namespace)
    return ResponseUtil.success(data=role, msg="获取角色详情成功")


@security_router.delete("/roles/{namespace}/{name}", response_model=BaseResponse, summary="删除角色")
async def delete_role(namespace: str, name: str):
    """:return: 删除指定的角色"""
    result = RoleService.delete_role(name=name, namespace=namespace)
    return ResponseUtil.success(data=result, msg="删除角色成功")


# ==================== ClusterRole 相关接口 ====================
@security_router.get("/clusterroles", response_model=BaseResponse, summary="获取集群角色列表")
async def list_cluster_roles():
    """:return: 获取所有集群角色列表"""
    cluster_roles = ClusterRoleService.list_cluster_roles()
    return ResponseUtil.success(data=cluster_roles, msg="获取集群角色列表成功")


@security_router.get("/clusterroles/{name}", response_model=BaseResponse, summary="获取集群角色详情")
async def get_cluster_role(name: str):
    """:return: 获取指定集群角色详情"""
    cluster_role = ClusterRoleService.get_cluster_role(name=name)
    return ResponseUtil.success(data=cluster_role, msg="获取集群角色详情成功")


@security_router.delete("/clusterroles/{name}", response_model=BaseResponse, summary="删除集群角色")
async def delete_cluster_role(name: str):
    """:return: 删除指定的集群角色"""
    result = ClusterRoleService.delete_cluster_role(name=name)
    return ResponseUtil.success(data=result, msg="删除集群角色成功")


# ==================== RoleBinding 相关接口 ====================
@security_router.get("/rolebindings", response_model=BaseResponse, summary="获取角色绑定列表")
async def list_role_bindings(namespace: str = None):
    """:return: 获取指定命名空间下的角色绑定列表"""
    role_bindings = RoleBindingService.list_role_bindings(namespace)
    return ResponseUtil.success(data=role_bindings, msg="获取角色绑定列表成功")


@security_router.get("/rolebindings/{namespace}/{name}", response_model=BaseResponse, summary="获取角色绑定详情")
async def get_role_binding(name: str, namespace: str = None):
    """:return: 获取指定命名空间下的指定角色绑定详情"""
    role_binding = RoleBindingService.get_role_binding(name=name, namespace=namespace)
    return ResponseUtil.success(data=role_binding, msg="获取角色绑定详情成功")


@security_router.delete("/rolebindings/{namespace}/{name}", response_model=BaseResponse, summary="删除角色绑定")
async def delete_role_binding(name: str, namespace: str = None):
    """:return: 删除指定的角色绑定"""
    result = RoleBindingService.delete_role_binding(name=name, namespace=namespace)
    return ResponseUtil.success(data=result, msg="删除角色绑定成功")


# ==================== ClusterRoleBinding 相关接口 ====================
@security_router.get("/clusterrolebindings", response_model=BaseResponse, summary="获取集群角色绑定列表")
async def list_cluster_role_bindings():
    """:return: 获取所有集群角色绑定列表"""
    cluster_role_bindings = ClusterRoleBindingService.list_cluster_role_bindings()
    return ResponseUtil.success(data=cluster_role_bindings, msg="获取集群角色绑定列表成功")


@security_router.get("/clusterrolebindings/{name}", response_model=BaseResponse, summary="获取集群角色绑定详情")
async def get_cluster_role_binding(name: str):
    """:return: 获取指定集群角色绑定详情"""
    cluster_role_binding = ClusterRoleBindingService.get_cluster_role_binding(name=name)
    return ResponseUtil.success(data=cluster_role_binding, msg="获取集群角色绑定详情成功")


@security_router.delete("/clusterrolebindings/{name}", response_model=BaseResponse, summary="删除集群角色绑定")
async def delete_cluster_role_binding(name: str):
    """:return: 删除指定的集群角色绑定"""
    result = ClusterRoleBindingService.delete_cluster_role_binding(name)
    return ResponseUtil.success(data=result, msg="删除集群角色绑定成功")
