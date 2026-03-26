import asyncio
from fastapi import WebSocket
from app.core.k8s_client import get_core_v1_api
from app.utils.logger import logger
from typing import Optional

# 终端流逻辑处理
class TerminalService:
    """Pod 终端 WebSocket 服务"""

    @staticmethod
    async def connect_terminal(websocket: WebSocket, namespace: str, pod_name: str, container: Optional[str] = None):
        """
        连接 Pod 终端
        
        Args:
            websocket: WebSocket 连接对象
            namespace: 命名空间
            pod_name: Pod 名称
            container: 容器名称（可选）
        """
        try:
            from kubernetes.stream import stream
            from kubernetes.client.rest import ApiException
            
            v1 = get_core_v1_api()
            
            # 验证 Pod
            try:
                pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
                logger.info(f"Pod 验证成功：{pod_name}, 状态：{pod.status.phase}")
            except ApiException as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Pod 不存在：{e.reason}"
                })
                await websocket.close()
                return
            
            await websocket.accept()
            
            # 使用 exec 连接到 Pod
            resp = stream(
                v1.connect_get_namespaced_pod_exec,
                name=pod_name,
                namespace=namespace,
                container=container,
                command=["/bin/sh"],
                stderr=True,
                stdin=True,
                stdout=True,
                tty=True,
                _preload_content=False
            )
            
            await websocket.send_json({
                "type": "connected",
                "message": f"已连接到终端：{namespace}/{pod_name}"
            })
            
            # 处理双向数据流
            async def recv_from_pod():
                """从 Pod 接收数据"""
                while resp.is_open():
                    if resp.peek_stdout():
                        output = resp.read_stdout()
                        try:
                            await websocket.send_json({
                                "type": "output",
                                "data": output
                            })
                        except:
                            break
                    if resp.peek_stderr():
                        error = resp.read_stderr()
                        try:
                            await websocket.send_json({
                                "type": "error",
                                "data": error
                            })
                        except:
                            break
                    await asyncio.sleep(0.1)
            
            async def send_to_pod():
                """发送数据到 Pod"""
                try:
                    async for message in websocket.iter_json():
                        if message.get("type") == "input":
                            cmd = message.get("data", "")
                            resp.write_stdin(cmd + "\n")
                except:
                    pass
                finally:
                    resp.close()
            
            # 并发运行
            await asyncio.gather(recv_from_pod(), send_to_pod())
            
        except Exception as e:
            logger.error(f"终端连接失败：{e}", exc_info=True)
            try:
                if websocket.client_connected:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"终端连接失败：{str(e)}"
                    })
                    await websocket.close()
            except:
                pass