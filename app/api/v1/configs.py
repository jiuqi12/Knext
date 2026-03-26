from fastapi import APIRouter, HTTPException, Query
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.utils.logger import logger
from app.services.configs.configmap_service import ConfigMapService
from app.services.configs.secret_service import SecretService

config_router = APIRouter()


# configmap相关接口
@config_router.get("/configmaps", summary="获取configmaps列表")
async def list_configmaps(namespace: str = Query(None, description="名称空间")):
    """
    获取ConfigMap列表
    - **namespace**: 命名空间（可选）
    """
    try:
        configmaps = ConfigMapService.list_configmaps(namespace)
        return ResponseUtil.success(data=configmaps, msg="获取configmaps成功")
    except ValueError as e:
        logger.error(f"获取configmaps失败：{e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取configmaps失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取configmaps失败：{str(e)}")


# secret相关接口
@config_router.get("/secrets", summary="获取secrets列表")
async def get_secrets(namespace: str = Query(None, description="名称空间")):
    """
    列获取Secret列表
    :param namespace: 命名空间（可选）
    """
    try:
        secrets = SecretService.list_secrets(namespace)
        return ResponseUtil.success(data=secrets, msg="获取secrets成功")
    except ValueError as e:
        logger.error(f"获取secrets失败：{e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error()


