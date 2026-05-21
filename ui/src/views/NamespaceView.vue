<template>
  <el-container>
    <el-main>
      <div class="header">
        <h2>Namespace</h2>
      </div>
      <el-table :data="namespaces" style="width: 100%">
        <el-table-column fixed prop="name" label="名称"></el-table-column>
        <el-table-column
          prop="creation_time"
          label="创建时间"
        ></el-table-column>
        <el-table-column label="标签" width="400">
          <template v-slot="scope">
            <el-tag
              v-for="(value, key, index) in scope.row.labels"
              :key="index"
              round
              >{{ key }}: {{ value }}</el-tag
            >
          </template>
        </el-table-column>
        <el-table-column prop="annotations" label="注解">
          <template v-slot="scope">
            <template v-if="scope.row.annotations !== null">
              <el-tag
                v-for="(value, key, index) in scope.row.annotations"
                :key="index"
                round
                >{{ key }}: {{ value }}</el-tag
              >
            </template>
            <template v-else>
              <el-tag type="danger">暂无注解</el-tag>
            </template>
          </template>
        </el-table-column>
        <el-table-column label="状态">
          <template v-slot="scope">
            <el-tag v-if="scope.row.status === 'Active'" type="success">{{
              scope.row.status
            }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="删除">
          <template v-slot="scope">
            <el-button type="danger" @click="handleDelete(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <div v-if="namespaces.length === 0" class="empty-state">
        <el-empty description="暂无数据" />
      </div>
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next, jumper"
        prev-text="上一页"
        next-text="下一页"
      ></el-pagination>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

defineOptions({
  name: 'ResourcesView'
})
import { getNamespaces, deleteNamespace } from '@/api/cluster'
import { ElMessage } from 'element-plus'

// 定义加载状态
const loading = ref(false)

// 定义数据
const namespaces = ref([])
// 获取命名空间数据
const getNamespaceData = async () => {
  try {
    loading.value = true
    const res = await getNamespaces()
    namespaces.value = res.data || []
  } finally {
    loading.value = false
  }
}
// 删除命名空间
const handleDelete = async (row) => {
  ElMessageBox.confirm(`确定要删除命名空间 "${row.name}" 吗？`, {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteNamespace(row.name)
        ElMessage.success('删除成功，异步操作中...请稍后刷新页面')
        await getNamespaceData()
      } catch {
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {
      ElMessage.error('取消删除')
    })
}

// 组件挂载之后获取数据
onMounted(() => {
  getNamespaceData()
})

// 分页参数
const currentPage = ref(1)
const pageSize = ref(10)
const total = computed(() => namespaces.value.length)
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
</style>
