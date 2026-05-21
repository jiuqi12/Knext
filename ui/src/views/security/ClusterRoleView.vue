<template>
  <el-container>
    <el-main>
      <div class="header">
        <h2>ClusterRole</h2>
        <div class="search-box">
          <el-input
            v-model="searchQuery"
            placeholder="搜索 ClusterRole..."
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
        <el-table-column fixed prop="name" label="名称" min-width="250"></el-table-column>
        <el-table-column label="类型" width="150">
          <template v-slot="scope">
            <el-tag type="primary" round>{{ scope.row.type || 'Cluster' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="权限" min-width="400">
          <template v-slot="scope">
            <div v-if="scope.row.rules && scope.row.rules.length > 0">
              <el-tag
                v-for="(rule, index) in scope.row.rules.slice(0, 3)"
                :key="index"
                round
                style="margin-right: 5px; margin-bottom: 5px"
                size="small"
              >
                {{ rule.verbs?.join(', ') }}
              </el-tag>
              <el-tag v-if="scope.row.rules.length > 3" type="info" size="small">
                +{{ scope.row.rules.length - 3 }} 更多
              </el-tag>
            </div>
            <el-tag v-else type="danger">无权限规则</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="creation_time" label="创建时间" width="200"></el-table-column>
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

defineOptions({
  name: 'ClusterRoleView'
})

// 定义加载状态
const loading = ref(false)

// 定义数据
const clusterRoles = ref([])

// 搜索关键词
const searchQuery = ref('')

// 分页参数
const currentPage = ref(1)
const pageSize = ref(10)

// 计算总数
const total = computed(() => filteredData.value.length)

// 过滤后的数据（支持搜索）
const filteredData = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) {
    return clusterRoles.value.slice(
      (currentPage.value - 1) * pageSize.value,
      currentPage.value * pageSize.value
    )
  }
  
  return clusterRoles.value.filter(item => {
    const nameMatch = item.name?.toLowerCase().includes(query)
    const rulesMatch = item.rules?.some(rule => 
      rule.verbs?.some(verb => verb.toLowerCase().includes(query)) ||
      rule.apiGroups?.some(group => group.toLowerCase().includes(query)) ||
      rule.resources?.some(resource => resource.toLowerCase().includes(query))
    )
    return nameMatch || rulesMatch
  }).slice((currentPage.value - 1) * pageSize.value, currentPage.value * pageSize.value)
})

// 获取 ClusterRole 数据
const getClusterRoleData = async () => {
  try {
    loading.value = true
    // TODO: 替换为实际的 API 调用
    // const res = await getClusterRoles()
    // clusterRoles.value = res.data || []
    
    // 模拟数据
    clusterRoles.value = [
      {
        name: 'cluster-admin',
        type: 'Cluster',
        rules: [
          { verbs: ['*'], apiGroups: ['*'], resources: ['*'] },
          { verbs: ['*'], apiGroups: [''], resources: ['pods', 'services'] }
        ],
        creation_time: '2024-01-15T10:30:00Z'
      },
      {
        name: 'system:controller',
        type: 'Cluster',
        rules: [
          { verbs: ['get', 'list', 'watch'], apiGroups: [''], resources: ['pods'] },
          { verbs: ['create', 'update', 'patch'], apiGroups: [''], resources: ['events'] }
        ],
        creation_time: '2024-01-15T10:30:00Z'
      }
    ]
  } catch (error) {
    console.error('获取 ClusterRole 数据失败:', error)
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
}

// 组件挂载后获取数据
onMounted(() => {
  getClusterRoleData()
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

.empty-state {
  margin-top: 20px;
}
</style>
