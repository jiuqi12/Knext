from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# 配置项
SECRET_KEY = "d8e8fca2dc0f896fd7cb4cb0031ba2492a0a3e5c3b3b3b3b3b3b3b3b3b3b3b3b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__ident="2b", deprecated="auto")


def verify_password(plain_password, hash_password):
    """
    校验明文密码 vs 哈希密码
    """
    return pwd_context.verify(plain_password, hash_password)



def get_password_hash(password: str):
    """
    对密码进行哈希（用于注册/修改密码）
    """
    return pwd_context.hash(password)



def create_access_token(data: dict):
    """
    生成JWT Token 访问令牌
    """
    to_encode = data.copy()
    # 设置过期时间
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 生成token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
