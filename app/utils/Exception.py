# 全局统一异常处理机制
# 采用函数注册方式，避免与 main.py 产生循环导入

import traceback
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from kubernetes.client.exceptions import ApiException
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.response import BaseResponse
from app.utils.exceptions import BizException
from app.utils.logger import get_logger
from tortoise.exceptions import DoesNotExist, IntegrityError

# 获取异常处理专用日志记录器
logger = get_logger("exception")


def _get_request_id(request: Request) -> str:
    """从 request.state 中获取请求 ID，如果不存在则返回 unknown"""
    return getattr(request.state, "request_id", "unknown")


def _build_response(request: Request, code: int, message: str) -> JSONResponse:
    """构建统一的错误响应，附带请求 ID，返回 JSONResponse 确保前端能正确解析"""
    request_id = _get_request_id(request)
    body = BaseResponse(code=code, msg=message, data=None, request_id=request_id).model_dump()
    return JSONResponse(content=body, status_code=200)


def register_exception_handlers(app: FastAPI):
    """
    注册所有全局异常处理器
    在 main.py 中调用此函数完成注册
    """

    # 捕获业务异常（BizException）
    # 业务逻辑中主动抛出的预期错误，使用 warning 级别记录
    @app.exception_handler(BizException)
    async def biz_exception_handler(request: Request, exc: BizException):
        request_id = _get_request_id(request)
        logger.warning(
            f"[{request_id}] 业务异常: {request.method} {request.url.path} "
            f"-> {exc.code}: {exc.message}"
        )
        return _build_response(request, exc.code, exc.message)

    # 捕获参数校验异常（RequestValidationError）
    # FastAPI/Pydantic 参数校验失败时触发，默认 422 转为 400 返回给前端
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        request_id = _get_request_id(request)
        # 提取前 5 条校验错误信息，拼接为可读字符串
        errors = exc.errors()
        details = "; ".join(
            [f"{e.get('loc', ['unknown'])[-1]}: {e.get('msg', '未知错误')}" for e in errors[:5]]
        )
        message = f"参数校验失败: {details}"
        logger.warning(
            f"[{request_id}] 参数校验失败: {request.method} {request.url.path} -> {message}"
        )
        return _build_response(request, status.HTTP_400_BAD_REQUEST, message)

    # 捕获 Kubernetes API 异常（ApiException）
    # K8s API 调用失败时触发，直接使用 K8s 返回的状态码和原因
    @app.exception_handler(ApiException)
    async def kubernetes_api_exception_handler(request: Request, exc: ApiException):
        request_id = _get_request_id(request)
        logger.error(
            f"[{request_id}] K8s API 异常: {request.method} {request.url.path} "
            f"-> {exc.status} {exc.reason}"
        )
        return _build_response(request, exc.status, f"K8s API 错误: {exc.reason}")

    # 捕获 HTTP 异常（StarletteHTTPException）
    # 框架自身抛出的 HTTP 异常，如 404 路由不存在、405 方法不允许等
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        request_id = _get_request_id(request)
        # 5xx 使用 error 级别，4xx 使用 warning 级别
        level = "error" if exc.status_code >= 500 else "warning"
        log_msg = (
            f"[{request_id}] HTTP 异常: {request.method} {request.url.path} "
            f"-> {exc.status_code}: {exc.detail}"
        )
        if level == "error":
            logger.error(log_msg)
        else:
            logger.warning(log_msg)
        return _build_response(request, exc.status_code, exc.detail)

    # 捕获数据库资源不存在异常（DoesNotExist）
    # Tortoise ORM 查询未找到记录时触发
    @app.exception_handler(DoesNotExist)
    async def not_exist_exception_handler(request: Request, exc: DoesNotExist):
        request_id = _get_request_id(request)
        logger.warning(
            f"[{request_id}] 资源不存在: {request.method} {request.url.path} -> {exc}"
        )
        return _build_response(request, status.HTTP_404_NOT_FOUND, "资源不存在")

    # 捕获数据库完整性约束异常（IntegrityError）
    # 唯一约束冲突、外键约束违反等
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        request_id = _get_request_id(request)
        logger.warning(
            f"[{request_id}] 数据完整性异常: {request.method} {request.url.path} -> {exc}"
        )
        return _build_response(request, status.HTTP_409_CONFLICT, "数据冲突，请检查是否重复")

    # 兜底：捕获所有未处理的异常（Exception）
    # 生产环境不暴露异常细节，仅返回友好提示，完整堆栈记录到日志
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        request_id = _get_request_id(request)
        # 记录完整的异常堆栈到日志文件，便于排查
        logger.error(
            f"[{request_id}] 未捕获异常: {request.method} {request.url.path}\n"
            f"{traceback.format_exc()}"
        )
        return _build_response(request, status.HTTP_500_INTERNAL_SERVER_ERROR, "服务器内部错误，请联系管理员")