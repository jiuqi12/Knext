from kubernetes import client
from app.core.K8sClientManager import k8s_client_manager
from fastapi import Depends
from app.api.deps import get_current_user


class K8sClientWrapper:
    """
    K8s Client 包装类 - 为每个请求动态获取用户专属的 client
    """
    def __init__(self, user: dict = None):
        self.user = user
        self._api_client = None
        self._core_v1 = None
        self._apps_v1 = None
        self._batch_v1 = None
        self._networking_v1 = None
        self._custom_objects = None
        self._storage_v1 = None
        self._rbac_v1 = None
    
    async def _ensure_client(self):
        """确保 client 已初始化"""
        if self._api_client is None and self.user:
            self._api_client = await k8s_client_manager.get_client(self.user)
    
    async def get_api_client(self) -> client.ApiClient:
        """获取 API 客户端"""
        await self._ensure_client()
        return self._api_client

    async def get_websocket_client(self):
        return self._api_client

    async def get_core_v1_api(self) -> client.CoreV1Api:
        """获取 CoreV1Api 客户端"""
        await self._ensure_client()
        if self._core_v1 is None:
            self._core_v1 = client.CoreV1Api(api_client=self._api_client)
        return self._core_v1

    async def get_apps_v1_api(self) -> client.AppsV1Api:
        """获取 AppsV1Api 客户端"""
        await self._ensure_client()
        if self._apps_v1 is None:
            self._apps_v1 = client.AppsV1Api(api_client=self._api_client)
        return self._apps_v1

    async def get_batch_v1_api(self) -> client.BatchV1Api:
        """获取 BatchV1Api 客户端"""
        await self._ensure_client()
        if self._batch_v1 is None:
            self._batch_v1 = client.BatchV1Api(api_client=self._api_client)
        return self._batch_v1

    async def get_networking_v1_api(self) -> client.NetworkingV1Api:
        """获取 NetworkingV1Api 客户端"""
        await self._ensure_client()
        if self._networking_v1 is None:
            self._networking_v1 = client.NetworkingV1Api(api_client=self._api_client)
        return self._networking_v1

    async def get_custom_objects_api(self) -> client.CustomObjectsApi:
        """获取 CustomObjectsApi 客户端"""
        await self._ensure_client()
        if self._custom_objects is None:
            self._custom_objects = client.CustomObjectsApi(api_client=self._api_client)
        return self._custom_objects

    async def get_storage_v1_api(self) -> client.StorageV1Api:
        """获取 StorageV1Api 客户端"""
        await self._ensure_client()
        if self._storage_v1 is None:
            self._storage_v1 = client.StorageV1Api(api_client=self._api_client)
        return self._storage_v1

    async def get_rbac_v1_api(self) -> client.RbacAuthorizationV1Api:
        """获取 RbacAuthorizationV1Api 客户端"""
        await self._ensure_client()
        if self._rbac_v1 is None:
            self._rbac_v1 = client.RbacAuthorizationV1Api(api_client=self._api_client)
        return self._rbac_v1


async def get_k8s_client_wrapper(user: dict = Depends(get_current_user)) -> K8sClientWrapper:
    """
    FastAPI 依赖注入函数（REST 路由专用）
    自动为每个请求创建用户专属的 K8s client wrapper
    通过 Depends(get_current_user) 从请求头 Authorization 中获取 token 并验证身份
    """
    user_data = {
        "user_id": user["id"],
        "username": user["username"],
        "role_id": user["role_id"],
    }
    return K8sClientWrapper(user=user_data)


async def get_ws_k8s_wrapper(user_info: dict) -> K8sClientWrapper:
    """
    WebSocket 专用的 K8s 客户端依赖函数

    认证已在 websocket.py 路由层通过消息认证完成，
    此处只负责根据已认证的用户信息创建 K8sClientWrapper。

    Args:
        user_info: 已认证的用户信息字典，包含 id, username, role_id 等
    """
    user_data = {
        "user_id": user_info["id"],
        "username": user_info["username"],
        "role_id": user_info["role_id"],
    }
    return K8sClientWrapper(user=user_data)
