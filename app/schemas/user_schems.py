from pydantic import BaseModel


# 登录请求体
class LoginRequest(BaseModel):
    username: str
    password: str


# 创建用户校验
class UserCreateOrUpdate(BaseModel):
    id: int = None
    username: str
    password: str
    email: str
    is_admin: bool = False
    namespace: str = None
    user_role_id: int

# 创建或修改用户角色校验
class UserRoleCreateOrUpdate(BaseModel):
    id: int = None
    name: str
    namespace: str
    service_accounts: str
    




