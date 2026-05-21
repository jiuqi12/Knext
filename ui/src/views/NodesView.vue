<template>
  <el-container>
    <el-main>
      <div class="header">
        <h2>Nodes</h2>
      </div>
      <el-table :data="nodes" style="width: 100%">
        <el-table-column fixed prop="name" label="名称"></el-table-column>
        <el-table-column label="状态">
          <template v-slot="scope">
            <el-tag type="success">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
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
        <el-table-column label="版本" width="100">
          <template v-slot="scope">
            <el-tag type="success" round>{{ scope.row.version }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="runtime"
          label="容器运行时"
          width="150"
        ></el-table-column>
        <el-table-column
          prop="internal_ip"
          label="IP地址"
          width="150"
        ></el-table-column>
        <el-table-column
          prop="os"
          label="操作系统"
          width="200"
        ></el-table-column>
        <el-table-column prop="cpu" label="CPU" width="100"></el-table-column>
        <el-table-column label="内存" width="100">
          <template v-slot="scope">
            <!-- {{ (scope.row.memory / 1024 / 1024).toFixed(2) }} GB -->
            {{ scope.row.memory }}
          </template>
        </el-table-column>
        <el-table-column prop="pods" label="Pods" width="100"></el-table-column>
        <el-table-column
          prop="creation_time"
          label="创建时间"
          width="200"
        ></el-table-column>
      </el-table>
      <div v-if="total === 0" class="empty-state">
        <el-empty description="暂无数据"></el-empty>
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
import { ref, onMounted } from 'vue'
import { getNodes } from '@/api/cluster'

// 声明节点数据
const nodes = ref([])
const total = ref(0)

// 声明分页数据
const currentPage = ref(1)
const pageSize = ref(10)

// 获取节点数据
const getNodeData = async () => {
  const res = await getNodes()
  nodes.value = res.data || []
  console.log(res.data)
  total.value = nodes.value.length
}

getNodeData()

onMounted(() => {})
</script>

<style lang="scss" scoped>
.header {
  height: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  h2 {
    margin: 0px;
  }
}
</style>
