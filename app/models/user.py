from tortoise.models import Model
from tortoise import fields


# 用户表
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, unique=True, description="用户名")
    hash_password = fields.CharField(max_length=118, description="密码")
    is_active = fields.BooleanField(default=True, description="是否启用改账号")
    login_attempts = fields.IntField(default=0, description="登录错误次数，超过三次禁用账号")
    is_admin = fields.BooleanField(default=False, description="是否是管理员")
    role_id = fields.IntField(description="角色ID")
    email = fields.CharField(max_length=30, description="邮箱")
    # namespace = fields.CharField(max_length=64, null=True, description="默认命名空间")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    last_login_attempt = fields.DatetimeField(null=True, description="最后登录尝试时间")

