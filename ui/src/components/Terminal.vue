<template>
  <div class="terminal-wrapper">
    <div class="terminal-container">
      <!-- 标题栏 -->
      <div class="terminal-header">
        <div class="header-left">
          <div class="terminal-icon">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path
                d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V6h16v12zM6 10h2v2H6zm0 4h8v2H6zm10 0h2v2h-2zm-6-4h8v2h-8z"
              />
            </svg>
          </div>
          <div class="terminal-info">
            <h3>Terminal 终端</h3>
            <span class="pod-info">{{ podInfo }}</span>
          </div>
        </div>
        <div class="header-right">
          <div class="status-indicator" :class="statusClass">
            <span class="status-dot"></span>
            <span class="status-text">{{ statusText }}</span>
          </div>
          <el-button
            v-if="socket && socket.readyState !== WebSocket.OPEN"
            type="primary"
            size="small"
            @click="reconnect"
            :loading="reconnecting"
          >
            重连
          </el-button>
        </div>
      </div>
      <!-- 终端容器 -->
      <div class="terminal-body">
        <div class="terminal" ref="terminalRef"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { Terminal } from 'xterm'
import 'xterm/css/xterm.css'
import { FitAddon } from 'xterm-addon-fit'

// DOM引用
const terminalRef = ref(null)
// WebSocket连接实例（响应式）
const socket = ref(null)
// 终端实例（在 onMounted 中创建）
let term = null
let fitAddon = null
// 认证状态
const authenticated = ref(false)
let authTimer = null
// 重连定时器
let reconnectTimer = null
// 心跳定时器
let heartbeatTimer = null
// 重连状态
const reconnecting = ref(false)
const reconnectAttempts = ref(0)
const maxReconnectAttempts = 5

// 创建路由实例获取参数
const route = useRoute()

// 获取WebSocket基础URL
const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
const WS_BASE_URL = `${wsProtocol}//${window.location.host}`

// 获取Pod信息
const podInfo = computed(() => {
  const namespace = route.params.namespace
  const podName = route.params.pod_name
  const containerName =
    route.params.container_name && route.params.container_name !== 'undefined'
      ? route.params.container_name
      : ''
  return `${namespace}/${podName}${containerName ? ` (${containerName})` : ''}`
})

// 连接状态
const connectionStatus = ref('connecting') // connecting, authenticating, open, closing, closed

// 状态文本
const statusText = computed(() => {
  const statusMap = {
    connecting: '连接中...',
    authenticating: '认证中...',
    open: '已连接',
    closing: '断开中...',
    closed: '已断开'
  }
  return statusMap[connectionStatus.value] || '未知'
})

// 状态样式类
const statusClass = computed(() => {
  return `status-${connectionStatus.value}`
})

// 终端配置
const terminalConfig = {
  cursorBlink: true,
  fontSize: 14,
  fontFamily: 'Menlo, Monaco, "Courier New", monospace',
  theme: {
    background: '#1e1e1e',
    foreground: '#ffffff',
    cursor: '#ffffff',
    selectionBackground: 'rgba(255, 255, 255, 0.3)',
    black: '#000000',
    red: '#ff5555',
    green: '#50fa7b',
    yellow: '#f1fa8c',
    blue: '#bd93f9',
    magenta: '#ff79c6',
    cyan: '#8be9fd',
    white: '#f8f8f2',
    brightBlack: '#4d4d4d',
    brightRed: '#ff6e6e',
    brightGreen: '#69ff94',
    brightYellow: '#ffffa5',
    brightBlue: '#d6acff',
    brightMagenta: '#ff92df',
    brightCyan: '#a4ffff',
    brightWhite: '#ffffff'
  },
  scrollback: 5000,
  cursorStyle: 'block',
  minimumContrastRatio: 7,
  allowProposedApi: true
}

// 初始化终端
const initTerminal = () => {
  term = new Terminal(terminalConfig)
  fitAddon = new FitAddon()

  term.loadAddon(fitAddon)
  term.open(terminalRef.value)
  fitAddon.fit()
  term.focus()

  // 显示连接信息
  term.writeln('\x1b[36m========================================\x1b[0m')
  term.writeln('\x1b[36m  Kubernetes Pod Terminal\x1b[0m')
  term.writeln('\x1b[36m========================================\x1b[0m')
  term.writeln(`\x1b[33m  Pod: ${podInfo.value}\x1b[0m`)
  term.writeln('\x1b[36m========================================\x1b[0m')
  term.writeln('')
  term.writeln('\x1b[32m正在连接到容器...\x1b[0m')

  // 监听终端输入事件
  term.onData((data) => {
    if (
      socket.value &&
      socket.value.readyState === WebSocket.OPEN &&
      authenticated.value
    ) {
      socket.value.send(JSON.stringify({ type: 'stdin', data }))
    }
  })

  // 监听终端大小变化
  term.onResize(({ cols, rows }) => {
    if (
      socket.value &&
      socket.value.readyState === WebSocket.OPEN &&
      authenticated.value
    ) {
      socket.value.send(JSON.stringify({ type: 'resize', cols, rows }))
    }
  })

  // 窗口变化时重新适配
  window.addEventListener('resize', handleResize)
}

