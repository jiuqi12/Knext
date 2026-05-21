<template>
  <div class="table-container">
    <el-table :data="tableData" border stripe style="width: 100%">
      <el-table-column prop="name" label="名称" min-width="180" />
      <el-table-column prop="provisioner" label="存储驱动" min-width="150" />
      <el-table-column prop="reclaim_policy" label="回收策略" width="120" />
      <el-table-column prop="volume_binding_mode" label="卷绑定模式" min-width="150" />
      <el-table-column prop="allow_volume_expansion" label="允许扩容" width="100">
        <template #default="{ row }">
          <el-tag :type="row.allow_volume_expansion ? 'success' : 'info'">
            {{ row.allow_volume_expansion ? '是' : '否' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="parameters" label="配置参数" min-width="250">
        <template #default="{ row }">
          <span v-for="(value, key, index) in row.parameters" :key="key">
            {{ key }}: {{ value }}<span v-if="index < Object.keys(row.parameters).length - 1">, </span>
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="creation_time" label="创建时间" min-width="160" />
    </el-table>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const tableData = ref([])

// TODO: 填充数据获取方法
</script>

<style lang="scss" scoped>
.table-container {
  padding: 20px;
}
</style>
