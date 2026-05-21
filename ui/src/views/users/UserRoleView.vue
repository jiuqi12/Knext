<template>
  <div class="user-role-info-container">
    <!-- 添加用户角色按钮 -->
    <div class="add-user">
      <el-button
        class="add-user-button"
        type="primary"
        @click="handleOpenCreate"
        >创建用户角色</el-button
      >
    </div>

    <!-- 用户角色信息卡片 -->
    <el-card class="user-info-card" header="用户角色信息">
      <el-table
        :data="userRoleDatas"
        width="100%"
        header-align="center"
        @cell-click="handleShowUser"
      >
        <el-table-column
          prop="user_role_id"
          label="ID"
          fixed
          width="120px"
          class="user-info-table"
          align="center"
        >
        </el-table-column>
        <el-table-column
          prop="user_role_name"
          label="角色名称"
          width="120px"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="user_role_sa"
          label="服务账号"
          width="200px"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="user_role_namespace"
          label="所属命名空间"
          width="120px"
          align="center"
        >
        </el-table-column>
        <el-table-column width="300" label="操作" fixed="right" align="center">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click.stop="handleUpdateInfo(scope.row)"
              >修改服务账号</el-button
            >
            <el-button
              type="danger"
              size="small"
              @click.stop="handleDeleteUserRole(scope.row)"
              >删除用户角色</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <!-- 添加用户角色表单 -->
    <el-dialog
      v-model="dialogVisible"
      title="创建用户角色"
      width="560px"
      class="user-add-dialog"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form
        ref="createUserRoleFormRef"
        :model="createUserRoleForm"
        label-width="100px"
      >
        <el-form-item label="用户角色名" prop="name">
          <el-input
            v-model="createUserRoleForm.name"
            placeholder="请输入用户角色名"
          />
        </el-form-item>
        <el-form-item label="命名空间">
          <el-select
            v-model="createUserRoleForm.namespace"
            placeholder="选择命名空间"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="role in saList"
              :key="role.user_role_id"
              :label="role.user_role_name"
              :value="role.user_role_id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="服务账号">
          <el-select
            v-model="createUserRoleForm.namespace"
            placeholder="选择服务账号"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="role in saList"
              :key="role.user_role_id"
              :label="role.user_role_name"
              :value="role.user_role_id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消创建</el-button>
          <el-button
            type="primary"
            @click="handleCreateUser"
            :loading="isLoading"
          >
            提交
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { listUserRoles, deleteUser, createUser } from '@/api/auth'
import { getAllSas } from '@/api/cluster'
import { ElMessage, ElMessageBox } from 'element-plus'

// 用户信息
const userRoleDatas = ref([])
const isLoading = ref(false)

// dialog状态
const dialogVisible = ref(false)

// 用户角色列表
const saList = ref([])

// 创建用户表单
const createUserRoleFormRef = ref(null)
const createUserRoleForm = ref({
  name: '',
  namespace: '',
  service_accounts: ''
})

// 获取当前系统的服务账号
const list_sa = async () => {
  try {
    const res = await getAllSas()
    saList.value = res.data || []
  } catch {
    saList.value = []
  }
}

// 打开创建对话框
const handleOpenCreate = () => {
  createUserRoleForm.value = {
    name: '',
    service_accounts: [],
    namespace: ''
  }
  saList.value = []
  dialogVisible.value = true
  list_sa()
}

// 提交创建用户角色
const handleCreateUser = async () => {
  if (!createUserRoleFormRef.value) return
  // 提交动作
  try {
    isLoading.value = true
    const res = await createUser(createUserRoleForm)
    if (res.code === 200) {
      ElMessage.success('用户创建成功')
      dialogVisible.value = false
      getUserRoleData()
    } else {
      ElMessage.error(res.detail || '创建失败')
    }
  } finally {
    isLoading.value = false
  }
}

// 获取用户角色信息
const getUserRoleData = async () => {
  try {
    isLoading.value = true
    const res = await listUserRoles()
    userRoleDatas.value = (res.data || []).map((user) => ({
      ...user,
      is_active: Boolean(user.is_active)
    }))
  } finally {
    isLoading.value = false
  }
}

// 删除用户角色
const handleDeleteUserRole = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户角色 "${row.username}" 吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
  } catch {
    return
  }

  try {
    const res = await deleteUser(row.user_id)
    if (res.code === 200) {
      ElMessage.success(`删除用户角色${res.data}成功`)
      getUserRoleData()
    } else {
      ElMessage.error(`删除用户角色${res.data}失败`)
    }
  } catch (err) {
    ElMessage.error(err.detail)
  }
}

onMounted(() => {
  getUserRoleData()
})
</script>

<style lang="scss" scoped>
.user-role-info-container {
  margin: 10px 10px;
  padding: 20px;
  .add-user {
    margin-bottom: 20px;
    text-align: right;
  }

  .user-info-card {
    width: 100%;

    .user-info-table {
      width: 100%;
      text-align: center;
    }
  }
  .user-add-dialog {
    padding: 15px;
  }
}

:deep(.el-dialog) {
  border-radius: 12px;
}

:deep(.el-dialog__header) {
  border-bottom: 1px solid #f0f0f0;
  padding: 16px 24px;
  margin: 0;
}

:deep(.el-dialog__body) {
  padding: 24px;
}

:deep(.el-dialog__footer) {
  border-top: 1px solid #f0f0f0;
  padding: 12px 24px;
}

:deep(.el-divider__text) {
  font-size: 13px;
  color: #909399;
  font-weight: 500;
}

// 禁用状态样式
.active-row {
  cursor: pointer;
}
.inactive-row {
  cursor: not-allowed;
  opacity: 0.6;
}

// 鼠标点击样式
.clickable-table :deep(.el-table__row) {
  cursor: pointer;
}
</style>
