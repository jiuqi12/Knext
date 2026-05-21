# from app.core.k8s_client import get_networking_v1_api
# from kubernetes.client.exceptions import ApiException
# from app.utils.logger import logger
# from typing import List, Dict, Any
#
#
# class GatewayService:
#     @staticmethod
#     def get_gateways(namespace: str = None) -> List[Dict[str, Any]]:
#         """获取 gateways 列表"""
#         try:
#             gateway_v1 = get_networking_v1_api()
#             if namespace:
#                 gateway_list = gateway_v1.list_namespaced_gateway(namespace).items
#             else:
#                 gateway_list = gateway_v1.list_gateway_for_all_namespaces().items
#             logger.info(f"获取命名空间 {namespace} 下的 gateways")
#             return [
#                 {
#                     "name": gateway.metadata.name,
#                     "namespace": gateway.metadata.namespace,
#                     "class": gateway.spec.gateway_class_name,
#                     "labels": gateway.metadata.labels,
#                     "address": gateway.status.addresses[0].value,
#                     "listeners": [
#                         {
#                             "name": listener.name,
#                             "port": listener.port,
#                             "protocol": listener.protocol
#                         }
#                         for listener in gateway.spec.listeners
#                     ],
#                     "status": gateway.status.conditions[0].status,
#                     "creation_time": gateway.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
#                 }for gateway in gateway_list
#             ]
#         except ApiException as e:
#             logger.error(f"获取 gateways 列表失败：{e}")
#             pass
#
#
#     @staticmethod
#     def get_gateway(namespace: str, gateway_name: str) -> Dict[str, Any]:
#         """获取指定 gateway 的详细信息"""
#         try:
#             gateway_v1 = get_networking_v1_api()
#             gateway = gateway_v1.read_namespaced_gateway(gateway_name, namespace)
#             logger.info(f"获取 {namespace}/{gateway_name} 命名空间下的 gateway")
#             return {
#                 "name": gateway.metadata.name,
#                 "namespace": gateway.metadata.namespace,
#                 "class": gateway.spec.gateway_class_name,
#                 "labels": gateway.metadata.labels,
#                 "address": gateway.status.addresses[0].value,
#                 "listeners": [
#                     {
#                         "name": listener.name,
#                         "port": listener.port,
#                         "protocol": listener.protocol
#                     }
#                     for listener in gateway.spec.listeners
#                 ],
#                 "status": gateway.status.conditions[0].status,
#                 "creation_time": gateway.metadata.creation_timestamp.strftime()
#             }
#         except ApiException as e:
#             logger.error(f"获取 {namespace}/{gateway_name} 命名空间下的 gateway 失败：{e}")
#             raise