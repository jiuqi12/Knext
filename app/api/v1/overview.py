from fastapi import APIRouter, HTTPException, Body
from app.services.overview_service import OverviewService
from app.utils.logger import logger
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil

overview_router = APIRouter()


# 获取 overview 统计信息
@overview_router.get("/", response_model=BaseResponse, summary="获取集群概览")
async def get_overview():
    """获取集群概览信息，包括节点、Pod、Deployment 等的统计"""
    try:
        overview = OverviewService.get_overview()
        return ResponseUtil.success(data=overview, msg="获取概览成功")
    except Exception as e:
        logger.error(f"获取集群概览失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取集群概览失败：{str(e)}")

