# User 表

from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=11, unique=True, description="用户名")
    password = fields.CharField(max_length=118, description="密码")
    is_active = fields.BooleanField(default=True, description="激活状态")
    login_attempts = fields.IntField(default=0, description="登录错误次数，超过三次为")
    email = fields.CharField(max_length=22, description="邮箱")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    last_login_attempt = fields.DatetimeField(null=True, description="最后登录尝试时间")

