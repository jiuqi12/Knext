from fastapi import APIRouter, HTTPException
from app.services.securitys.sa_service import SaService
from app.services.securitys.role_service import RoleService
from app.services.securitys.clusterrole_service import ClusterRoleService
from app.services.securitys.rolebinding_service import RoleBindingService
from app.services.securitys.clusterrolebinding_service import ClusterRoleBindingService
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.utils.logger import logger

security_router = APIRouter()


# ==================== ServiceAccount 相关接口 ====================
@security_router.get("/serviceaccounts", response_model=BaseResponse, summary="获取服务账户列表")
async def get_service_accounts(namespace: str = "default"):
    """:return: 获取指定命名空间下的服务账户列表"""
    try:
        service_accounts = SaService.get_service_accounts(namespace=namespace)
        return ResponseUtil.success(data=service_accounts, msg="获取服务账户列表成功")
    except Exception as e:
        logger.error(f"获取服务账户列表失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取服务账户列表失败：{str(e)}")


@security_router.delete("/serviceaccounts/{name}", response_model=BaseResponse, summary="删除服务账户")
async def delete_service_account(name: str, namespace: str = "default"):
    """:return: 删除指定的服务账户"""
    try:
        result = SaService.delete_service_account(name=name, namespace=namespace)
        return ResponseUtil.success(data=result, msg="删除服务账户成功")
    except Exception as e:
        logger.error(f"删除服务账户失败：{e}")
        raise HTTPException(status_code=500, detail=f"删除服务账户失败：{str(e)}")


# ==================== Role 相关接口 ====================
@security_router.get("/roles", response_model=BaseResponse, summary="获取角色列表")
async def get_roles(namespace: str = "default"):
    """:return: 获取指定命名空间下的角色列表"""
    try:
        roles = RoleService.get_roles(namespace=namespace)
        return ResponseUtil.success(data=roles, msg="获取角色列表成功")
    except Exception as e:
        logger.error(f"获取角色列表失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取角色列表失败：{str(e)}")


@security_router.delete("/roles/{name}", response_model=BaseResponse, summary="删除角色")
async def delete_role(name: str, namespace: str = "default"):
    """:return: 删除指定的角色"""
    try:
        result = RoleService.delete_role(name=name, namespace=namespace)
        return ResponseUtil.success(data=result, msg="删除角色成功")
    except Exception as e:
        logger.error(f"删除角色失败：{e}")
        raise HTTPException(status_code=500, detail=f"删除角色失败：{str(e)}")


# ==================== ClusterRole 相关接口 ====================
@security_router.get("/clusterroles", response_model=BaseResponse, summary="获取集群角色列表")
async def get_cluster_roles():
    """:return: 获取所有集群角色列表"""
    try:
        cluster_roles = ClusterRoleService.get_cluster_roles()
        return ResponseUtil.success(data=cluster_roles, msg="获取集群角色列表成功")
    except Exception as e:
        logger.error(f"获取集群角色列表失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取集群角色列表失败：{str(e)}")


@security_router.delete("/clusterroles/{name}", response_model=BaseResponse, summary="删除集群角色")
async def delete_cluster_role(name: str):
    """:return: 删除指定的集群角色"""
    try:
        result = ClusterRoleService.delete_cluster_role(name=name)
        return ResponseUtil.success(data=result, msg="删除集群角色成功")
    except Exception as e:
        logger.error(f"删除集群角色失败：{e}")
        raise HTTPException(status_code=500, detail=f"删除集群角色失败：{str(e)}")


# ==================== RoleBinding 相关接口 ====================
@security_router.get("/rolebindings", response_model=BaseResponse, summary="获取角色绑定列表")
async def get_role_bindings(namespace: str = "default"):
    """:return: 获取指定命名空间下的角色绑定列表"""
    try:
        role_bindings = RoleBindingService.get_role_bindings(namespace=namespace)
        return ResponseUtil.success(data=role_bindings, msg="获取角色绑定列表成功")
    except Exception as e:
        logger.error(f"获取角色绑定列表失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取角色绑定列表失败：{str(e)}")


@security_router.delete("/rolebindings/{name}", response_model=BaseResponse, summary="删除角色绑定")
async def delete_role_binding(name: str, namespace: str = "default"):
    """:return: 删除指定的角色绑定"""
    try:
        result = RoleBindingService.delete_role_binding(name=name, namespace=namespace)
        return ResponseUtil.success(data=result, msg="删除角色绑定成功")
    except Exception as e:
        logger.error(f"删除角色绑定失败：{e}")
        raise HTTPException(status_code=500, detail=f"删除角色绑定失败：{str(e)}")


# ==================== ClusterRoleBinding 相关接口 ====================
@security_router.get("/clusterrolebindings", response_model=BaseResponse, summary="获取集群角色绑定列表")
async def get_cluster_role_bindings():
    """:return: 获取所有集群角色绑定列表"""
    try:
        cluster_role_bindings = ClusterRoleBindingService.get_cluster_role_bindings()
        return ResponseUtil.success(data=cluster_role_bindings, msg="获取集群角色绑定列表成功")
    except Exception as e:
        logger.error(f"获取集群角色绑定列表失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取集群角色绑定列表失败：{str(e)}")


@security_router.delete("/clusterrolebindings/{name}", response_model=BaseResponse, summary="删除集群角色绑定")
async def delete_cluster_role_binding(name: str):
    """:return: 删除指定的集群角色绑定"""
    try:
        result = ClusterRoleBindingService.delete_cluster_role_binding(name=name)
        return ResponseUtil.success(data=result, msg="删除集群角色绑定成功")
    except Exception as e:
        logger.error(f"删除集群角色绑定失败：{e}")
        raise HTTPException(status_code=500, detail=f"删除集群角色绑定失败：{str(e)}")
