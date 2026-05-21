<template>
  <div class="table-container">
    <el-table :data="tableData" border stripe style="width: 100%">
      <el-table-column prop="name" label="名称" min-width="150" />
      <el-table-column prop="namespace" label="命名空间" min-width="120" />
      <el-table-column prop="class" label="Ingress 控制器" min-width="120" />
      <el-table-column prop="hosts" label="域名列表" min-width="200">
        <template #default="{ row }">
          <span v-for="(host, index) in row.hosts" :key="index">
            {{ host }}<span v-if="index < row.hosts.length - 1">, </span>
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="address" label="外部访问地址" min-width="150" />
      <el-table-column prop="tls" label="TLS" width="80">
        <template #default="{ row }">
          <el-tag :type="row.tls ? 'success' : 'info'">
            {{ row.tls ? '已启用' : '未启用' }}
          </el-tag>
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
