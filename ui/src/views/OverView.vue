<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'
import { getOverview, createResource } from '@/api/cluster'
import { ElMessage } from 'element-plus'

// 刷新时间相关
const refreshTime = ref('12:00:00')
// 加载状态
const isLoding = ref(false)
// 集群数据
const total_cards = ref([])
const total_nodes = ref([])
const recentEvents = ref([])
const pods_status = ref([])
const resource_usage = ref({})
// 获取数据
const fetchData = async () => {
  try {
    isLoding.value = true
    const res = await getOverview()
    refreshTime.value = res.data.refreshTime || []
    total_cards.value = res.data.clusterInfo || []
    total_nodes.value = res.data.nodes_list || []
    recentEvents.value = res.data.recentEvents || []
    pods_status.value = res.data.pods_status || []
    resource_usage.value = res.data.resourceUsage || {}
    console.log(resource_usage.value)
    ElMessage.success('刷新成功')
  } finally {
    isLoding.value = false
  }
}
const showEditor = ref(false)
const yamlContent = ref('')
const yamlEditorRef = ref(null)

// 创建资源
const handleCreateResource = async () => {
  // 前置校验：内容是否为空
  if (!yamlContent.value?.trim()) {
    ElMessage.warning('YAML 内容不能为空')
    return
  }

  // 前置校验：YAML 语法是否正确
  if (yamlEditorRef.value && !yamlEditorRef.value.validate()) {
    ElMessage.warning('YAML 格式有误，请先修正语法错误')
    return
  }

  try {
    isLoding.value = true
    const res = await createResource(yamlContent.value)
    showEditor.value = false
    yamlContent.value = ''
    ElMessage.success(res?.detail || '资源创建成功')
    fetchData()
  } catch (error) {
    console.error('创建资源失败:', error)
  } finally {
    isLoding.value = false
  }
}

// echarts饼图相关
const podChartRef = ref(null)
let podChartInstance = null

const initPodChart = () => {
  if (!podChartRef.value) return
  podChartInstance = echarts.init(podChartRef.value)
  updatePodChart()
}

const updatePodChart = () => {
  if (!podChartInstance) return

  // 状态名 → 颜色映射（匹配 API 返回的中文 title）
  const statusColorMap = {
    运行中: '#67c23a',
    等待中: '#e6a23c',
    失败: '#f56c6c',
    完成: '#909399',
    未知: '#c0c4cc'
  }

  // 按数据顺序生成颜色数组
  const chartData = pods_status.value.map((item) => ({
    name: item.title,
    value: item.value
  }))
  const colors = pods_status.value.map(
    (item) => statusColorMap[item.title] || '#409eff'
  )

  const option = {
    color: colors,
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} 个 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'center'
    },
    series: [
      {
        name: 'Pod 状态',
        type: 'pie',
        radius: ['40%', '65%'],
        center: ['60%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 6,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{c} 个'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 15,
            fontWeight: 'bold'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        data: chartData
      }
    ]
  }

  podChartInstance.setOption(option, true)
}

// 监听pods_status变化
watch(
  pods_status,
  () => {
    nextTick(() => {
      updatePodChart()
    })
  },
  { deep: true }
)

onMounted(() => {
  fetchData()
  nextTick(() => {
    initPodChart()
  })
})
</script>

