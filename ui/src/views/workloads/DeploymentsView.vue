<template>
  <el-container>
    <el-main>
      <div class="header">
        <h2>Deployment 部署</h2>
        <div class="controls">
          <el-input
            v-model="searchQuery"
            placeholder="搜索部署名称"
            prefix-icon="Search"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
        </div>
      </div>

      <el-table
        :data="paginatedData"
        style="width: 100%"
        border
        v-loading="loading"
      >
        <el-table-column prop="name" label="名称" width="180" fixed>
        </el-table-column>
        <el-table-column prop="namespace" label="命名空间" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.namespace }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="副本数" width="120" align="center">
          <template #default="{ row }">
            <span :style="{ color: row.replicas?.ready === row.replicas?.desired ? '#67c23a' : '#e6a23c' }">
              {{ row.replicas?.ready || 0 }}/{{ row.replicas?.desired || 0 }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.replicas?.ready === row.replicas?.desired ? 'success' : 'warning'">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="更新策略" width="130" align="center">
          <template #default="{ row }">
            <el-tag type="info">{{ row.strategy }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="容器镜像" min-width="200">
          <template #default="{ row }">
            <div v-for="c in row.containers" :key="c.name" class="container-item">
              <span class="container-name">{{ c.name }}</span>
              <span class="container-image">{{ c.image }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="标签" min-width="180">
          <template #default="{ row }">
            <el-tag
              v-for="(val, key) in row.labels"
              :key="key"
              size="small"
              class="label-tag"
            >
              {{ key }}={{ val }}
            </el-tag>
            <span v-if="!row.labels || Object.keys(row.labels).length === 0">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ row.created_at }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleScale(row)">
              扩缩容
            </el-button>
            <el-button link type="danger" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next, jumper"
        prev-text="上一页"
        next-text="下一页"
        @current-change="handlePageChange"
      ></el-pagination>

      <!-- 扩缩容对话框 -->
      <el-dialog v-model="scaleDialogVisible" title="扩缩容" width="400px">
        <el-form :model="scaleForm" label-width="80px">
          <el-form-item label="副本数">
            <el-input-number
              v-model="scaleForm.replicas"
              :min="1"
              :max="100"
              style="width: 100%"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="scaleDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitScale" v-loading="loading">
            确定
          </el-button>
        </template>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getDeployments, deleteDeployment } from '@/api/cluster'

defineOptions({
  name: 'DeploymentsView'
})

// 加载状态
const loading = ref(false)
// 源数据
const datas = ref([])
// 搜索后数据
const filteredData = ref([])

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

// 总条数
const total = computed(() => filteredData.value.length)

// 获取 Deployments 列表
const getDeploymentData = async () => {
  loading.value = true
  try {
    const res = await getDeployments()
    datas.value = res?.data || []
    filteredData.value = [...datas.value]
  } catch {
    ElMessage.error('获取部署列表失败')
  } finally {
    loading.value = false
  }
}

// 扩缩容对话框状态
const scaleDialogVisible = ref(false)
// 扩缩容表单
const scaleForm = ref({
  replicas: 1
})
// 扩缩容表单
const handleScale = async (row) => {
  scaleDialogVisible.value = true
  scaleForm.value = {
    replicas: row.replicas,
    name: row.name,
    namespace: row.namespace
  }
}
// 提交扩缩容
const submitScale = async () => {
  try {
    loading.value = true
    // TODO: 调用扩缩容 API
    // await scaleDeployment(selectedDeployment.value.name, selectedDeployment.value.namespace, scaleForm.value.replicas)
    ElMessage.success(
      `扩缩容成功: ${scaleForm.value.name} 副本数设为 ${scaleForm.value.replicas}`
    )
    scaleDialogVisible.value = false
  } catch {
    ElMessage.error('扩缩容失败')
  } finally {
    loading.value = false
  }
}

// 删除Deployment
const handleDelete = (row) => {
  ElMessageBox.confirm(`确定要删除部署 ${row.name} 吗？`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // TODO: 调用删除 API
      await deleteDeployment(row.name, row.namespace)
      ElMessage.success('删除成功')
      getDeploymentData()
    } catch {
      ElMessage.error('删除失败')
    }
  })
}

// 组件挂载时获取数据
onMounted(() => {
  getDeploymentData()
})
</script>

<style lang="scss" scoped>
.header {
  height: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  h2 {
    margin: 0;
  }
  .controls {
    display: flex;
    align-items: center;
    gap: 15px;
  }
}

.empty-state {
  padding: 40px 0;
}

.container-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 2px 0;

  .container-name {
    font-weight: 500;
    color: #303133;
  }

  .container-image {
    font-size: 12px;
    color: #909399;
    font-family: monospace;
  }
}

.label-tag {
  margin: 2px 4px 2px 0;
}
</style>
