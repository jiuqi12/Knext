# 请求 ID 中间件
# 为每个请求生成唯一标识，用于日志追踪和问题排查
# 使用原生 ASGI 实现，避免 BaseHTTPMiddleware 导致的请求卡死问题

import uuid
from starlette.types import ASGIApp, Receive, Scope, Send


class RequestIDMiddleware:
    """
    请求 ID 中间件（原生 ASGI 实现）
    - 优先从请求头 X-Request-ID 中获取（支持上游网关传递）
    - 如果未提供，则自动生成一个 8 位短 ID
    - 将 request_id 存入 scope["state"]，供后续使用
    - 在响应头中返回 X-Request-ID，方便前端关联请求
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # 仅处理 HTTP 和 WebSocket 请求
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        # 从请求头中提取 X-Request-ID，或自动生成
        headers = dict(scope.get("headers", []))
        request_id = headers.get(b"x-request-id")
        if request_id:
            request_id = request_id.decode("utf-8")
        else:
            request_id = str(uuid.uuid4())[:8]

        # 将 request_id 存入 scope，供异常处理器等下游使用
        # Starlette 的 request.state 从 scope["state"] 中读取
        scope.setdefault("state", {})
        scope["state"]["request_id"] = request_id

        # 包装 send 函数，在响应头中注入 X-Request-ID
        async def send_with_request_id(message):
            if message["type"] == "http.response.start":
                # 复制响应头并添加 X-Request-ID
                response_headers = list(message.get("headers", []))
                response_headers.append((b"x-request-id", request_id.encode("utf-8")))
                message["headers"] = response_headers
            await send(message)

        await self.app(scope, receive, send_with_request_id)