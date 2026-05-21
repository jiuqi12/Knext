from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from kubernetes.client.configuration import Configuration
import urllib3
from app.utils.logger import logger
from app.utils.exceptions import K8sException
import time
from app.models.user_role import UserRoles

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class K8sClientManager:
    """Kubernetes 客户端管理器 - 支持多用户动态创建"""

    def __init__(self):
        # 缓存结构
        # user_id -> {client, expire_time}
        self.client_cache = {}
        
        # 基础配置(全局共享)，生产环境建议配置环境变量获取
        self.api_server = "https://master:6443"
        
        # 全局 api_client（用于创建 SA token）
        self._global_api_client = None
        
    def _get_global_client(self):
        """获取全局客户端（用于管理操作，如创建 SA token）"""
        if self._global_api_client is None:
            try:
                config.load_incluster_config()
                logger.info("成功加载集群内配置")
            except ConfigException:
                try:
                    config.load_kube_config()
                    logger.info("成功加载本地 kubeconfig 配置")
                except ConfigException as e:
                    logger.error(f"K8s 配置加载失败：{e}")
                    raise
            
            configuration = Configuration.get_default_copy()
            configuration.verify_ssl = False
            configuration.host = self.api_server
            self._global_api_client = client.ApiClient(configuration)
        
        return self._global_api_client

    async def get_client(self, user: dict):
        """
        根据用户返回对应权限的 client
        """
        user_id = user["user_id"]

        # 2. 判断缓存是否存在
        if user_id in self.client_cache:
            logger.info(f"使用缓存的 K8s client: user_id={user_id}")
            cache = self.client_cache[user_id]

            # 未过期直接返回
            if cache["expire"] > time.time():
                logger.debug(f"使用缓存的 K8s client: user_id={user_id}")
                return cache["client"]
            else:
                logger.debug(f"K8s client 已过期，重新创建: user_id={user_id}")

        # 2. 生成新 client
        new_client = await self._create_client(user)

        # 3. 写入缓存（5分钟）
        self.client_cache[user_id] = {
            "client": new_client,
            "expire": time.time() + 300
        }
        
        logger.info(f"为用户创建新的 K8s client: user_id={user_id}, username={user.get('username')}")

        return new_client

    async def _create_client(self, user: dict):
        """为用户创建独立的 K8s client"""
        try:
            # 获取全局客户端用于创建 SA token
            global_client = self._get_global_client()
            user_role_id = user['role_id']

            role = await UserRoles.get_or_none(id=user_role_id).values()
            if not role:
                raise ValueError(f"用户角色不存在: user_role_id={user['role_id']}")
            
            sa_name = role['service_accounts']
            sa_namespace = role['namespace']
            
            # 使用全局客户端创建 CoreV1Api
            core_v1 = client.CoreV1Api(api_client=global_client)
            
            # 使用 TokenRequest API 获取 token
            body = client.AuthenticationV1TokenRequest(
                spec=client.V1TokenRequestSpec(
                    audiences=["https://kubernetes.default.svc.cluster.local"],
                    expiration_seconds=3600
                )
            )

            response = core_v1.create_namespaced_service_account_token(
                name=sa_name,
                namespace=sa_namespace,
                body=body
            )

            # 获取token
            token = response.status.token

            # 构造用户专属的 client 配置
            configuration = Configuration.get_default_copy()
            configuration.verify_ssl = False
            configuration.host = self.api_server
            configuration.api_key = {"authorization": f"Bearer {token}"}

            return client.ApiClient(configuration)

        except TimeoutError as e:
            logger.error(f"为用户创建 K8s client 失败: user_id={user.get('user_id')}, error={str(e)}")
            raise K8sException("K8s client 创建超时")
        
        except Exception as e:
            logger.error(f"为用户创建 K8s client 失败: user_id={user.get('user_id')}, error={str(e)}")
            raise


# 创建全局管理器实例
k8s_client_manager = K8sClientManager()
