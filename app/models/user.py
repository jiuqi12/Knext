from tortoise.models import Model
from tortoise import fields


# 用户表
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, unique=True, description="用户名")
    hash_password = fields.CharField(max_length=118, description="密码")
    is_active = fields.BooleanField(default=True, description="激活状态")
    login_attempts = fields.IntField(default=0, description="登录错误次数，超过三次禁用账号")
    email = fields.CharField(max_length=30, description="邮箱")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    last_login_attempt = fields.DatetimeField(auto_now=True, null=True, description="最后登录尝试时间")


# 权限表