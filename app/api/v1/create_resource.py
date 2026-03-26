from fastapi import APIRouter, HTTPException, Request
from app.utils.logger import logger
from app.utils.response import BaseResponse
from app.utils.response_util import ResponseUtil
from app.services.resource_service import ResourceService
import yaml

create_resource_router = APIRouter()


# 通过yaml创建资源
@create_resource_router.post("/", response_model=BaseResponse, summary="通过yaml创建资源")
async def create_resource_from_yaml(request: Request):
    """通过yaml创建资源"""
    body = await request.body()
    yaml_content = body.decode("utf-8")
    try:
        # 解析yaml
        docs = yaml.safe_load_all(yaml_content)
        results = []
        for doc in docs:
            result = ResourceService.create_resource_yaml(doc)
            results.append(result)
        return ResponseUtil.success(data=results, msg="创建资源成功")
    except yaml.YAMLError as e:
        logger.error(f"解析yaml失败：{e}")
        raise HTTPException(status_code=400, detail=f"解析yaml失败：{str(e)}")
    except Exception as e:
        logger.error(f"创建资源失败：{e}")
        raise HTTPException(status_code=500, detail=f"创建资源失败：{str(e)}")