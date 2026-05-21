<template>
  <el-container>
    <el-main>
      <div class="header">
        <h2>ServiceAccount</h2>
        <div class="search-box">
          <el-input
            v-model="searchQuery"
            placeholder="搜索 ServiceAccount..."
            clearable
            @keyup.enter="handleSearch"
            @clear="handleSearch"
            style="width: 300px"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </div>
      <el-table :data="filteredData" style="width: 100%" v-loading="loading">
        <el-table-column
          fixed
          prop="name"
          label="名称"
          min-width="200"
        ></el-table-column>
        <el-table-column prop="namespace" label="命名空间" min-width="150">
          <template #default="scope">
            <el-tag type="primary" effect="plain" round size="small">
              {{ scope.row.namespace }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="类型" width="150">
          <template #default>
            <el-tag type="info" round>ServiceAccount</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Labels" min-width="200">
          <template #default="scope">
            <div v-if="hasLabels(scope.row)">
              <el-tag
                v-for="(value, key) in scope.row.labels"
                :key="key"
                round
                size="small"
                style="margin-right: 5px; margin-bottom: 5px"
              >
                {{ key }}={{ value }}
              </el-tag>
            </div>
            <span v-else class="no-data">-</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="creation_time"
          label="创建时间"
          width="200"
        ></el-table-column>
      </el-table>
      <div v-if="filteredData.length === 0 && !loading" class="empty-state">
        <el-empty description="暂无数据" />
      </div>
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next, jumper"
        prev-text="上一页"
        next-text="下一页"
        style="margin-top: 20px"
      ></el-pagination>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getAllSas } from '@/api/cluster'

defineOptions({
  name: 'SaView'
})

const loading = ref(false)
const serviceAccounts = ref([])
const searchQuery = ref('')

// 分页参数
const currentPage = ref(1)
const pageSize = ref(10)

const total = computed(() => filteredData.value.length)

// 过滤后的数据（支持搜索）
const filteredData = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) {
    return serviceAccounts.value.slice(
      (currentPage.value - 1) * pageSize.value,
      currentPage.value * pageSize.value
    )
  }

  return serviceAccounts.value
    .filter((item) => {
      const nameMatch = item.name?.toLowerCase().includes(query)
      const namespaceMatch = item.namespace?.toLowerCase().includes(query)
      const labelsMatch = item.labels
        ? Object.entries(item.labels).some(
            ([k, v]) =>
              k.toLowerCase().includes(query) ||
              v?.toLowerCase().includes(query)
          )
        : false
      return nameMatch || namespaceMatch || labelsMatch
    })
    .slice(
      (currentPage.value - 1) * pageSize.value,
      currentPage.value * pageSize.value
    )
})

// 获取全部 ServiceAccount 数据
const loadServiceAccounts = async () => {
  try {
    loading.value = true
    const res = await getAllSas()
    serviceAccounts.value = res.data || []
  } catch (error) {
    console.error('获取 ServiceAccount 数据失败:', error)
    ElMessage.error('获取数据失败')
    serviceAccounts.value = []
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
}

// 判断是否有 labels
const hasLabels = (row) => {
  return row.labels && Object.keys(row.labels).length > 0
}

onMounted(() => {
  loadServiceAccounts()
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
    color: #343a40;
  }
  .search-box {
    display: flex;
    align-items: center;
  }
}

.no-data {
  color: #c0c4cc;
  font-size: 13px;
}

.empty-state {
  margin-top: 20px;
}
</style>
