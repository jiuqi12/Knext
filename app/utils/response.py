# 统一响应结构

from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    code: int = 200  # 状态码
    msg: str = "success"  # 信息
    data: Optional[T] = None  # 数据
    request_id: Optional[str] = None  # 请求 ID，用于链路追踪

# 200: 成功
#
# 400: 参数错误 (Bad Request)
#
# 401: 未登录或 Token 过期 (Unauthorized)
#
# 403: 权限不足 (Forbidden)
#
# 404: 资源不存在 (Not Found)
#
# 500: K8s API 调用失败或后端内部错误
