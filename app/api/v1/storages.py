from fastapi import APIRouter, Query, Depends
from app.services.storages.pv_service import PersistentVolumeService
from app.services.storages.pvc_service import PersistentVolumeClaimService
from app.services.storages.storageclass_service import StorageClassService
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.api.deps import get_current_user

storage_router = APIRouter(dependencies=[Depends(get_current_user)])


# pv模块
@storage_router.get("/pvs", response_model=BaseResponse, summary="列出存储卷列表")
async def list_storages():
    """
    列出pv列表
    - **return**: pv列表
    """
    pvs = PersistentVolumeService.list_persistent_volumes()
    return ResponseUtil.success(data=pvs, msg="获取PV成功")


@storage_router.get("/pvs/{pv_name}", response_model=BaseResponse, summary="获取指定存储卷")
async def get_storage(pv_name: str):
    """
    获取指定pv
    - **pv_name**: 存储卷名称
    - **return**: pv的详细信息
    """
    pv = PersistentVolumeService.get_persistent_volume(pv_name)
    return ResponseUtil.success(data=pv, msg="获取PV成功")


@storage_router.delete("/pvs/{pv_name}", response_model=BaseResponse, summary="删除指定存储卷")
async def get_storage(pv_name: str):
    """
    删除指定pv
    - **pv_name**: 存储卷名称
    - **return**: data
    """
    data = PersistentVolumeService.delete_persistent_volume(pv_name)
    return ResponseUtil.success(data=data, msg="获取PV成功")


# pvc模块
@storage_router.get("/pvcs", response_model=BaseResponse, summary="列出存储卷声明列表")
async def list_pvcs(namespace: str = Query(None, description="名称空间")):
    """
    列出pvc
    - **namespace**: 命名空间（可选）
    - **return**: 指定pv的详细信息
    """
    pvcs = PersistentVolumeClaimService.list_persistent_volume_claims(namespace)
    return ResponseUtil.success(data=pvcs, msg="获取PVC成功")


@storage_router.get("/pvcs/{pvc_name}", response_model=BaseResponse, summary="获取指定存储卷声明")
async def get_pvc(pvc_name: str, namespace: str = Query(None, description="名称空间")):
    """
    获取指定pvc
    - **pvc_name**: 存储卷声明名称
    - **namespace**: 命名空间（可选）
    - **return**: 存储卷声明的详细信息
    """
    pvc = PersistentVolumeClaimService.get_persistent_volume_claim(pvc_name, namespace)
    return ResponseUtil.success(data=pvc, msg="获取PVC成功")


@storage_router.delete("/pvcs/{pvc_name}", response_model=BaseResponse, summary="删除指定存储卷声明")
async def delete_pvc(pvc_name: str, namespace: str = Query(None, description="名称空间")):
    """
    删除指定pvc
    - **pvc_name**: 存储卷声明名称
    - **namespace**: 命名空间（可选）
    - **return**: data
    """
    data = PersistentVolumeClaimService.delete_persistent_volume_claim()
    return ResponseUtil.success(data=data, msg="获取PVC成功")


# storageclass模块
@storage_router.get("/storageclasses", response_model=BaseResponse, summary="列出存储类列表")
async def list_storageclasses():
    """
    列出存储类列表
    - **return**: storageclass列表
    """
    storage_class = StorageClassService.list_storages()
    return ResponseUtil.success(data=storage_class, msg="获取storageclass成功")


@storage_router.get("/storageclasses/{storage_class_name}", response_model=BaseResponse, summary="获取指定存储类")
async def get_storageclass(storage_class_name: str):
    """
    获取指定存储类
    - **storage_class_name**: 存储类名称
    - **return**: 存储类的详细信息
    """
    storage_class = StorageClassService.get_storage(storage_class_name)
    return ResponseUtil.success(data=storage_class, msg="获取storageclass成功")


@storage_router.delete("/storageclasses/{storage_class_name}", response_model=BaseResponse, summary="删除指定存储类")
async def delete_storageclass(storage_class_name: str):
    """
    删除指定存储类
    - **storage_class_name**: 存储类名称
    - **return**: data
    """
    data = StorageClassService.delete_storage(storage_class_name)
    return ResponseUtil.success(data=data, msg="删除storageclass成功")
