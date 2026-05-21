<template>
  <div class="log-wrapper">
    <div class="log-container">
      <!-- 标题栏 -->
      <div class="log-header">
        <div class="header-left">
          <div class="log-icon">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path
                d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"
              />
            </svg>
          </div>
          <div class="header-title">
            <h3>Kubernetes Pod Logs</h3>
            <span class="subtitle">{{ namespace }} / {{ pod_name }}</span>
          </div>
        </div>
        <div class="header-right">
          <div class="status-indicator" :class="{ connected: isConnected }">
            <span class="status-dot"></span>
            <span class="status-text">{{
              isConnected ? '已连接' : '未连接'
            }}</span>
          </div>
        </div>
      </div>

      <!-- 控制栏 -->
      <div class="controls">
        <button
          class="btn btn-start"
          @click="connect"
          :disabled="isConnected || isConnecting"
        >
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M8 5v14l11-7z" />
          </svg>
          <span>{{ isConnecting ? '连接中...' : '开始监听' }}</span>
        </button>
        <button
          class="btn btn-stop"
          @click="disconnect"
          :disabled="!isConnected"
        >
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M6 6h12v12H6z" />
          </svg>
          <span>停止监听</span>
        </button>
        <button class="btn btn-clear" @click="clearLogs">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path
              d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
            />
          </svg>
          <span>清空日志</span>
        </button>
      </div>

      <!-- 日志窗口 -->
      <div class="log-body">
        <div class="log-window" ref="logWindow">
          <div v-for="(line, index) in logs" :key="index" class="log-line">
            <span class="line-number">{{ index + 1 }}</span>
            <span class="line-content">{{ line }}</span>
          </div>
          <div v-if="logs.length === 0" class="empty-state">
            <svg viewBox="0 0 24 24" width="48" height="48" fill="currentColor">
              <path
                d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 12H4V8h16v10z"
              />
            </svg>
            <p>点击"开始监听"按钮查看日志</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()

const ws = ref(null)
const logs = ref([])
const namespace = route.params.namespace
const pod_name = route.params.pod_name
const isConnecting = ref(false)
const isAuthenticated = ref(false)
const isConnected = ref(false)
let authTimer = null

const logWindow = ref(null)

// 认证失败处理
const handleAuthFail = (message) => {
  isAuthenticated.value = false
  isConnecting.value = false
  isConnected.value = false
  if (authTimer) {
    clearTimeout(authTimer)
    authTimer = null
  }
  logs.value.push(`[认证失败] ${message}`)
  if (ws.value) {
    ws.value.onclose = null
    ws.value.close()
    ws.value = null
  }
}

function connect() {
  if (isConnected.value || isConnecting.value) return

  isConnecting.value = true
  isAuthenticated.value = false
  isConnected.value = false
  logs.value = []

  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const url = `${wsProtocol}//${window.location.host}/api/v1/ws/pods/${namespace}/${pod_name}/logs`

  ws.value = new WebSocket(url)

  ws.value.onopen = () => {
    isConnected.value = true
    // 连接后发送认证消息
    const token = localStorage.getItem('access_token')
    if (!token) {
      handleAuthFail('未找到登录凭证，请重新登录')
      return
    }
    ws.value.send(JSON.stringify({ type: 'auth', token }))

    // 认证超时
    authTimer = setTimeout(() => {
      if (!isAuthenticated.value) {
        handleAuthFail('认证超时')
      }
    }, 5000)
  }

  ws.value.onmessage = (event) => {
    try {
      const message = JSON.parse(event.data)
      if (message.type === 'auth_ok') {
        isAuthenticated.value = true
        if (authTimer) {
          clearTimeout(authTimer)
          authTimer = null
        }
        isConnecting.value = false
        logs.value.push('[系统] 认证通过，开始接收日志...')
        return
      } else if (message.type === 'auth_fail') {
        handleAuthFail(message.message || '认证被拒绝')
        return
      }
    } catch {
      // 非 JSON，按原始日志处理
    }

    // 认证通过后才接收日志
    if (!isAuthenticated.value) return

    logs.value.push(event.data)

    // 限制最大日志数量
    if (logs.value.length > 1000) {
      logs.value.shift()
    }

    scrollToBottom()
  }

  ws.value.onerror = () => {
    isConnecting.value = false
  }

  ws.value.onclose = () => {
    isConnecting.value = false
    isAuthenticated.value = false
    isConnected.value = false
    if (authTimer) {
      clearTimeout(authTimer)
      authTimer = null
    }
    ws.value = null
  }
}

