import json
from app.core.k8s_client import K8sClientWrapper
from kubernetes.dynamic import DynamicClient
from kubernetes.dynamic.exceptions import ResourceNotFoundError
from kubernetes.client import ApiException
from app.utils.logger import logger
from app.utils.exceptions import ValidationException
import yaml


def _parse_k8s_error(e: ApiException) -> str:
    """解析 K8s API 异常，提取友好的错误信息"""
    try:
        body = json.loads(e.body) if isinstance(e.body, str) else e.body
        message = body.get("message", "")
    except (json.JSONDecodeError, TypeError, AttributeError):
        message = str(e)

    # 常见错误类型映射
    if e.status == 400:
        # 类型错误（如 nodeSelector 格式错误）
        if "cannot unmarshal" in message:
            return f"YAML 字段格式错误：{message}"
        return f"请求格式错误：{message}"
    elif e.status == 403:
        return f"权限不足：{message}"
    elif e.status == 404:
        return f"资源不存在：{message}"
    elif e.status == 409:
        return f"资源冲突：{message}"
    elif e.status == 422:
        return f"资源验证失败：{message}"
    else:
        return f"K8s API 错误 ({e.status})：{message}"


class ResourceService:
    """创建资源类"""

    @staticmethod
    async def create_resource_yaml(yaml_body, k8s_wrapper: K8sClientWrapper = None) -> str:
        # 处理输入类型
        if isinstance(yaml_body, bytes):
            yaml_str = yaml_body.decode("utf-8")
        elif isinstance(yaml_body, str):
            yaml_str = yaml_body
        else:
            raise ValidationException("请求体必须是 YAML 字符串")

        # 解析 YAML
        try:
            files = list(yaml.safe_load_all(yaml_str))
        except yaml.YAMLError as e:
            error_msg = f"YAML 解析失败：{str(e)}"
            logger.error(error_msg)
            raise ValidationException(error_msg)

        if not files:
            raise ValidationException("YAML 内容为空")

        count = 0
        result = []
        api_client = await k8s_wrapper.get_api_client()
        dyn_client = DynamicClient(api_client)

        for idx, file in enumerate(files):
            if not file or not isinstance(file, dict):
                continue

            api_version = file.get("apiVersion")
            kind = file.get("kind")
            metadata = file.get("metadata", {})
            name = metadata.get("name")
            namespace = metadata.get("namespace", "default")

            # 参数校验
            if not api_version:
                raise ValidationException(f"第 {idx + 1} 个资源缺少 apiVersion 字段")
            if not kind:
                raise ValidationException(f"第 {idx + 1} 个资源缺少 kind 字段")
            if not name:
                raise ValidationException(f"第 {idx + 1} 个资源缺少 metadata.name 字段")

            # 获取资源类型
            try:
                resource = dyn_client.resources.get(api_version=api_version, kind=kind)
            except ResourceNotFoundError:
                raise ValidationException(f"未知的资源类型：{api_version}/{kind}")
            except ApiException as e:
                raise ValidationException(_parse_k8s_error(e))

            # 创建资源
            try:
                resp = dyn_client.server_side_apply(
                    resource=resource,
                    body=file,
                    name=name,
                    field_manager="admin",
                    namespace=namespace
                )
                count += 1
                result.append({
                    "name": resp.metadata.name,
                    "type": resp.kind
                })
            except ApiException as e:
                error_msg = _parse_k8s_error(e)
                logger.error(f"创建资源失败 [{kind}/{name}]：{error_msg}")
                raise ValidationException(f"创建 {kind}/{name} 失败：{error_msg}")
            except Exception as e:
                logger.error(f"创建资源异常 [{kind}/{name}]：{e}", exc_info=True)
                raise ValidationException(f"创建 {kind}/{name} 失败：{str(e)}")

        return f"创建成功，共创建 {count} 个资源，分别是 {result}"
