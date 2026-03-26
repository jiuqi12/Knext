from fastapi import APIRouter, HTTPException
from app.services.nodes_service import NodesService
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.utils.logger import logger

nodes_router = APIRouter()


@nodes_router.get("/", response_model=BaseResponse, summary="获取节点信息")
async def get_nodes():
    """:return: 获取节点的信息"""
    try:
        overview = NodesService.get_nodes()
        return ResponseUtil.success(data=overview, msg="获取节点信息成功")
    except Exception as e:
        logger.error(f"获取节点信息失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取节点信息失败：{str(e)}")


@nodes_router.get("/{node_name}", response_model=BaseResponse, summary="获取指定节点信息")
async def get_node(node_name: str):
    """:return: 获取指定节点的信息"""
    try:
        node = NodesService.get_node(node_name)
        return ResponseUtil.success(data=node, msg="获取节点信息成功")
    except Exception as e:
        logger.error(f"获取节点信息失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取节点信息失败：{str(e)}")
