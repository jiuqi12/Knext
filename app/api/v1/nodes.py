from fastapi import APIRouter, Depends
from app.services.nodes_service import NodesService
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.api.deps import get_current_user
from app.core.k8s_client import get_k8s_client_wrapper, K8sClientWrapper

nodes_router = APIRouter(dependencies=[Depends(get_current_user)])


@nodes_router.get("", response_model=BaseResponse, summary="获取节点信息")
async def get_nodes(k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)):
    """
    获取节点信息
    - **return**: 获取节点的信息
    """
    overview = await NodesService.get_nodes(k8s_wrapper)
    return ResponseUtil.success(data=overview, msg="获取节点信息成功")


@nodes_router.get("/{node_name}", response_model=BaseResponse, summary="获取指定节点信息")
async def get_node(
    node_name: str,
    k8s_wrapper: K8sClientWrapper = Depends(get_k8s_client_wrapper)
):
    """
    获取指定节点信息
    - **node_name**：节点名称
    - **return**: 获取指定节点的信息
    """
    node = await NodesService.get_node(node_name, k8s_wrapper)
    return ResponseUtil.success(data=node, msg="获取节点信息成功")
