# 自定义业务异常体系
# 用于替代 HTTPException，将业务逻辑与 HTTP 协议解耦


class BizException(Exception):
    """
    业务异常基类
    所有业务相关的异常都应继承此类，通过 code 区分 HTTP 状态码，message 提供错误描述
    """

    def __init__(self, code: int = 400, message: str = "业务错误", data=None):
        self.code = code          # HTTP 状态码
        self.message = message    # 错误描述信息
        self.data = data          # 附加数据（可选）
        super().__init__(self.message)


class NotFoundException(BizException):
    """资源不存在异常（404）"""

    def __init__(self, message: str = "资源不存在"):
        super().__init__(code=404, message=message)


class AuthException(BizException):
    """认证失败异常（401）—— Token 无效、过期、用户不存在等"""

    def __init__(self, message: str = "认证失败"):
        super().__init__(code=401, message=message)


class ForbiddenException(BizException):
    """权限不足异常（403）—— 用户被禁用、无权访问等"""

    def __init__(self, message: str = "权限不足"):
        super().__init__(code=403, message=message)


class ValidationException(BizException):
    """参数校验异常（400）—— 请求参数不合法、格式错误等"""

    def __init__(self, message: str = "参数校验失败"):
        super().__init__(code=400, message=message)


class K8sException(BizException):
    """Kubernetes 相关异常（500）—— K8s API 调用失败、客户端创建超时等"""

    def __init__(self, message: str = "K8s 操作失败"):
        super().__init__(code=500, message=message)