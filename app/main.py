from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api.api import v1_router
from tortoise.contrib.fastapi import register_tortoise
from app.core.database import TORTOISE_ORM

# 配置日志
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="K8s 可视化管理平台", description="K8s 可视化管理平台", version="0.1.0")

# 配置跨域（CORS）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # 生产环境应该替换为具体的前端域名，如 "http://localhost:3000", "https://yourdomain.com"
    ],
    allow_credentials=True,  # 允许携带 cookie
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    # generate_config=False, # 如果启用，则自动生成数据库配置
    add_exception_handlers=True # 如果启用，自动处理 Tortoise 抛出的 DoesNotExist 异常为 404
)

app.include_router(v1_router, prefix="/api")
