import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import K8sClientWrapper
from app.utils.logger import logger
from typing import Optional


# 日志逻辑处理
class PodLogService:
    """Pod 日志 WebSocket 服务"""

    @staticmethod
    async def stream_logs(websocket: WebSocket, namespace: str, pod_name: str,
                          container: Optional[str] = None, k8s_wrapper: K8sClientWrapper = None):
        """
        流式传输 Pod 日志

        Args:
            websocket: WebSocket 连接对象
            namespace: 命名空间
            pod_name: Pod 名称
            container: 容器名称（可选，当 Pod 有多个容器时需要指定）
            k8s_wrapper: K8s 客户端包装器（由路由层认证后传入）
        """
        log_stream = None
        try:
            # 使用路由层传入的 K8s 客户端（认证已在路由层完成）
            v1 = await k8s_wrapper.get_core_v1_api()

            # 验证 Pod 是否存在
            try:
                pod = await asyncio.to_thread(v1.read_namespaced_pod, name=pod_name, namespace=namespace)
                logger.info(f"Pod 验证成功：{pod_name}，状态：{pod.status.phase}")
            except ApiException as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Pod 不存在或无法访问：{e.reason}"
                })
                await websocket.close()
                return

            # 打开日志流
            logger.info(f"开始获取日志：namespace={namespace}, pod={pod_name}, container={container}")

            log_stream = await asyncio.to_thread(
                v1.read_namespaced_pod_log,
                name=pod_name,
                namespace=namespace,
                container=container,
                follow=True,
                tail_lines=1000,
                _preload_content=False,
                timestamps=True
            )

            logger.info(f"WebSocket 已接受连接：{namespace}/{pod_name}")

            # 发送初始消息
            await websocket.send_json({
                "type": "connected",
                "message": f"已连接到 Pod {namespace}/{pod_name} 的日志流"
            })

            # 读取并发送日志（使用 Queue 桥接线程与协程）
            log_queue = asyncio.Queue()

            def log_producer():
                """在线程中读取日志流，放入队列"""
                try:
                    for line in log_stream.stream():
                        log_queue.put_nowait(line)
                except Exception as e:
                    log_queue.put_nowait(e)
                finally:
                    log_queue.put_nowait(None)  # 结束信号

            # 在线程池中启动生产者
            producer_task = asyncio.create_task(asyncio.to_thread(log_producer))

            line_count = 0
            try:
                while True:
                    item = await log_queue.get()
                    if item is None:
                        break
                    if isinstance(item, Exception):
                        raise item

                    decoded_line = item.decode('utf-8').strip()
                    if decoded_line:
                        if websocket.client_state == WebSocketState.CONNECTED:
                            await websocket.send_json({
                                "type": "stdout",
                                "data": decoded_line
                            })
                            line_count += 1

                        if line_count % 100 == 0:
                            logger.info(f"已发送 {line_count} 行日志")
            except WebSocketDisconnect:
                logger.info("WebSocket 连接已关闭，停止日志流")
                producer_task.cancel()

            # 日志流结束
            try:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_json({
                        "type": "close",
                        "reason": f"日志流已结束，共发送 {line_count} 行"
                    })
            except Exception as send_err:
                logger.info(f"发送结束消息失败：{send_err}")

        except WebSocketDisconnect:
            logger.info(f"日志 WebSocket 客户端断开：{namespace}/{pod_name}")
        except ApiException as e:
            logger.error(f"K8s API 错误：{e}")
            try:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"K8s API 错误：{e.reason}"
                    })
            except Exception:
                pass
        except Exception as e:
            logger.error(f"日志流处理失败：{e}", exc_info=True)
            try:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"日志处理失败：{e}"
                    })
            except Exception:
                pass
        finally:
            # 确保日志流关闭
            if log_stream is not None:
                try:
                    await asyncio.to_thread(log_stream.close)
                    logger.info(f"日志流已关闭：{namespace}/{pod_name}")
                except Exception as e:
                    logger.warning(f"关闭日志流失败：{e}")

            # 确保 WebSocket 连接关闭
            try:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.close()
            except Exception:
                pass
