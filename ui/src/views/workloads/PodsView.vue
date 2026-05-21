<template>
  <el-container>
    <el-main>
      <!-- 头部操作区 -->
      <div class="header">
        <h2>Pods 管理</h2>
        <div class="controls">
          <el-input
            v-model="searchQuery"
            placeholder="搜索 Pod 名称或命名空间"
            clearable
            prefix-icon="Search"
            style="width: 300px"
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          />
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </div>
      </div>

      <!-- 表格列表 -->
      <el-table
        :data="paginatedData"
        style="width: 100%"
        border
        v-loading="loading"
        element-loading-text="加载中..."
      >
        <el-table-column fixed prop="name" label="名称" width="200">
        </el-table-column>
        <el-table-column
          prop="namespace"
          label="命名空间"
          width="120"
        ></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="restart_count"
          label="重启次数"
          width="100"
        ></el-table-column>
        <el-table-column label="标签" width="260">
          <template #default="{ row }">
            <div v-if="row.labels !== null">
              <el-tag
                v-for="(value, key) in row.labels"
                :key="key"
                style="margin-right: 5px; margin-bottom: 5px"
              >
                {{ key }}={{ value }}
              </el-tag>
            </div>
            <div v-else>无标签</div>
          </template>
        </el-table-column>
        <el-table-column
          prop="pod_ip"
          label="Pod_IP"
          width="130"
        ></el-table-column>
        <el-table-column
          prop="node_name"
          label="节点"
          width="120"
        ></el-table-column>
        <el-table-column
          prop="images[0]"
          label="镜像"
          width="300"
        ></el-table-column>
        <el-table-column
          prop="creation_time"
          label="创建时间"
          width="120"
        ></el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleLog(row)">
              查看日志
            </el-button>
            <el-button link type="primary" @click="handleTerminal(row)">
              Web终端
            </el-button>
            <el-button link type="danger" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        class="custom-pagination"
        v-model:current-page.sync="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next, jumper"
        :prev-text="'上一页'"
        :next-text="'下一页'"
        @current-change="handlePageChange"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed, ref, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getPods, deletePod } from '@/api/cluster'
import router from '@/router'
import { ElMessage, ElMessageBox } from 'element-plus'

defineOptions({
  name: 'PodsView'
})

// 加载状态
const loading = ref(false)
// 源数据
const datas = ref([])
// 搜索后数据
const filteredData = ref([])

// 搜索参数
const searchQuery = ref('')
// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  if (!searchQuery.value.trim()) {
    filteredData.value = [...datas.value]
  } else {
    const query = searchQuery.value.toLowerCase()
    filteredData.value = datas.value.filter(
      (item) =>
        item.name.toLowerCase().includes(query) ||
        item.namespace.toLowerCase().includes(query)
    )
  }
}

// 分页处理
const currentPage = ref(1)
const pageSize = ref(10)
// 计算分页数据
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredData.value.slice(start, end)
})
// 分页变化处理
const handlePageChange = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 计算总数
const total = computed(() => filteredData.value.length)

// 状态映射表
const getStatusType = (status) => {
  const statusMap = {
    Running: 'success',
    Pending: 'warning',
    Failed: 'danger',
    Succeeded: 'info',
    Unknown: ''
  }
  return statusMap[status] || ''
}

// ECharts 饼图
const chartRef = ref(null)
let chartInstance = null

const statusCounts = computed(() => {
  const counts = {}
  datas.value.forEach((pod) => {
    const s = pod.status || 'Unknown'
    counts[s] = (counts[s] || 0) + 1
  })
  return Object.entries(counts).map(([name, value]) => ({ name, value }))
})

const statusColors = {
  Running: '#67c23a',
  Pending: '#e6a23c',
  Failed: '#f56c6c',
  Succeeded: '#909399',
  Unknown: '#c0c4cc'
}

const initChart = () => {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chartInstance) return
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'center'
    },
    color: Object.values(statusColors),
    series: [
      {
        name: 'Pod 状态',
        type: 'pie',
        radius: ['40%', '70%'],
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
        data: statusCounts.value
      }
    ]
  }
  chartInstance.setOption(option, true)
}

watch(
  statusCounts,
  () => {
    nextTick(updateChart)
  },
  { deep: true }
)

// Web 终端
const handleTerminal = (row) => {
  const container = row.container_name ? `/${row.container_name}` : ''
  router.push(`/terminal/${row.namespace}/${row.name}${container}`)
}

// 查看 Pod 日志
const handleLog = (row) => {
  const container = row.container_name ? `/${row.container_name}` : ''
  router.push(`/logs/${row.namespace}/${row.name}${container}`)
}

// 删除 Pod
const handleDelete = (row) => {
  ElMessageBox.confirm(`确定要删除 Pod "${row.name}" 吗？`, '删除确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deletePod(row.namespace, row.name)
        ElMessage.success(`删除成功${row.name}`)
        await getData()
      } catch (error) {
        console.error('删除失败:', error)
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {
      ElMessage.info('已取消删除')
    })
}

// 获取数据
const getData = async () => {
  loading.value = true
  try {
    const res = await getPods()
    // 根据实际 API 返回结构调整数据路径
    datas.value = res?.data || []
    filteredData.value = [...datas.value]
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
    datas.value = []
    filteredData.value = []
  } finally {
    loading.value = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  getData()
  nextTick(initChart)
})
</script>

<style lang="scss" scoped>
.header {
  height: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

  h2 {
    margin: 0;
    font-size: 20px;
    color: #303133;
  }

  .controls {
    display: flex;
    align-items: center;
    gap: 15px;
  }
}

:deep(.el-pagination) {
  display: flex;
  justify-content: flex-end;
}
</style>