function disconnect() {
  if (ws.value) {
    ws.value.close()
  }
}

function clearLogs() {
  logs.value = []
}

function scrollToBottom() {
  nextTick(() => {
    if (logWindow.value) {
      logWindow.value.scrollTop = logWindow.value.scrollHeight
    }
  })
}
</script>

<style lang="scss" scoped>
.log-wrapper {
  padding: 24px;
  background-color: #e6e6e6;
  min-height: 100%;
  box-sizing: border-box;
}

.log-container {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 48px);
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;

    .log-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      background: rgba(56, 239, 125, 0.15);
      border-radius: 10px;
      color: #38ef7d;
    }

    .header-title {
      display: flex;
      flex-direction: column;
      gap: 4px;

      h3 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: 0.5px;
      }

      .subtitle {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.6);
        font-family: monospace;
      }
    }
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;

    .status-indicator {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      background: rgba(255, 107, 107, 0.15);
      border-radius: 20px;
      border: 1px solid rgba(255, 107, 107, 0.3);
      transition: all 0.3s ease;

      .status-dot {
        width: 8px;
        height: 8px;
        background: #ff6b6b;
        border-radius: 50%;
      }

      .status-text {
        font-size: 13px;
        color: #ff6b6b;
        font-weight: 500;
      }

      &.connected {
        background: rgba(56, 239, 125, 0.15);
        border-color: rgba(56, 239, 125, 0.3);

        .status-dot {
          background: #38ef7d;
          animation: pulse 2s infinite;
        }

        .status-text {
          color: #38ef7d;
        }
      }
    }
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(0.9);
  }
}

.controls {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;

  .btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    svg {
      flex-shrink: 0;
    }
  }

  .btn-start {
    background: linear-gradient(135deg, #80ff91 0%, #4dab71 100%);
    color: white;

    &:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
    }
  }

  .btn-stop {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
    color: white;

    &:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
    }
  }

  .btn-clear {
    background: #f1f3f4;
    color: #5f6368;

    &:hover {
      background: #e8eaeb;
    }
  }
}

.log-body {
  flex: 1;
  padding: 16px;
  background: #1a1a2e;
  overflow: hidden;

  .log-window {
    height: 100%;
    overflow: auto;
    background: #0d1117;
    border-radius: 8px;
    padding: 0;
    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
    font-size: 13px;
    line-height: 1.6;
    letter-spacing: 0.02em; /* 添加字符间距 */

    &::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }

    &::-webkit-scrollbar-track {
      background: #161b22;
    }

    &::-webkit-scrollbar-thumb {
      background: #30363d;
      border-radius: 4px;

      &:hover {
        background: #484f58;
      }
    }
  }
}

.log-line {
  display: flex;
  padding: 2px 16px; /* 增加垂直内边距 */
  transition: background 0.15s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.03);
  }

  .line-number {
    flex-shrink: 0;
    width: 48px;
    padding-right: 16px;
    color: #484f58;
    text-align: right;
    user-select: none;
    font-family:
      'Cascadia Code', 'Fira Code', 'Consolas', monospace; /* 等宽字体 */
    font-size: 12px; /* 稍小的字体大小 */
    opacity: 0.8;
  }

  .line-content {
    flex: 1;
    color: #c9d1d9;
    white-space: pre-wrap;
    word-break: break-all;
    font-family: inherit; /* 继承容器的等宽字体 */
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #8b949e;

  svg {
    opacity: 0.5;
    margin-bottom: 16px;
  }

  p {
    margin: 0;
    font-size: 14px;
  }
}

:deep(.xterm) {
  padding: 12px;
}

:deep(.xterm-viewport) {
  border-radius: 8px;
}
</style>
