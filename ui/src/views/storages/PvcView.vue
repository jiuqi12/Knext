<template>
  <div class="table-container">
    <el-table :data="tableData" border stripe style="width: 100%">
      <el-table-column prop="name" label="名称" min-width="180" />
      <el-table-column prop="namespace" label="命名空间" min-width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusTag(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="access_modes" label="访问模式" min-width="200">
        <template #default="{ row }">
          <span v-for="(mode, index) in row.access_modes" :key="index">
            {{ mode }}<span v-if="index < row.access_modes.length - 1">, </span>
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="storage_class" label="存储类" min-width="150" />
      <el-table-column prop="capacity" label="请求容量" width="120">
        <template #default="{ row }">
          {{ row.capacity?.storage || '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="volume" label="绑定 PV" min-width="180" />
      <el-table-column prop="creation_time" label="创建时间" min-width="160" />
    </el-table>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const tableData = ref([])

const getStatusTag = (status) => {
  const statusMap = {
    Pending: 'warning',
    Bound: 'success',
    Lost: 'danger'
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
