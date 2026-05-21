<template>
  <div class="table-container">
    <el-table :data="tableData" border stripe style="width: 100%">
      <el-table-column prop="name" label="名称" min-width="180" />
      <el-table-column prop="namespace" label="命名空间" min-width="120" />
      <el-table-column
        prop="desired_number_scheduled"
        label="期望调度"
        width="100"
      />
      <el-table-column
        prop="current_number_scheduled"
        label="当前调度"
        width="100"
      />
      <el-table-column prop="number_ready" label="就绪节点" min-width="150">
        <template #default="{ row }">
          <el-progress
            :percentage="
              getProgress(row.number_ready, row.desired_number_scheduled)
            "
            :status="
              row.number_ready === row.desired_number_scheduled ? 'success' : ''
            "
          />
        </template>
      </el-table-column>
      <el-table-column
        prop="updated_number_scheduled"
        label="已更新"
        width="100"
      />
      <el-table-column prop="image" label="镜像" min-width="200" />
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
