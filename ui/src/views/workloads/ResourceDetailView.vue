<template>
  <div class="resource-detail">
    <h2>{{ resourceType }} 详情 - {{ name }}</h2>

    <!-- 基本信息 -->
    <el-card class="box-card" style="margin-bottom: 20px">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
        </div>
      </template>
      <el-descriptions :column="1" border size="large">
        <el-descriptions-item label="名称">{{
          detailData.metadata.name
        }}</el-descriptions-item>
        <el-descriptions-item label="命名空间">{{
          detailData.metadata.namespace
        }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusTagType">{{ detailData.status.phase }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{
          formatTime(detailData.metadata.creationTimestamp)
        }}</el-descriptions-item>
        <el-descriptions-item label="标签">
          <el-tag
            v-for="(value, key) in detailData.metadata.labels"
            :key="key"
            style="margin-right: 5px; margin-bottom: 5px"
          >
            {{ key }}: {{ value }}
          </el-tag>
          <el-tag
            v-if="
              !detailData.metadata.labels ||
              Object.keys(detailData.metadata.labels).length === 0
            "
            type="info"
            >无标签</el-tag
          >
        </el-descriptions-item>
        <el-descriptions-item label="注解">
          <el-popover
            v-if="
              detailData.metadata.annotations &&
              Object.keys(detailData.metadata.annotations).length > 0
            "
            placement="right"
            width="400"
            trigger="hover"
          >
            <template #reference>
              <el-button link type="primary"
                >查看注解 ({{
                  Object.keys(detailData.metadata.annotations).length
                }})</el-button
              >
            </template>
            <div
              v-for="(value, key) in detailData.metadata.annotations"
              :key="key"
              style="margin-bottom: 10px"
            >
              <strong>{{ key }}:</strong>
              <div style="margin-left: 10px; word-break: break-all">
                {{ value }}
              </div>
            </div>
          </el-popover>
          <el-tag v-else type="info">无注解</el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 状态信息 -->
    <el-card
      class="box-card"
      style="margin-bottom: 20px"
      v-if="detailData.status"
    >
      <template #header>
        <div class="card-header">
          <span>状态信息</span>
        </div>
      </template>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="阶段">{{
          detailData.status.phase
        }}</el-descriptions-item>
        <el-descriptions-item label="主机IP">{{
          detailData.status.hostIP
        }}</el-descriptions-item>
        <el-descriptions-item label="Pod IP">{{
          detailData.status.podIP
        }}</el-descriptions-item>
        <el-descriptions-item label="启动时间">{{
          formatTime(detailData.status.startTime)
        }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 容器信息 -->
    <el-card
      class="box-card"
      style="margin-bottom: 20px"
      v-if="detailData.spec.containers"
    >
      <template #header>
        <div class="card-header">
          <span>容器信息 ({{ detailData.spec.containers.length }})</span>
        </div>
      </template>
      <el-table
        :data="detailData.spec.containers"
        style="width: 100%"
        row-key="name"
      >
        <el-table-column prop="name" label="名称" width="180"></el-table-column>
        <el-table-column prop="image" label="镜像">
          <template #default="scope">
            <el-tooltip :content="scope.row.image" placement="top">
              <span>{{ scope.row.image }}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="端口映射">
          <template #default="scope">
            <div v-for="port in scope.row.ports" :key="port.containerPort">
              {{ port.containerPort }}/{{ port.protocol }} ->
              {{ port.hostPort || 'N/A' }}
            </div>
            <div v-if="!scope.row.ports || scope.row.ports.length === 0">
              无端口映射
            </div>
          </template>
        </el-table-column>
        <el-table-column label="环境变量">
          <template #default="scope">
            <el-tag
              v-for="env in scope.row.env"
              :key="env.name"
              style="margin-right: 5px; margin-bottom: 5px"
            >
              {{ env.name }}
            </el-tag>
            <el-tag
              v-if="!scope.row.env || scope.row.env.length === 0"
              type="info"
              >无环境变量</el-tag
            >
          </template>
        </el-table-column>
        <el-table-column label="资源限制">
          <template #default="scope">
            <div v-if="scope.row.resources && scope.row.resources.limits">
              CPU: {{ scope.row.resources.limits.cpu }}<br />
              内存: {{ scope.row.resources.limits.memory }}
            </div>
            <div v-else>未设置</div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 卷信息 -->
    <el-card
      class="box-card"
      style="margin-bottom: 20px"
      v-if="detailData.spec.volumes"
    >
      <template #header>
        <div class="card-header">
          <span>卷信息 ({{ detailData.spec.volumes.length }})</span>
        </div>
      </template>
      <el-table
        :data="detailData.spec.volumes"
        style="width: 100%"
        row-key="name"
      >
        <el-table-column prop="name" label="名称" width="180"></el-table-column>
        <el-table-column label="类型">
          <template #default="scope">
            <span v-if="scope.row.configMap">ConfigMap</span>
            <span v-else-if="scope.row.secret">Secret</span>
            <span v-else-if="scope.row.persistentVolumeClaim"
              >PersistentVolumeClaim</span
            >
            <span v-else-if="scope.row.emptyDir">EmptyDir</span>
            <span v-else>未知</span>
          </template>
        </el-table-column>
        <el-table-column label="挂载信息">
          <template #default="scope">
            <div
              v-for="container in detailData.spec.containers"
              :key="container.name"
            >
              <div
                v-for="volumeMount in container.volumeMounts || []"
                :key="volumeMount.mountPath"
              >
                <span v-if="volumeMount.name === scope.row.name">
                  {{ container.name }}: {{ volumeMount.mountPath }}
                  {{ volumeMount.readOnly ? '(只读)' : '' }}
                </span>
              </div>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 事件信息 -->
    <el-card
      class="box-card"
      style="margin-bottom: 20px"
      v-if="events && events.length > 0"
    >
      <template #header>
        <div class="card-header">
          <span>最近事件 ({{ events.length }})</span>
        </div>
      </template>
      <el-timeline>
        <el-timeline-item
          v-for="(event, index) in events"
          :key="index"
          :timestamp="formatTime(event.lastTimestamp)"
          :type="event.type === 'Warning' ? 'danger' : 'success'"
        >
          <el-card shadow="hover">
            <h4>{{ event.reason }}</h4>
            <p><strong>消息:</strong> {{ event.message }}</p>
            <p>
              <strong>来源:</strong> {{ event.source.component }}/{{
                event.source.host
              }}
            </p>
            <p>
              <strong>第一次出现:</strong>
              {{ formatTime(event.firstTimestamp) }}
            </p>
            <p><strong>计数:</strong> {{ event.count }}</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>

    <el-button @click="$router.back()" style="margin-top: 20px">
      返回列表
    </el-button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

// 获取路由参数
const route = useRoute()

// 定义响应式数据
const resourceType = ref(route.params.resourceType || 'Pod')
const name = ref(route.params.name)
const namespace = ref(route.params.namespace || 'default')

// 假数据 - 模拟K8s Pod资源详细信息
const fakePodData = {
  apiVersion: 'v1',
  kind: 'Pod',
  metadata: {
    name: 'nginx-deployment-75675f5897-abcde',
    namespace: 'default',
    uid: 'a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8',
    creationTimestamp: '2025-03-04T10:30:00Z',
    labels: {
      app: 'nginx',
      'pod-template-hash': '75675f5897'
    },
    annotations: {
      'kubectl.kubernetes.io/last-applied-configuration':
        '{"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"name":"nginx-deployment","namespace":"default"},"spec":{"replicas":3,"selector":{"matchLabels":{"app":"nginx"}},"template":{"metadata":{"labels":{"app":"nginx"}},"spec":{"containers":[{"image":"nginx:1.15.4","name":"nginx","ports":[{"containerPort":80}]}]}}}}',
      'checksum/config': '0123456789abcdef'
    }
  },
  spec: {
    containers: [
      {
        name: 'nginx',
        image: 'nginx:1.15.4',
        ports: [
          {
            containerPort: 80,
            protocol: 'TCP'
          }
        ],
        env: [
          {
            name: 'ENVIRONMENT',
            value: 'production'
          },
          {
            name: 'LOG_LEVEL',
            value: 'info'
          }
        ],
        resources: {
          limits: {
            cpu: '500m',
            memory: '512Mi'
          },
          requests: {
            cpu: '250m',
            memory: '256Mi'
          }
        },
        volumeMounts: [
          {
            name: 'config-volume',
            mountPath: '/etc/config',
            readOnly: true
          },
          {
            name: 'logs',
            mountPath: '/var/log/nginx'
          }
        ]
      }
    ],
    volumes: [
      {
        name: 'config-volume',
        configMap: {
          name: 'nginx-config'
        }
      },
      {
        name: 'logs',
        emptyDir: {}
      }
    ],
    restartPolicy: 'Always',
    terminationGracePeriodSeconds: 30,
    dnsPolicy: 'ClusterFirst',
    serviceAccountName: 'default',
    nodeName: 'node-1',
    securityContext: {},
    schedulerName: 'default-scheduler'
  },
  status: {
    phase: 'Running',
    conditions: [
      {
        type: 'Initialized',
        status: 'True',
        lastProbeTime: null,
        lastTransitionTime: '2025-03-04T10:30:15Z'
      },
      {
        type: 'Ready',
        status: 'True',
        lastProbeTime: null,
        lastTransitionTime: '2025-03-04T10:31:00Z'
      },
      {
        type: 'ContainersReady',
        status: 'True',
        lastProbeTime: null,
        lastTransitionTime: '2025-03-04T10:31:00Z'
      },
      {
        type: 'PodScheduled',
        status: 'True',
        lastProbeTime: null,
        lastTransitionTime: '2025-03-04T10:30:15Z'
      }
    ],
    hostIP: '192.168.1.10',
    podIP: '10.244.0.5',
    startTime: '2025-03-04T10:30:15Z',
    containerStatuses: [
      {
        name: 'nginx',
        state: {
          running: {
            startedAt: '2025-03-04T10:31:00Z'
          }
        },
        lastState: {},
        ready: true,
        restartCount: 0,
        image: 'nginx:1.15.4',
        imageID: 'docker-pullable://nginx@sha256:abcd1234',
        containerID: 'docker://efgh5678'
      }
    ],
    qosClass: 'Burstable'
  }
}

// 假事件数据
const fakeEvents = [
  {
    metadata: {
      name: 'nginx-deployment-75675f5897-abcde.17890123456789ab',
      namespace: 'default',
      uid: 'i4j5k6l7-m8n9-o0p1-q2r3-s4t5u6v7w8x9',
      creationTimestamp: '2025-03-04T10:31:15Z'
    },
    involvedObject: {
      kind: 'Pod',
      namespace: 'default',
      name: 'nginx-deployment-75675f5897-abcde',
      uid: 'a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8',
      apiVersion: 'v1',
      resourceVersion: '12345',
      fieldPath: 'spec.containers{nginx}'
    },
    reason: 'Pulled',
    message: 'Successfully pulled image "nginx:1.15.4"',
    source: {
      component: 'kubelet',
      host: 'node-1'
    },
    firstTimestamp: '2025-03-04T10:30:45Z',
    lastTimestamp: '2025-03-04T10:30:45Z',
    count: 1,
    type: 'Normal',
    eventTime: null,
    series: null,
    action: 'Pulled',
    related: null,
    reportingComponent: '',
    reportingInstance: ''
  },
  {
    metadata: {
      name: 'nginx-deployment-75675f5897-abcde.17890123456789ac',
      namespace: 'default',
      uid: 'j5k6l7m8-n9o0-p1q2-r3s4-t5u6v7w8x9y0',
      creationTimestamp: '2025-03-04T10:31:30Z'
    },
    involvedObject: {
      kind: 'Pod',
      namespace: 'default',
      name: 'nginx-deployment-75675f5897-abcde',
      uid: 'a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8',
      apiVersion: 'v1',
      resourceVersion: '12346',
      fieldPath: 'spec.containers{nginx}'
    },
    reason: 'Created',
    message: 'Created container nginx',
    source: {
      component: 'kubelet',
      host: 'node-1'
    },
    firstTimestamp: '2025-03-04T10:30:50Z',
    lastTimestamp: '2025-03-04T10:30:50Z',
    count: 1,
    type: 'Normal',
    eventTime: null,
    series: null,
    action: 'Created',
    related: null,
    reportingComponent: '',
    reportingInstance: ''
  },
  {
    metadata: {
      name: 'nginx-deployment-75675f5897-abcde.17890123456789ad',
      namespace: 'default',
      uid: 'k6l7m8n9-o0p1-q2r3-s4t5-u6v7w8x9y0z1',
      creationTimestamp: '2025-03-04T10:31:45Z'
    },
    involvedObject: {
      kind: 'Pod',
      namespace: 'default',
      name: 'nginx-deployment-75675f5897-abcde',
      uid: 'a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8',
      apiVersion: 'v1',
      resourceVersion: '12347',
      fieldPath: 'spec.containers{nginx}'
    },
    reason: 'Started',
    message: 'Started container nginx',
    source: {
      component: 'kubelet',
      host: 'node-1'
    },
    firstTimestamp: '2025-03-04T10:31:00Z',
    lastTimestamp: '2025-03-04T10:31:00Z',
    count: 1,
    type: 'Normal',
    eventTime: null,
    series: null,
    action: 'Started',
    related: null,
    reportingComponent: '',
    reportingInstance: ''
  }
]

// 使用假数据
const detailData = ref(fakePodData)
const events = ref(fakeEvents)

// 计算属性：根据状态设置标签类型
const statusTagType = computed(() => {
  switch (detailData.value.status.phase) {
    case 'Running':
      return 'success'
    case 'Pending':
      return 'warning'
    case 'Failed':
    case 'Error':
      return 'danger'
    default:
      return ''
  }
})

// 时间格式化函数
const formatTime = (timestamp) => {
  if (!timestamp) return 'N/A'

  try {
    const date = new Date(timestamp)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    })
  } catch (error) {
    console.error('时间格式化错误:', error)
    return timestamp
  }
}
</script>

<style lang="scss" scoped>
.resource-detail {
  padding: 20px;
}

.card-header {
  font-size: 16px;
  font-weight: bold;
}

.el-card {
  border-radius: 8px;
}

.el-descriptions {
  margin-top: 10px;
}

.el-tag {
  margin-right: 5px;
}

.el-table {
  margin-top: 10px;
}

.el-timeline {
  margin-top: 10px;
}

.box-card {
  margin-bottom: 20px;
}
</style>
