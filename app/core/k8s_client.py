# k8s_client 单例模式封装

from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from kubernetes.client.configuration import Configuration
from kubernetes.dynamic import DynamicClient
from kubernetes.dynamic.exceptions import ResourceNotFoundError
import urllib3
from app.utils.logger import logger

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class K8sClient:
    """Kubernetes 客户端单例封装"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(K8sClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            try:
                # 尝试加载 k8s 配置
                config.load_incluster_config()
                logger.info("成功加载集群内配置")
            except ConfigException:
                # 如果不在集群内，尝试加载本地 kubeconfig
                try:
                    config.load_kube_config()
                    logger.info("成功加载本地 kubeconfig 配置")
                except ConfigException as e:
                    logger.error(f"K8s 配置加载失败：{e}")
                    raise

            # 配置 API 客户端，禁用 SSL 验证（适用于开发环境）
            configuration = Configuration.get_default_copy()
            configuration.verify_ssl = False
            configuration.assert_hostname = False
            Configuration.set_default(configuration)

            # 初始化常用的 API 客户端
            self.api_client = client.ApiClient(configuration)
            self.core_v1 = client.CoreV1Api(client.ApiClient(configuration))
            self.apps_v1 = client.AppsV1Api(client.ApiClient(configuration))
            self.batch_v1 = client.BatchV1Api(client.ApiClient(configuration))
            self.networking_v1 = client.NetworkingV1Api(client.ApiClient(configuration))
            self.custom_objects = client.CustomObjectsApi(client.ApiClient(configuration))
            self.storage_v1 = client.StorageV1Api(client.ApiClient(configuration))

            self._initialized = True
            logger.info("K8s 客户端初始化成功（已禁用 SSL 验证）")

    def get_api_client(self) -> client.api_client:
        return self.api_client

    def get_core_v1_api(self) -> client.CoreV1Api:
        """获取 CoreV1Api 客户端"""
        return self.core_v1

    def get_apps_v1_api(self) -> client.AppsV1Api:
        """获取 AppsV1Api 客户端"""
        return self.apps_v1

    def get_batch_v1_api(self) -> client.BatchV1Api:
        """获取 BatchV1Api 客户端"""
        return self.batch_v1

    def get_networking_v1_api(self) -> client.NetworkingV1Api:
        """获取 NetworkingV1Api 客户端"""
        return self.networking_v1

    def get_custom_objects_api(self) -> client.CustomObjectsApi:
        """获取 CustomObjectsApi 客户端"""
        return self.custom_objects

    def get_storage_v1_api(self) -> client.StorageV1Api:
        """获取 StorageV1Api 客户端"""
        return self.storage_v1


# 全局实例
k8s_client = K8sClient()


# 便捷访问函数

def get_api_client() -> client.api_client:
    """获取 API 客户端"""
    return k8s_client.get_api_client()


def get_k8s_client() -> K8sClient:
    """获取 K8s 客户端单例实例"""
    return k8s_client


def get_core_v1_api() -> client.CoreV1Api:
    """获取 CoreV1Api 客户端"""
    return k8s_client.get_core_v1_api()


def get_apps_v1_api() -> client.AppsV1Api:
    """获取 AppsV1Api 客户端"""
    return k8s_client.get_apps_v1_api()


def get_batch_v1_api() -> client.BatchV1Api:
    """获取 BatchV1Api 客户端"""
    return k8s_client.get_batch_v1_api()


def get_networking_v1_api() -> client.NetworkingV1Api:
    """获取 NetworkingV1Api 客户端"""
    return k8s_client.get_networking_v1_api()


def get_custom_objects_api() -> client.CustomObjectsApi:
    """获取 CustomObjectsApi 客户端"""
    return k8s_client.get_custom_objects_api()


def get_storage_v1_api() -> client.StorageV1Api:
    """获取 StorageV1Api 客户端"""
    return k8s_client.get_storage_v1_api()
