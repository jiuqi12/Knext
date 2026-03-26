# 全局统一异常处理机制
from app.main import app
from fastapi import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.response import BaseResponse
from tortoise.exceptions import DoesNotExist


# 捕获抛出的HTTPException异常
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(exc: StarletteHTTPException):
    return BaseResponse(code=exc.status_code, message=exc.detail, data=None)


# 捕获数据库的不存在异常
@app.exception_handler(DoesNotExist)
async def not_exist_exception_handler(exc: DoesNotExist):
    return BaseResponse(code=status.HTTP_404_NOT_FOUND, message="未获取到资源", data=exc)


# 捕获全局未处理的异常
@app.exception_handler(Exception)
async def global_exception_handler(exc: Exception):
    return BaseResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, messag="服务器内部错误", data=exc)
