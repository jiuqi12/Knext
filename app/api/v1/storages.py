from fastapi import APIRouter, Query, HTTPException
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.utils.logger import logger
from app.services.storages.pv_service import PersistentVolumeService
from app.services.storages.pvc_service import PersistentVolumeClaimService
from app.services.storages.storageclass_service import StorageClassService

storage_router = APIRouter()


# 存储模块
# pv模块
@storage_router.get("/pvs", response_model=BaseResponse, summary="列出存储卷列表")
async def list_storages(namespace: str = Query(None, description="名称空间")):
    """
    列出存储卷列表
    :param namespace: 命名空间（可选）
    :return:
    """
    try:
        pvs = PersistentVolumeService.list_persistent_volumes(namespace)
        return ResponseUtil.success(data=pvs, msg="获取PV成功")
    except ValueError as e:
        logger.error(f"列出PV失败：{e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取PV失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取PV失败：{str(e)}")


# pvc模块
@storage_router.get("/pvcs", response_model=BaseResponse, summary="列出存储卷声明列表")
async def list_pvcs(namespace: str = Query(None, description="名称空间")):
    """
    列出存储卷声明列表
    :param namespace: 命名空间（可选）
    :return:
    """
    try:
        pvcs = PersistentVolumeClaimService.list_persistent_volume_claims(namespace)
        return ResponseUtil.success(data=pvcs, msg="获取PVC成功")
    except ValueError as e:
        logger.error(f"列出PVC失败：{e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取PVC失败：{e}")
        raise HTTPException(status_code=500, detail=f"获取PVC失败：{str(e)}")


# storageclass模块
# 列出存储类
@storage_router.get("/storageclasses", response_model=BaseResponse, summary=["列出存储类列表"])
async def list_storageclasses():
    """
    列出存储类列表
    :return:
    """
    try:
        storage_class = StorageClassService.list_storages()
        return ResponseUtil.success(data=storage_class, msg="获取storageclass成功")
    except ValueError as e:
        logger.error(f"列出storageclass失败：{e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取storageclass失败：{e}")
