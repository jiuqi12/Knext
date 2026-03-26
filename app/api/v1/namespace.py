from app.utils.logger import logger
from app.services.namespace_service import NamespaceService
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from fastapi import APIRouter, HTTPException

namespace_router = APIRouter()


@namespace_router.get("/", response_model=BaseResponse, summary="获取全部的命名空间")
async def get_namespaces():
    """获取全部命名空间"""
    try:
        namespaces = NamespaceService.get_namespaces()
        return ResponseUtil.success(data=namespaces, msg="获取命名空间成功")
    except Exception as e:
        logger.error(f"获取命名空间失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取命名空间失败：{str(e)}")


@namespace_router.post("/", response_model=BaseResponse, summary="创建命名空间")
async def create_namespace(namespace_name: str):
    """创建命名空间"""
    try:
        namespace = NamespaceService.create_namespace(namespace_name)
        return ResponseUtil.success(data=namespace, msg="创建命名空间成功")
    except Exception as e:
        logger.error(f"创建命名空间失败：{e}")
        raise HTTPException(status_code=500, detail=f"创建命名空间失败：{str(e)}")


@namespace_router.delete("/{namespace_name}", response_model=BaseResponse, summary="删除命名空间")
async def delete_namespace(namespace_name: str):
    """删除命名空间"""
    try:
        status = NamespaceService.delete_namespace(namespace_name)
        return ResponseUtil.success(data=status, msg="删除命名空间成功")
    except Exception as e:
        logger.error(f"删除命名空间失败：{e}")
        raise HTTPException(status_code=500, detail=f"删除命名空间失败：{str(e)}")