# JWT 生成与解析与密码
import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext

# 配置项
SECRET_KEY = "d8e8fca2dc0f896fd7cb4cb0031ba2492a0a3e5c3b3b3b3b3b3b3b3b3b3b3b3b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__ident="2b", deprecated="auto")


# 密码哈希校验
# 校验明文密码 vs 哈希密码
def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)


# 对密码进行哈希（用于注册/修改密码）
def get_password_hash(password: str):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="服务器内部错误")


# 生成JWT Token 访问令牌
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