// 窗口大小变化处理
const handleResize = () => {
  if (terminalRef.value && fitAddon) {
    try {
      fitAddon.fit()
    } catch {
      // 组件销毁后忽略
    }
  }
}

// 发送认证消息
const sendAuth = () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    handleAuthFail('未找到登录凭证，请重新登录')
    return
  }

  connectionStatus.value = 'authenticating'
  term.writeln('\x1b[33m正在认证...\x1b[0m')

  socket.value.send(JSON.stringify({ type: 'auth', token }))

  // 认证超时计时器（5秒）
  authTimer = setTimeout(() => {
    if (!authenticated.value) {
      handleAuthFail('认证超时')
    }
  }, 5000)
}

// 认证成功处理
const handleAuthOk = () => {
  authenticated.value = true
  if (authTimer) {
    clearTimeout(authTimer)
    authTimer = null
  }

  connectionStatus.value = 'open'
  reconnectAttempts.value = 0
  reconnecting.value = false

  term.clear()
  term.writeln('\x1b[32m✓ 连接成功，认证通过！\x1b[0m')
  term.writeln('')

  // 发送初始终端尺寸
  if (term.cols && term.rows) {
    socket.value.send(
      JSON.stringify({ type: 'resize', cols: term.cols, rows: term.rows })
    )
  }

  startHeartbeat()
}

// 认证失败处理
const handleAuthFail = (message) => {
  authenticated.value = false
  if (authTimer) {
    clearTimeout(authTimer)
    authTimer = null
  }

  term.writeln(`\r\n\x1b[31m✗ 认证失败: ${message}\x1b[0m`)

  if (socket.value) {
    socket.value.onclose = null
    socket.value.close()
    socket.value = null
  }

  connectionStatus.value = 'closed'
  reconnecting.value = false

  // token 无效时跳转登录
  if (
    message.includes('凭证') ||
    message.includes('过期') ||
    message.includes('无效')
  ) {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_info')
    setTimeout(() => {
      window.location.href = '/login'
    }, 2000)
  }
}

// 创建WebSocket连接
const createWebSocket = () => {
  const namespace = route.params.namespace
  const podName = route.params.pod_name
  const containerName =
    route.params.container_name && route.params.container_name !== 'undefined'
      ? route.params.container_name
      : ''

  // 关闭旧连接
  if (socket.value) {
    socket.value.onclose = null
    socket.value.close()
    socket.value = null
  }
  authenticated.value = false

  // 构建WebSocket URL（不携带 token）
  let wsUrl = `${WS_BASE_URL}/api/v1/ws/pods/${namespace}/${podName}/terminal`
  if (containerName) {
    wsUrl += `?container=${containerName}`
  }

  try {
    socket.value = new WebSocket(wsUrl)
    connectionStatus.value = 'connecting'

    socket.value.onopen = () => {
      // 连接建立后发送认证消息
      sendAuth()
    }

    socket.value.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)

        if (message.type === 'auth_ok') {
          handleAuthOk()
        } else if (message.type === 'auth_fail') {
          handleAuthFail(message.message || '认证被拒绝')
        } else if (message.type === 'stdout') {
          term.write(message.data)
        } else if (message.type === 'error') {
          term.writeln(`\r\n\x1b[31m错误: ${message.message}\x1b[0m`)
        } else if (message.type === 'close') {
          term.writeln(
            `\r\n\x1b[33m容器会话已关闭: ${message.reason || '未知原因'}\x1b[0m`
          )
        } else if (message.type === 'heartbeat') {
          // 心跳响应，忽略
        } else {
          term.write(event.data)
        }
      } catch {
        term.write(event.data)
      }
    }

    socket.value.onerror = () => {
      term.writeln('\r\n\x1b[31m✗ 连接错误\x1b[0m')
    }

    socket.value.onclose = (event) => {
      connectionStatus.value = 'closed'
      authenticated.value = false
      stopHeartbeat()

      if (authTimer) {
        clearTimeout(authTimer)
        authTimer = null
      }

      if (event.code !== 1000 && event.code !== 1001) {
        term.writeln(`\r\n\x1b[31m✗ 连接已断开 (代码: ${event.code})\x1b[0m`)

        if (reconnectAttempts.value < maxReconnectAttempts) {
          autoReconnect()
        } else {
          reconnecting.value = false
          term.writeln('\x1b[33m已达到最大重连次数，请手动重连\x1b[0m')
        }
      }
    }
  } catch (error) {
    term.writeln(`\r\n\x1b[31m✗ 创建连接失败: ${error.message}\x1b[0m`)
    connectionStatus.value = 'closed'
  }
}

