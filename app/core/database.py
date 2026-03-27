# ORM 初始化与连接配置

TORTOISE_ORM = {
    "connections": {
        # 生产环境下，建议从环境变量读取 db_url
        "default": "mysql://root:000000@127.0.0.1:3306/knext"
    },
    "apps": {
        "models": {
            # 确保 user.py 文件放在 app/models/ 目录下
            "models": ["app.models.user"],
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}