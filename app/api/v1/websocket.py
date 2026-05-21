from fastapi import APIRouter, WebSocketDisconnect, Path, WebSocket
from app.services.websocket.terminal_service import TerminalService
from app.services.websocket.log_service import PodLogService
from app.core.k8s_client import get_ws_k8s_wrapper
from app.api.deps import verify_websocket_token
from app.utils.logger import logger
from typing import Optional

ws_router = APIRouter()


@ws_router.websocket("/pods/{namespace}/{pod_name}/logs")
async def pod_logs_websocket(
        websocket: WebSocket,
        namespace: str = Path(..., description="命名空间"),
        pod_name: str = Path(..., description="Pod 名称"),
        container: Optional[str] = None,
):
    """
    Pod 日志 WebSocket 流式接口

    认证流程：
    1. 连接建立后，发送 {"type":"auth","token":"<jwt>"}
    2. 等待 {"type":"auth_ok"} 或 {"type":"auth_fail","message":"..."}
    3. 认证通过后使用标准消息协议通信
    """
    try:
        user_info = await verify_websocket_token(websocket)
        k8s_wrapper = await get_ws_k8s_wrapper(user_info)
        await PodLogService.stream_logs(websocket, namespace, pod_name, container, k8s_wrapper)
    except WebSocketDisconnect:
        logger.info("日志 WebSocket 客户端断开连接")


@ws_router.websocket("/pods/{namespace}/{pod_name}/terminal")
async def pod_terminal_websocket(
        websocket: WebSocket,
        namespace: str = Path(..., description="命名空间"),
        pod_name: str = Path(..., description="Pod 名称"),
        container: Optional[str] = None,
):
    """
    Pod Web 终端 WebSocket 接口

    认证流程：
    1. 连接建立后，发送 {"type":"auth","token":"<jwt>"}
    2. 等待 {"type":"auth_ok"} 或 {"type":"auth_fail","message":"..."}
    3. 认证通过后使用标准消息协议通信
    """
    try:
        user_info = await verify_websocket_token(websocket)
        k8s_wrapper = await get_ws_k8s_wrapper(user_info)
        await TerminalService.connect_terminal(websocket, namespace, pod_name, container, k8s_wrapper)
    except WebSocketDisconnect:
        logger.info("终端 WebSocket 客户端断开连接")
