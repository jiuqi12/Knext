<template>
  <div class="table-container">
    <el-table :data="tableData" border stripe style="width: 100%">
      <el-table-column prop="name" label="名称" min-width="180" />
      <el-table-column prop="namespace" label="命名空间" min-width="120" />
      <el-table-column prop="replicas" label="期望副本" width="100" />
      <el-table-column prop="ready_replicas" label="就绪副本" min-width="150">
        <template #default="{ row }">
          <el-progress 
            :percentage="getProgress(row.ready_replicas, row.replicas)"
            :status="row.ready_replicas === row.replicas ? 'success' : ''"
          />
        </template>
      </el-table-column>
      <el-table-column prop="current_replicas" label="当前副本" width="100" />
      <el-table-column prop="updated_replicas" label="已更新" width="100" />
      <el-table-column prop="image" label="镜像" min-width="200" />
      <el-table-column prop="service_name" label="关联服务" min-width="150" />
      <el-table-column prop="created_at" label="创建时间" min-width="160" />
    </el-table>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const tableData = ref([])

const getProgress = (current, total) => {
  return total ? Math.round((current / total) * 100) : 0
}

// TODO: 填充数据获取方法
</script>

<style lang="scss" scoped>
.table-container {
  padding: 20px;
}
</style>
