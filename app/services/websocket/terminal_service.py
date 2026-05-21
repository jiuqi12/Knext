import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from app.core.k8s_client import K8sClientWrapper
from app.utils.logger import logger
from typing import Optional


# 终端流逻辑处理
class TerminalService:
    """Pod 终端 WebSocket 服务"""

    @staticmethod
    async def connect_terminal(websocket: WebSocket, namespace: str, pod_name: str, container: Optional[str] = None, k8s_wrapper: K8sClientWrapper = None):
        """
        连接 Pod 终端

        Args:
            websocket: WebSocket 连接对象
            namespace: 命名空间
            pod_name: Pod 名称
            container: 容器名称（可选）
            k8s_wrapper: K8s client wrapper
        """
        resp = None
        try:
            from kubernetes.stream import stream
            from kubernetes.client.rest import ApiException

            if k8s_wrapper is None:
                logger.error("终端连接失败：未传入 K8s 客户端包装器")
                await websocket.send_json({
                    "type": "error",
                    "message": "认证失败：未提供有效的 K8s 客户端"
                })
                await websocket.close()
                return

            v1 = await k8s_wrapper.get_core_v1_api()

            # 验证 Pod
            try:
                pod = await asyncio.to_thread(v1.read_namespaced_pod, name=pod_name, namespace=namespace)
                logger.info(f"Pod 验证成功：{pod_name}, 状态：{pod.status.phase}")
            except ApiException as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Pod 不存在：{e.reason}"
                })
                await websocket.close()
                return

            # 使用 exec 连接到 Pod（线程池中执行，避免阻塞事件循环）
            resp = await asyncio.to_thread(
                stream,
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
                """从 Pod 接收数据（所有 K8s 操作在线程池中执行）"""
                try:
                    while await asyncio.to_thread(resp.is_open):
                        if await asyncio.to_thread(resp.peek_stdout):
                            output = await asyncio.to_thread(resp.read_stdout)
                            if websocket.client_state == WebSocketState.CONNECTED:
                                await websocket.send_json({
                                    "type": "stdout",
                                    "data": output
                                })
                        if await asyncio.to_thread(resp.peek_stderr):
                            error = await asyncio.to_thread(resp.read_stderr)
                            if websocket.client_state == WebSocketState.CONNECTED:
                                await websocket.send_json({
                                    "type": "error",
                                    "message": error
                                })
                        await asyncio.sleep(0.05)
                except WebSocketDisconnect:
                    logger.info("终端 WebSocket 客户端断开（recv）")
                except Exception as e:
                    logger.error(f"终端接收数据异常：{e}")

            async def send_to_pod():
                """发送数据到 Pod"""
                try:
                    async for message in websocket.iter_json():
                        msg_type = message.get("type")
                        if msg_type == "stdin":
                            cmd = message.get("data", "")
                            await asyncio.to_thread(resp.write_stdin, cmd)
                        elif msg_type == "resize":
                            cols = message.get("cols", 80)
                            rows = message.get("rows", 24)
                            logger.debug(f"终端 resize: cols={cols}, rows={rows}")
                        elif msg_type == "heartbeat":
                            if websocket.client_state == WebSocketState.CONNECTED:
                                await websocket.send_json({"type": "heartbeat"})
                except WebSocketDisconnect:
                    logger.info("终端 WebSocket 客户端断开（send）")
                except Exception as e:
                    logger.error(f"终端发送数据异常：{e}")

            # 并发运行，当一个任务完成或异常时取消另一个
            tasks = [
                asyncio.create_task(recv_from_pod()),
                asyncio.create_task(send_to_pod())
            ]

            # 等待任意一个任务完成（通常是客户端断开）
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            # 取消剩余任务
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            # 发送关闭消息
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_json({
                    "type": "close",
                    "reason": "终端连接已关闭"
                })

        except Exception as e:
            logger.error(f"终端连接失败：{e}", exc_info=True)
            try:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"终端连接失败：{str(e)}"
                    })
            except Exception:
                pass
        finally:
            # 确保 K8s exec 连接关闭
            if resp is not None:
                try:
                    await asyncio.to_thread(resp.close)
                    logger.info(f"终端 K8s exec 连接已关闭：{namespace}/{pod_name}")
                except Exception as e:
                    logger.warning(f"关闭 K8s exec 连接失败：{e}")

            # 确保 WebSocket 连接关闭
            try:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.close()
            except Exception:
                pass