<template>
  <div class="dashboard-container" :loading="isLoding">
    <!-- 集群版本 -->
    <div class="header">
      <div class="version">
        <h1>集群仪表盘</h1>
        <p>数据源: Kubernetes：v1.29</p>
        <p>更新时间：{{ refreshTime }}</p>
      </div>
      <div class="time">
        <el-button type="primary" @click="fetchData">刷新数据</el-button>
        <el-button type="primary" class="create-btn" @click="showEditor = true">
          <el-icon><Plus /></el-icon>
          创建资源
        </el-button>
        <el-dialog
          v-model="showEditor"
          destroy-on-close
          width="72%"
          class="create-resource-dialog"
          :show-close="true"
          :close-on-click-modal="false"
        >
          <template #header>
            <div class="dialog-header">
              <el-icon class="dialog-icon"><Document /></el-icon>
              <span>创建资源</span>
            </div>
          </template>
          <div class="dialog-body">
            <YamlEditor ref="yamlEditorRef" v-model="yamlContent" />
          </div>
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="showEditor = false" class="cancel-btn">
                取消
              </el-button>
              <el-button
                type="primary"
                @click="handleCreateResource"
                class="submit-btn"
              >
                <el-icon><Check /></el-icon>
                创建
              </el-button>
            </div>
          </template>
        </el-dialog>
      </div>
    </div>
    <!-- 集群信息区域 -->
    <el-row :gutter="20">
      <!-- 集群统计 -->
      <el-col
        :xs="12"
        :sm="6"
        v-for="(item, index) in total_cards"
        :key="index"
      >
        <el-card shadow="hover">
          <div class="card-inner">
            <div class="info">
              <div class="lable">
                <span>{{ item.title }}</span>
              </div>
              <div class="value">
                <span>{{ item.value }}</span>
              </div>
            </div>
            <div class="icon">
              <el-icon><Box /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 资源使用状态 -->
      <el-col>
        <el-card header="资源">
          <div class="resource-item">
            <span style="margin: 10px 0">CPU使用情况</span>
            <el-progress
              :percentage="resource_usage?.cpu?.percent_cpu"
              :stroke-width="20"
              :text-inside="true"
              :status="
                resource_usage?.cpu?.percent_cpu > 60 ? 'exception' : 'success'
              "
            ></el-progress>
            <span style="margin: 10px 0"
              >总量：{{ resource_usage?.cpu?.total_cpu || 0 }} vCPUs /
              已分配：{{ resource_usage?.cpu?.usage_cpu || 0 }} vCPUs</span
            >
          </div>
          <div class="resource-item">
            <span>内存使用情况</span>
            <el-progress
              :percentage="resource_usage?.mem?.percent_mem"
              :stroke-width="20"
              :text-inside="true"
              :status="
                resource_usage?.mem?.percent_mem > 60 ? 'exception' : 'success'
              "
            ></el-progress>
            <span
              >总量：{{ resource_usage?.mem?.total_mem || 0 }} GBi / 已分配：
              {{ resource_usage?.mem?.usage_mem || 0 }} GBi</span
            >
          </div>
        </el-card>
      </el-col>
      <!-- pods状态分布 -->
      <el-col>
        <el-card header="pods使用">
          <div ref="podChartRef" style="width: 100%; height: 380px"></div>
        </el-card>
      </el-col>
      <!-- 节点详情 -->
      <el-col>
        <el-card header="节点详情 (Nodes)">
          <el-table width="100%" :data="total_nodes">
            <el-table-column
              prop="name"
              label="name"
              width="100%"
              fixed
              align="center"
            ></el-table-column>
            <el-table-column label="status" align="center">
              <template v-slot="scope">
                <el-tag v-for="tag in scope.row.status" :key="tag">{{
                  tag
                }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="roles" align="center">
              <template v-slot="scope">
                <el-tag v-for="tag in scope.row.roles" :key="tag">{{
                  tag
                }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="version" align="center">
              <template v-slot="scope">
                <el-tag effect="dark">{{ scope.row.version }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <!-- 集群最近事件 -->
      <el-col>
        <el-card header="近期事件 (Events)">
          <el-timeline style="padding-left: 0">
            <el-timeline-item
              v-for="(ev, index) in recentEvents"
              :key="index"
              :type="ev.type === 'Warning' ? 'danger' : 'primary'"
              :timestamp="ev.lastTimestamp"
              size="normal"
            >
              <b style="font-size: 13px">{{ ev.reason }}</b>
              <p style="font-size: 13px; color: #666; margin-top: 4px">
                {{ ev.message }}
              </p>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style lang="scss" scoped>
h1 {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
}
.dashboard-container {
  padding: 32px;
  margin: 0 auto;
  width: 100%;
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    flex-wrap: wrap; /** 解决元素宽度不够时，换行显示，保证移动端显式正常 */
    gap: 16px;
    .version {
      p {
        font-size: 14px;
        color: #6b7280;
      }
    }
  }
  // 卡片公共样式
  .el-card {
    border: none;
    border-radius: 12px;
    margin-bottom: 20px;
    .card-inner {
      display: flex;
      justify-content: space-between;
      align-items: center;
      height: 80px;
      .info {
        .label {
          font-size: 15px;
          font-weight: 800;
          padding-bottom: 30px;
          span {
            font-size: 12px;
            font-weight: 400;
            color: #3b82f6;
          }
        }
        .value {
          font-size: 25px;
          font-weight: 800;
        }
      }
      .icon {
        font-size: 30px;
      }
    }
  }
  // 资源项样式
  .resource-item {
    margin: 30px;
    span {
      margin: 10px 0;
    }
  }
  // 创建资源按钮
  .create-btn {
    border-radius: 8px;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(64, 158, 255, 0.35);
    }
  }
  // Pod项样式
  .pod-item {
    text-align: center;
    border-radius: 50%;
    padding: 16px;
    width: 110px;
    height: 110px;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border: 2px solid #dee2e6;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 8px;
    margin: 0 auto;

    &:hover {
      transform: translateY(-4px) scale(1.05);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
      border-color: #c5cae9;
      background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
    }

    > div {
      margin-bottom: 2px;

      :deep(.el-tag) {
        font-size: 11px;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 12px;
        border: none;
        letter-spacing: 0.3px;
      }
    }

    span {
      font-size: 22px;
      font-weight: 700;
      color: #343a40;
      line-height: 1;
      display: block;
      transition: color 0.3s ease;
    }

    &:hover span {
      color: #5c7cfa;
    }
  }
}

// 创建资源对话框样式
.create-resource-dialog {
  .dialog-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 17px;
    font-weight: 700;
    color: #303133;
    .dialog-icon {
      font-size: 20px;
      color: #409eff;
    }
  }
  .dialog-body {
    height: 520px;
  }
  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    .cancel-btn {
      border-radius: 8px;
    }
    .submit-btn {
      border-radius: 8px;
      font-weight: 600;
      padding: 8px 24px;
      transition: all 0.3s ease;
      &:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(64, 158, 255, 0.35);
      }
    }
  }
}

:deep(.el-dialog) {
  border-radius: 12px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
  margin: 0;
}

:deep(.el-dialog__body) {
  padding: 16px 20px;
}

:deep(.el-dialog__footer) {
  padding: 12px 24px;
  border-top: 1px solid #f0f0f0;
}
</style>
