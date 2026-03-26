# User 表

from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=11, unique=True, description="用户名")
    password = fields.CharField(max_length=118, description="密码")
    is_active = fields.IntField(default=3, description="账号登录次数，初始化为3，当变为0时不可用")
    email = fields.CharField(max_length=22, description="邮箱")
    department = fields.CharField(max_length=13, description="属于部门")