// 自动重连
const autoReconnect = () => {
  reconnectAttempts.value++
  reconnecting.value = true

  const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.value), 30000)

  term.writeln(
    `\x1b[33m${delay / 1000}秒后尝试第 ${reconnectAttempts.value} 次重连...\x1b[0m`
  )

  reconnectTimer = setTimeout(() => {
    if (connectionStatus.value !== 'open') {
      term.write('\r\x1b[K\x1b[32m正在重连...\x1b[0m')
      createWebSocket()
    }
  }, delay)
}

// 手动重连
const reconnect = () => {
  if (reconnecting.value) return

  reconnectAttempts.value = 0
  reconnecting.value = true

  term.clear()
  term.writeln('\x1b[32m正在重新连接...\x1b[0m')

  createWebSocket()
}

// 启动心跳
const startHeartbeat = () => {
  stopHeartbeat()

  heartbeatTimer = setInterval(() => {
    if (socket.value && socket.value.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify({ type: 'heartbeat' }))
    }
  }, 30000)
}

// 停止心跳
const stopHeartbeat = () => {
  if (heartbeatTimer) {
    clearInterval(heartbeatTimer)
    heartbeatTimer = null
  }
}

// 组件挂载后执行
onMounted(() => {
  initTerminal()
  createWebSocket()
})

// 组件销毁前执行
onBeforeUnmount(() => {
  if (reconnectTimer) {
    clearTimeout(reconnectTimer)
    reconnectTimer = null
  }
  if (authTimer) {
    clearTimeout(authTimer)
    authTimer = null
  }
  stopHeartbeat()

  if (socket.value) {
    socket.value.onclose = null
    socket.value.close()
    socket.value = null
  }

  if (term) {
    term.dispose()
    term = null
  }

  window.removeEventListener('resize', handleResize)
})
</script>

<style lang="scss" scoped>
.terminal-wrapper {
  padding: 24px;
  background-color: #e6e6e6;
  min-height: 100%;
  box-sizing: border-box;
}

.terminal-container {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 48px);
}

.terminal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;

    .terminal-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      color: #50fa7b;
    }

    .terminal-info {
      display: flex;
      flex-direction: column;
      gap: 2px;

      h3 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: 0.5px;
      }

      .pod-info {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.7);
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
      border-radius: 20px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      transition: all 0.3s ease;

      .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        transition: all 0.3s ease;
      }

      .status-text {
        font-size: 13px;
        font-weight: 500;
      }

      &.status-connecting {
        background: rgba(241, 250, 140, 0.15);
        border-color: rgba(241, 250, 140, 0.3);

        .status-dot {
          background: #f1fa8c;
          animation: pulse 1s infinite;
        }

        .status-text {
          color: #f1fa8c;
        }
      }

      &.status-open {
        background: rgba(80, 250, 123, 0.15);
        border-color: rgba(80, 250, 123, 0.3);

        .status-dot {
          background: #50fa7b;
          animation: pulse 2s infinite;
        }

        .status-text {
          color: #50fa7b;
        }
      }

      &.status-closing {
        background: rgba(255, 121, 198, 0.15);
        border-color: rgba(255, 121, 198, 0.3);

        .status-dot {
          background: #ff79c6;
          animation: pulse 0.5s infinite;
        }

        .status-text {
          color: #ff79c6;
        }
      }

      &.status-authenticating {
        background: rgba(64, 158, 255, 0.15);
        border-color: rgba(64, 158, 255, 0.3);

        .status-dot {
          background: #409eff;
          animation: pulse 1s infinite;
        }

        .status-text {
          color: #409eff;
        }
      }

      &.status-closed {
        background: rgba(255, 85, 85, 0.15);
        border-color: rgba(255, 85, 85, 0.3);

        .status-dot {
          background: #ff5555;
        }

        .status-text {
          color: #ff5555;
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

.terminal-body {
  flex: 1;
  padding: 16px;
  background: #1e1e1e;
  overflow: hidden;

  .terminal {
    width: 100%;
    height: 100%;
    border-radius: 8px;
    overflow: hidden;
  }
}

:deep(.xterm) {
  padding: 12px;
}

:deep(.xterm-viewport) {
  border-radius: 8px;
}

:deep(.xterm-screen) {
  font-family: Menlo, Monaco, 'Courier New', monospace;
}
</style>
