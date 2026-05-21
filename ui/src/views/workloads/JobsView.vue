<template>
  <div class="table-container">
    <el-table :data="tableData" border stripe style="width: 100%">
      <el-table-column prop="name" label="名称" min-width="180" />
      <el-table-column prop="namespace" label="命名空间" min-width="120" />
      <el-table-column prop="status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusTag(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="completions" label="完成次数" width="100" />
      <el-table-column prop="parallelism" label="并行度" width="100" />
      <el-table-column prop="start_time" label="开始时间" min-width="160" />
      <el-table-column prop="completion_time" label="完成时间" min-width="160" />
      <el-table-column prop="image" label="镜像" min-width="200" />
      <el-table-column prop="command" label="命令" min-width="200" />
      <el-table-column label="Pod 统计" min-width="200">
        <template #default="{ row }">
          <span>活跃：{{ row.active_pods }}</span>
          <span style="margin: 0 8px">|</span>
          <span style="color: green">成功：{{ row.successful_pods }}</span>
          <span style="margin: 0 8px">|</span>
          <span style="color: red">失败：{{ row.failed_pods }}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const tableData = ref([])

const getStatusTag = (status) => {
  const statusMap = {
    Running: 'warning',
    Complete: 'success',
    Failed: 'danger'
  }
  return statusMap[status] || 'info'
}

// TODO: 填充数据获取方法
</script>

<style lang="scss" scoped>
.table-container {
  padding: 20px;
}
</style>
