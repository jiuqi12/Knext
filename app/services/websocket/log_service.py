import websockets
from fastapi import WebSocket
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import get_core_v1_api
from app.utils.logger import logger
from typing import Optional


# 日志逻辑处理
class PodLogService:
    """Pod 日志 WebSocket 服务"""

    @staticmethod
    async def stream_logs(websocket: WebSocket, namespace: str, pod_name: str, container: Optional[str] = None):
        """
        流式传输 Pod 日志

        Args:
            websocket: WebSocket 连接对象
            namespace: 命名空间
            pod_name: Pod 名称
            container: 容器名称（可选，当 Pod 有多个容器时需要指定）
        """
        try:
            v1 = get_core_v1_api()

            # 验证 Pod 是否存在
            # try:
            #     pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            #     logger.info(f"Pod 验证成功：{pod_name}, 状态：{pod.status.phase}")
            # except ApiException as e:
            #     await websocket.send_json({
            #         "type": "error",
            #         "message": f"Pod 不存在或无法访问：{e.reason}"
            #     })
            #     await websocket.close()
            #     return

            # # 如果未指定容器且 Pod 有多个容器，返回容器列表让前端选择
            # if not container:
            #     containers = []
            #     if pod.spec.containers:
            #         containers = [c.name for c in pod.spec.containers]
            #     if len(containers) > 1:
            #         await websocket.send_json({
            #             "type": "info",
            #             "message": f"Pod 有多个容器，请指定容器名称：{containers}"
            #         })
            #         container = containers[0]  # 默认使用第一个容器
            #         logger.info(f"使用默认容器：{container}")

            # 打开日志流
            logger.info(f"开始获取日志：namespace={namespace}, pod={pod_name}, container={container}")

            log_stream = v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                container=container,
                follow=True,
                tail_lines=1000,
                _preload_content=False,
                timestamps=True
            )

            await websocket.accept()
            logger.info(f"WebSocket 已接受连接：{namespace}/{pod_name}")

            # 发送初始消息
            await websocket.send_json({
                "type": "connected",
                "message": f"已连接到 Pod {namespace}/{pod_name} 的日志流"
            })

            # 读取并发送日志
            line_count = 0
            for line in log_stream.stream():
                try:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line:
                        await websocket.send_json({
                            "type": "log",
                            "data": decoded_line
                        })
                        line_count += 1

                        # 每 100 行记录一次日志
                        if line_count % 100 == 0:
                            logger.info(f"已发送 {line_count} 行日志")
                except websockets.exceptions.ConnectionClosed:
                    logger.info("WebSocket 连接已关闭，停止日志流")
                    break
                except Exception as e:
                    logger.error(f"发送日志失败：{e}")
                    continue

            # 日志流结束
            try:
                await websocket.send_json({
                    "type": "end",
                    "message": f"日志流已结束，共发送 {line_count} 行"
                })
                await websocket.close()
            except Exception:
                pass

        except ApiException as e:
            logger.error(f"K8s API 错误：{e}")
            try:
                if websocket.client_connected:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"K8s API 错误：{e.reason}"
                    })
                    await websocket.close()
            except Exception:
                pass
        except Exception as e:
            logger.error(f"日志流处理失败：{e}", exc_info=True)
            try:
                if websocket.client_connected:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"日志流处理失败：{str(e)}"
                    })
                    await websocket.close()
            except Exception:
                pass