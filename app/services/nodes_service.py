from app.core.k8s_client import K8sClientWrapper
from kubernetes.client.exceptions import ApiException
from app.utils.logger import logger
from typing import Dict, Any, List
from app.utils.parse import parse_mem, parse_cpu


class NodesService:
    @staticmethod
    async def get_nodes(k8s_wrapper: K8sClientWrapper = None) -> List[Dict[str, Any]]:
        """获取所有节点信息"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            node_list = v1.list_node().items
            return [
                {
                    "name": node.metadata.name,
                    "status": next((state.type for state in node.status.conditions if state.type == "Ready"),
                                   "Unknown"),
                    "roles": [role.role for role in node.metadata.labels.get("node-role.kubernetes.io", [])],
                    "labels": node.metadata.labels,
                    "version": node.status.node_info.kubelet_version,
                    "runtime": node.status.node_info.container_runtime_version,
                    "internal_ip": node.status.addresses[0].address,
                    "os": node.status.node_info.os_image,
                    "cpu": parse_cpu(node.status.capacity.get("cpu")),
                    "memory": parse_mem(node.status.capacity.get("memory")),
                    "pods": node.status.capacity.get("pods"),
                    "creation_time": node.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                }for node in node_list
            ]
        except ApiException as e:
            logger.error(f"获取节点信息失败：{e}")
            raise

    @staticmethod
    async def get_node(node_name: str, k8s_wrapper: K8sClientWrapper = None) -> Dict[str, Any]:
        """获取指定节点信息"""
        try:
            v1 = await k8s_wrapper.get_core_v1_api()
            node = v1.read_node(node_name)
            return {
                "name": node.metadata.name,
                "status": next((state.type for state in node.status.conditions if state.type == "Ready"),
                               "Unknown"),
                "roles": [role.role for role in node.metadata.labels.get("node-role.kubernetes.io", [])],
                "labels": node.metadata.labels,
                "version": node.status.node_info.kubelet_version,
                "runtime": node.status.node_info.container_runtime_version,
            }

        except ApiException as e:
            logger.error(f"获取节点信息失败：{e}")
            raise
