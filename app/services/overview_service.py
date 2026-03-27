from typing import Any, Dict
from datetime import datetime
from kubernetes.client.exceptions import ApiException
from app.core.k8s_client import get_core_v1_api, get_apps_v1_api, get_custom_objects_api
from app.utils.logger import logger
from app.utils.parse import parse_cpu, parse_mem


class OverviewService:
    @staticmethod
    def get_overview() -> Dict[str, Any]:
        """获取集群概览信息"""
        try:
            v1 = get_core_v1_api()
            apps_v1 = get_apps_v1_api()
            custom_objects = get_custom_objects_api()

            # 获取所有的 nodes
            nodes = v1.list_node()
            node_total = len(nodes.items)

            # 获取 nodes 概览数据
            nodes_list = []
            for node in nodes.items:
                nodes_list.append({
                    "name": node.metadata.name,
                    "status": (state.type for state in node.status.conditions if state.type == "Ready"),
                    "roles": (
                                label[len("node-role.kubernetes.io/"):]
                                for label in node.metadata.labels
                                if label.startswith("node-role.kubernetes.io/")
                            ),
                    "version": node.status.node_info.kubelet_version,
                })

            # 获取所有的 namespace
            namespaces = v1.list_namespace()
            namespace_total = len(namespaces.items)

            # 获取所有的 Pod
            pods = v1.list_pod_for_all_namespaces()
            pod_total = len(pods.items)

            # 获取 pods 运行状态
            pods_status = [
                {"title": "运行中", "type": "success" , "value": len([pod for pod in pods.items if pod.status.phase == "Running"])},
                {"title": "等待中", "type": "primary" , "value": len([pod for pod in pods.items if pod.status.phase == "Pending"])},
                {"title": "失败", "type": "warning" , "value": len([pod for pod in pods.items if pod.status.phase == "Failed"])},
                {"title": "完成", "type": "info" , "value": len([pod for pod in pods.items if pod.status.phase == "Succeeded"])},
                {"title": "未知", "type": "warning" , "value": len([pod for pod in pods.items if pod.status.phase == "Unknown"])}
            ]

            # 获取所有的 deployment
            deployments = apps_v1.list_deployment_for_all_namespaces()
            deployment_total = len(deployments.items)

            # 从 metrics-server 获取实时资源使用量
            total_cpu = 0
            total_mem = 0
            usage_cpu = 0
            usage_mem = 0
            percent_cpu = 0
            percent_mem = 0
            try:
                # 获取所有节点总容量
                for node in nodes.items:
                    total_cpu += parse_cpu(node.status.capacity["cpu"])
                    total_mem += parse_mem(node.status.capacity["memory"])

                # 获取所有节点的 metrics
                resources_metircs = custom_objects.list_cluster_custom_object(
                    group='metrics.k8s.io',
                    version='v1beta1',
                    plural='nodes'
                )

                # 从metrics中累加节点总使用量
                for item in resources_metircs['items']:
                    usage_cpu += parse_cpu(item['usage']['cpu'])
                    usage_mem += parse_mem(item['usage']['memory'])

                # 计算百分比
                percent_cpu = round((usage_cpu / total_cpu) * 100, 2)
                percent_mem = round((usage_mem / total_mem) * 100, 2)

            except ApiException as e:
                logger.warning(f"metrics-server 不可用，请安装metrics-server{e}")
                pass

            # 获取最近事件（从所有命名空间）
            recent_events = []
            try:
                # 获取所有命名空间的事件
                events = v1.list_event_for_all_namespaces(limit=5)
                # 按时间戳排序，取最新的 5 个事件

                for event in events.items:
                    recent_events.append({
                        "type": event.type or "Normal",
                        "reason": event.reason or "",
                        "message": event.message or "",
                        "lastTimestamp": event.last_timestamp.strftime(
                            "%Y-%m-%d %H:%M:%S") if event.last_timestamp else (
                            event.event_timestamp.isoformat() if event.event_timestamp else None
                        )
                    })
            except Exception as e:
                logger.warning(f"获取事件失败：{e}")
                pass

            logger.info("获取集群概览成功")
            # 构建响应数据
            return {
                "clusterInfo": [
                    {"title": "Nodes", "value": node_total},
                    {"title": "Namespaces", "value": namespace_total},
                    {"title": "Pods", "value": pod_total},
                    {"title": "Deployments", "value": deployment_total}
                ],
                "refreshTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "resourceUsage": {
                    "cpu": {
                        "total_cpu": total_cpu,
                        "usage_cpu": usage_cpu,
                        "percent_cpu": percent_cpu
                    },
                    "mem": {
                        "total_mem": total_mem,
                        "usage_mem": usage_mem,
                        "percent_mem": percent_mem
                    }
                },
                "nodes_list": nodes_list,
                "pods_status": pods_status,
                "recentEvents": recent_events,

            }
        except ApiException as e:
            logger.error(f"获取集群概览失败：{e}")
            raise
