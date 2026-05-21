<template>
  <el-container>
    <el-main>
      <div class="header">
        <h2>Service 服务</h2>
      </div>

      <el-table
        :data="paginatedData"
        border
        stripe
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="name" label="名称" min-width="150" fixed />
        <el-table-column prop="namespace" label="命名空间" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.namespace }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="130" align="center">
          <template #default="{ row }">
            <el-tag :type="getTypeTag(row.type)">{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cluster_ip" label="集群 IP" min-width="140" />
        <el-table-column label="外部名称" min-width="150">
          <template #default="{ row }">
            {{ row.external_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="端口映射" min-width="200">
          <template #default="{ row }">
            <div
              v-for="(port, index) in row.ports"
              :key="index"
              class="port-item"
            >
              <el-tag size="small" type="info">{{ port }}</el-tag>
            </div>
            <span v-if="!row.ports || row.ports.length === 0">-</span>
          </template>
        </el-table-column>
        <el-table-column label="选择器" min-width="180">
          <template #default="{ row }">
            <template
              v-if="row.selector && Object.keys(row.selector).length > 0"
            >
              <el-tag
                v-for="(value, key) in row.selector"
                :key="key"
                size="small"
                class="selector-tag"
              >
                {{ key }}={{ value }}
              </el-tag>
            </template>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="creation_time"
          label="创建时间"
          min-width="160"
        />
      </el-table>

      <div v-if="!loading && tableData.length === 0" class="empty-state">
        <el-empty description="暂无数据" />
      </div>

      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next, jumper"
        prev-text="上一页"
        next-text="下一页"
        @current-change="handlePageChange"
      />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getService } from '@/api/cluster'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = computed(() => tableData.value.length)

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return tableData.value.slice(start, start + pageSize.value)
})

const handlePageChange = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 获取 Service 列表
const fetchServices = async () => {
  loading.value = true
  try {
    const res = await getService()
    tableData.value = res?.data || []
    currentPage.value = 1
  } catch {
    ElMessage.error('获取服务列表失败')
    tableData.value = []
  } finally {
    loading.value = false
  }
}

// 类型标签颜色
const getTypeTag = (type) => {
  const typeMap = {
    ClusterIP: 'info',
    NodePort: 'warning',
    LoadBalancer: 'success',
    ExternalName: 'danger'
  }
  return typeMap[type] || 'info'
}

onMounted(() => {
  fetchServices()
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
}

.port-item {
  display: inline-block;
  margin: 2px 4px 2px 0;
}

.selector-tag {
  margin: 2px 4px 2px 0;
}

.empty-state {
  padding: 40px 0;
}
</style>
