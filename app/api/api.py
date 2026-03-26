# 汇总api接口
from fastapi import APIRouter
from app.api.v1.configs import config_router
from app.api.v1.networks import network_router
from app.api.v1.securitys import security_router
from app.api.v1.storages import storage_router
from app.api.v1.users import user_router
from app.api.v1.websocket import ws_router
from app.api.v1.workloads import workload_router
from app.api.v1.namespace import namespace_router
from app.api.v1.nodes import nodes_router
from app.api.v1.overview import overview_router
from app.api.v1.create_resource import create_resource_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(overview_router, prefix="/overview", tags=["系统概览"])
v1_router.include_router(create_resource_router, prefix="/create_resource", tags=["创建资源"])
v1_router.include_router(namespace_router, prefix="/namespaces", tags=["命名空间"])
v1_router.include_router(nodes_router, prefix="/nodes", tags=["节点管理"])
v1_router.include_router(workload_router, prefix="/workloads", tags=["工作负载管理"])
v1_router.include_router(config_router, prefix="/configs", tags=["配置管理"])
v1_router.include_router(network_router, prefix="/networks", tags=["网络管理"])
v1_router.include_router(security_router, prefix="/securities", tags=["安全管理"])
v1_router.include_router(storage_router, prefix="/storages", tags=["存储管理"])
v1_router.include_router(user_router, prefix="/users", tags=["用户管理"])
v1_router.include_router(ws_router, prefix="/ws", tags=["websocket管理"])
