# Knext

新一代 Kubernetes 可视化管理面板，提供直观的 Web 界面来管理 Kubernetes 集群资源。

## 功能特性

- **工作负载管理** — Pod、Deployment、DaemonSet、StatefulSet、Job、CronJob 的查看、删除与扩缩容
- **网络资源** — Service、Ingress、Gateway 的管理
- **配置管理** — ConfigMap、Secret 的查看与编辑
- **存储管理** — PV、PVC、StorageClass 的管理
- **安全 RBAC** — Role、ClusterRole、RoleBinding、ClusterRoleBinding、ServiceAccount 管理
- **集群概览** — 仪表盘展示集群资源使用概况
- **Namespace / Node 管理** — 命名空间与节点的浏览
- **YAML 编辑器** — 基于 Monaco Editor 的 YAML 资源创建与编辑
- **Pod 终端** — 浏览器内通过 xterm.js 直接 exec 进入 Pod
- **实时日志** — WebSocket 流式查看 Pod 日志
- **多用户与权限** — 基于 JWT 认证，每个用户绑定独立的 Kubernetes ServiceAccount

## 技术栈

| 层 | 技术 |
|---|---|
| 后端框架 | FastAPI + Uvicorn |
| 数据库 | MySQL (Tortoise ORM + Aerich 迁移) |
| K8s 客户端 | kubernetes Python SDK |
| 认证 | JWT (python-jose) + bcrypt |
| 包管理 | uv |
| 前端框架 | Vue 3 + Vue Router + Pinia |
| UI 组件库 | Element Plus |
| 构建工具 | Vite |
| 终端模拟 | xterm.js |
| 代码编辑器 | Monaco Editor / CodeMirror |
| 图表 | ECharts |

## 项目结构

```
Knext/
├── app/                    # Python 后端
│   ├── api/                # 路由定义 (v1)
│   ├── core/               # 数据库、K8s 客户端、安全模块
│   ├── middleware/          # ASGI 中间件
│   ├── models/             # ORM 模型
│   ├── schemas/            # Pydantic 请求/响应模型
│   ├── services/           # 业务逻辑层
│   └── utils/              # 工具函数
├── ui/                     # Vue 前端
│   ├── src/
│   │   ├── api/            # API 调用封装
│   │   ├── components/     # 公共组件 (Log, Terminal, YamlEditor)
│   │   ├── views/          # 页面视图
│   │   ├── stores/         # Pinia 状态管理
│   │   ├── router/         # 路由配置
│   │   └── utils/          # 前端工具
│   └── package.json
├── migrations/             # Aerich 数据库迁移文件
├── pyproject.toml          # Python 项目配置
└── uv.lock                 # uv 锁文件
```

## 快速开始

### 环境要求

- Python >= 3.10
- Node.js ^20.19 或 >= 22.12
- MySQL 5.7+ / 8.0+
- 可访问的 Kubernetes 集群

### 1. 克隆项目

```bash
git clone <repo-url>
cd Knext
```

### 2. 后端启动

```bash
# 安装 uv (如未安装)
pip install uv

# 安装依赖
uv sync

# 配置数据库连接
# 编辑 app/core/database.py 中的数据库连接字符串
# 默认: mysql://root:000000@127.0.0.1:3306/knext

# 初始化数据库迁移
aerich init-db

# 启动后端服务 (默认 8000 端口)
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 前端启动

```bash
cd ui

# 安装依赖
npm install

# 启动开发服务器 (默认 5173 端口)
npm run dev
```

### 4. 访问

浏览器打开 `http://localhost:5173`，使用管理员账号登录。

## API 文档

后端启动后访问 Swagger UI：`http://localhost:8000/docs`

### API 路由一览

| 路径 | 功能 |
|---|---|
| `/api/v1/users` | 用户管理与登录 |
| `/api/v1/overview` | 集群概览 |
| `/api/v1/namespaces` | 命名空间管理 |
| `/api/v1/nodes` | 节点管理 |
| `/api/v1/workloads` | 工作负载管理 |
| `/api/v1/configs` | ConfigMap / Secret |
| `/api/v1/networks` | Service / Ingress / Gateway |
| `/api/v1/securities` | RBAC 资源 |
| `/api/v1/storages` | PV / PVC / StorageClass |
| `/api/v1/create_resource` | YAML 方式创建资源 |
| `/api/v1/ws` | WebSocket (日志 / 终端) |

## 架构说明

- **多租户 K8s 访问**：每个用户绑定一个 Kubernetes ServiceAccount，通过 TokenRequest API 获取短期 Token，客户端缓存 5 分钟自动续期
- **统一响应格式**：所有 API 返回 `{code, msg, data, request_id}` 结构
- **请求追踪**：ASGI 中间件为每个请求注入 `X-Request-ID`，贯穿日志链路
- **全局异常处理**：自定义异常层级 (BizException, AuthException, K8sException 等) 由统一 Handler 转换为 HTTP 响应

## 许可证

[MIT](LICENSE)
