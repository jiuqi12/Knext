import asyncio
import json

from fastapi import Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user import User
from app.utils.logger import logger
from app.utils.exceptions import AuthException, ForbiddenException

AUTH_TIMEOUT_SECONDS = 5

# OAuth2 scheme，用于从请求头中获取token
# 默认 Authorization: Bearer <token> 中读取
api_key = HTTPBearer(auto_error=False)


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(api_key)) -> dict:
    """
    验证 JWT token 并返回当前用户的信息
    """
    if token is None:
        logger.error("未找到token")
        raise AuthException("凭证错误")
    try:
        # 解析JWT
        jwt_token = token.credentials
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])

        # 获取当前用户的信息
        username: str = payload.get("username")
        if username is None:
            logger.error("登陆失败：token失效或用户不存在")
            raise AuthException("凭证错误")
    except JWTError as e:
        logger.error(f"token 错误{e}")
        raise AuthException("凭证错误")

    # 查询用户状态
    user = await User.get_or_none(username=username)
    if not user:
        logger.error(f"用户{username}不存在")
        raise AuthException("凭证错误")

    # 检查用户状态
    if not user.is_active:
        logger.error(f"用户{user}已被禁用")
        raise ForbiddenException("用户已被禁用")

    # 返回当前用户
    return {
        "id": user.id,
        "username": user.username,
        "role_id": user.role_id,
        "is_admin": user.is_admin,
        "email": user.email,
    }


async def _send_auth_fail(websocket: WebSocket, reason: str):
    """发送认证失败消息，连接已关闭时静默忽略"""
    try:
        await websocket.send_json({"type": "auth_fail", "message": reason})
    except Exception:
        pass


async def verify_websocket_token(websocket: WebSocket) -> dict:
    """
    通过消息认证验证 WebSocket 连接

    流程：
    1. accept 连接
    2. 等待客户端发送 {"type": "auth", "token": "..."}（5 秒超时）
    3. 验证 JWT + 用户状态
    4. 成功返回 user dict，失败发送 auth_fail 并关闭连接
    """
    await websocket.accept()

    # 带超时等待认证消息
    try:
        raw = await asyncio.wait_for(
            websocket.receive_text(),
            timeout=AUTH_TIMEOUT_SECONDS
        )
    except asyncio.TimeoutError:
        logger.error("WebSocket 认证超时：5秒内未收到认证消息")
        await _send_auth_fail(websocket, "认证超时，请在连接后立即发送认证消息")
        await websocket.close(code=1008)
        raise HTTPException(status_code=401, detail="认证超时")
    except WebSocketDisconnect:
        logger.info("WebSocket 连接在认证前断开")
        raise HTTPException(status_code=401, detail="连接已断开")

    # 解析 JSON 并校验消息类型
    try:
        message = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        await _send_auth_fail(websocket, "消息格式错误，需要 JSON 格式")
        await websocket.close(code=1008)
        raise HTTPException(status_code=401, detail="消息格式错误")

    if message.get("type") != "auth" or not message.get("token"):
        await _send_auth_fail(websocket, "第一条消息必须是认证消息，格式：{\"type\":\"auth\",\"token\":\"...\"}")
        await websocket.close(code=1008)
        raise HTTPException(status_code=401, detail="缺少认证消息")

    token = message["token"]

    # 验证 JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            await _send_auth_fail(websocket, "无效的认证令牌：缺少用户信息")
            await websocket.close(code=1008)
            raise HTTPException(status_code=401, detail="token 无效")
    except JWTError as e:
        logger.error(f"WebSocket JWT 验证失败: {e}")
        await _send_auth_fail(websocket, "认证令牌无效或已过期")
        await websocket.close(code=1008)
        raise HTTPException(status_code=401, detail="token 验证失败")

    # 查询用户并验证状态
    user = await User.get_or_none(username=username)
    if not user:
        logger.error(f"用户 {username} 不存在")
        await _send_auth_fail(websocket, "用户不存在")
        await websocket.close(code=1008)
        raise HTTPException(status_code=401, detail="用户不存在")

    if not user.is_active:
        logger.error(f"用户 {username} 已被禁用")
        await _send_auth_fail(websocket, "用户已被禁用")
        await websocket.close(code=1003)
        raise HTTPException(status_code=403, detail="用户已被禁用")

    # 认证成功
    await websocket.send_json({"type": "auth_ok"})
    logger.info(f"WebSocket 认证成功：user={username}")

    return {
        "id": user.id,
        "username": user.username,
        "role_id": user.role_id,
        "is_admin": user.is_admin,
        "email": user.email,
    }
