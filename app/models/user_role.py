from tortoise.models import Model
from tortoise import fields


# 权限表
class UserRoles(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30, unique=True, description="角色名")
    service_accounts = fields.CharField(max_length=30, description="服务账号")
    namespace = fields.CharField(max_length=30, description="命名空间")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")