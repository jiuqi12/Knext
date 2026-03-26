from fastapi import APIRouter, Query, HTTPException
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.utils.logger import logger
from app.services.networks.service_service import ServiceService


network_router = APIRouter()


# 获取service服务列表
@network_router.get("/services", response_model=BaseResponse, summary="列出Service列表")
async def list_services(namespace: str = Query(None, description="名称空间")):
    """
    列出Service列表
    :param namespace: 命名空间（可选）
    """
    try:
        networks = ServiceService.list_services(namespace)
        return ResponseUtil.success(data=networks, msg="获取网络成功")
    except ValueError as e:
        logger.error(f"列出网络失败：{e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取网络失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取网络失败：{str(e)}")