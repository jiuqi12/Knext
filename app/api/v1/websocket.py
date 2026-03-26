# 处理日志、终端流接口
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Path
from app.services.websocket.terminal_service import TerminalService
from app.services.websocket.log_service import PodLogService
from typing import Optional

ws_router = APIRouter()


# 实时日志流，url:ws://localhost:8000/api/v1/ws/pods/{namespace}/{pod_name}/logs
@ws_router.websocket("/pods/{namespace}/{pod_name}/logs")
async def pod_logs_websocket(
        websocket: WebSocket,
        namespace: str = Path(..., description="命名空间"),
        pod_name: str = Path(..., description="Pod 名称"),
        container: Optional[str] = None
):
    """
    Pod 日志 WebSocket 流式接口
    
    连接示例:
        ws://localhost:8000/api/v1/ws/pods/default/nginx-pod/logs
        ws://localhost:8000/api/v1/ws/pods/kube-system/coredns-abc/logs?container=coredns
    
    消息格式:
        - 连接成功：{"type": "connected", "message": "..."}
        - 日志数据：{"type": "log", "data": "2024-01-01T12:00:00Z log content"}
        - 信息提示：{"type": "info", "message": "..."}
        - 错误信息：{"type": "error", "message": "..."}
        - 结束：{"type": "end", "message": "..."}
    """
    try:
        await PodLogService.stream_logs(websocket, namespace, pod_name, container)
    except WebSocketDisconnect:
        print("客户端断开连接")
        pass  # 客户端断开连接是正常行为
    except Exception as e:
        # 其他异常会由 service 层处理
        pass


# web 终端，url:ws://localhost:8000/api/v1/ws/pods/{namespace}/{pod_name}/terminal
@ws_router.websocket("/pods/{namespace}/{pod_name}/terminal")
async def pod_terminal_websocket(
        websocket: WebSocket,
        namespace: str = Path(..., description="命名空间"),
        pod_name: str = Path(..., description="Pod 名称"),
        container: Optional[str] = None
):
    """
    Pod Web 终端 WebSocket 接口
    
    连接示例:
        ws://localhost:8000/api/v1/ws/pods/default/nginx-pod/terminal
        ws://localhost:8000/api/v1/ws/pods/kube-system/coredns-abc/terminal?container=coredns
    
    消息格式:
        - 连接成功：{"type": "connected", "message": "..."}
        - 发送命令：{"type": "input", "data": "ls -la"}
        - 接收输出：{"type": "output", "data": "..."}
        - 错误信息：{"type": "error", "data": "..."}
    """
    try:
        await TerminalService.connect_terminal(websocket, namespace, pod_name, container)
    except WebSocketDisconnect:
        pass  # 客户端断开连接是正常行为
    except Exception as e:
        # 其他异常会由 service 层处理
        pass
