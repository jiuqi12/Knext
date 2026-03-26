from app.utils.response import BaseResponse
from typing import Any, TypeVar, Generic

T = TypeVar("T")


class ResponseUtil(Generic[T]):
    """封装统一响应工具类"""
    
    @staticmethod
    def success(data: Any = None, msg: str = "操作成功", code: int = 200) -> BaseResponse:
        """
        成功响应
        
        :param data: 返回数据
        :param msg: 提示信息
        :param code: 状态码
        :return: BaseResponse
        """
        return BaseResponse(code=code, msg=msg, data=data)
    
    @staticmethod
    def error(msg: str = "操作失败", code: int = 500, data: Any = None) -> BaseResponse:
        """
        错误响应
        
        :param msg: 错误信息
        :param code: 状态码
        :param data: 返回数据（可选）
        :return: BaseResponse
        """
        return BaseResponse(code=code, msg=msg, data=data)
    
    @staticmethod
    def bad_request(msg: str = "请求参数错误", data: Any = None) -> BaseResponse:
        """
        400 错误响应
        
        :param msg: 错误信息
        :param data: 返回数据
        :return: BaseResponse
        """
        return BaseResponse(code=400, msg=msg, data=data)
    
    @staticmethod
    def unauthorized(msg: str = "未授权，请先登录", data: Any = None) -> BaseResponse:
        """
        401 错误响应
        
        :param msg: 错误信息
        :param data: 返回数据
        :return: BaseResponse
        """
        return BaseResponse(code=401, msg=msg, data=data)
    
    @staticmethod
    def forbidden(msg: str = "权限不足", data: Any = None) -> BaseResponse:
        """
        403 错误响应
        
        :param msg: 错误信息
        :param data: 返回数据
        :return: BaseResponse
        """
        return BaseResponse(code=403, msg=msg, data=data)
    
    @staticmethod
    def not_found(msg: str = "资源不存在", data: Any = None) -> BaseResponse:
        """
        404 错误响应
        
        :param msg: 错误信息
        :param data: 返回数据
        :return: BaseResponse
        """
        return BaseResponse(code=404, msg=msg, data=data)
    
    @staticmethod
    def internal_error(msg: str = "服务器内部错误", data: Any = None) -> BaseResponse:
        """
        500 错误响应
        
        :param msg: 错误信息
        :param data: 返回数据
        :return: BaseResponse
        """
        return BaseResponse(code=500, msg=msg, data=data)
    
    @staticmethod
    def list_response(items: list, total: int, page: int = 1, limit: int = 10, msg: str = "获取成功") -> BaseResponse:
        """
        列表响应（带分页信息）
        
        :param items: 数据列表
        :param total: 总数
        :param page: 当前页码
        :param limit: 每页数量
        :param msg: 提示信息
        :return: BaseResponse
        """
        data = {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit
        }
        return BaseResponse(code=200, msg=msg, data=data)


# 便捷函数
def success(data: Any = None, msg: str = "操作成功", code: int = 200) -> BaseResponse:
    """成功响应"""
    return ResponseUtil.success(data, msg, code)


def error(msg: str = "操作失败", code: int = 500, data: Any = None) -> BaseResponse:
    """错误响应"""
    return ResponseUtil.error(msg, code, data)


def bad_request(msg: str = "请求参数错误", data: Any = None) -> BaseResponse:
    """400 错误响应"""
    return ResponseUtil.bad_request(msg, data)


def unauthorized(msg: str = "未授权，请先登录", data: Any = None) -> BaseResponse:
    """401 错误响应"""
    return ResponseUtil.unauthorized(msg, data)


def forbidden(msg: str = "权限不足", data: Any = None) -> BaseResponse:
    """403 错误响应"""
    return ResponseUtil.forbidden(msg, data)


def not_found(msg: str = "资源不存在", data: Any = None) -> BaseResponse:
    """404 错误响应"""
    return ResponseUtil.not_found(msg, data)


def internal_error(msg: str = "服务器内部错误", data: Any = None) -> BaseResponse:
    """500 错误响应"""
    return ResponseUtil.internal_error(msg, data)


def list_response(items: list, total: int, page: int = 1, limit: int = 10, msg: str = "获取成功") -> BaseResponse:
    """列表响应"""
    return ResponseUtil.list_response(items, total, page, limit, msg)
