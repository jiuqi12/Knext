<template>
  <div class="user-info-container">
    <!-- 添加用户按钮 -->
    <div class="add-user">
      <el-button
        class="add-user-button"
        type="primary"
        @click="handleOpenCreate"
        >创建用户</el-button
      >
    </div>

    <!-- 用户信息卡片 -->
    <el-card class="user-info-card" header="用户信息">
      <el-table
        :data="userDatas"
        :row-class-name="tableRowClassName"
        width="100%"
        header-align="center"
        @cell-click="handleShowUser"
      >
        <el-table-column
          prop="username"
          label="用户名"
          fixed
          width="120px"
          class="user-info-table"
          align="center"
        >
        </el-table-column>
        <el-table-column
          prop="user_id"
          label="员工ID"
          width="120px"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="email"
          label="邮箱"
          width="200px"
          align="center"
        ></el-table-column>
        <el-table-column label="是否启用账号" align="center">
          <template #default="scope">
            <div @click.stop>
              <el-switch
                v-model="scope.row.is_active"
                active-color="#13ce66"
                inactive-color="#ff4949"
                @change="handlechangeUser(scope.row.user_id)"
              ></el-switch>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="is_admin"
          label="角色"
          width="120px"
          align="center"
        >
          <template #default="scope">
            <el-tag v-if="scope.row.is_admin" type="primary">管理员</el-tag>
            <el-tag v-else type="info">普通用户</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="last_login_time"
          label="最近登录时间"
          width="200px"
          align="center"
        >
          <template #default="scope">
            <span @click.stop>{{ scope.row.last_login_time }}</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="创建时间"
          width="140px"
          align="center"
        >
          <template #default="scope">
            <span @click.stop>{{ scope.row.created_at }}</span>
          </template>
        </el-table-column>
        <el-table-column width="300" label="操作" fixed="right" align="center">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click.stop="handleUpdateInfo(scope.row)"
              >修改密码</el-button
            >
            <el-button
              type="danger"
              size="small"
              @click.stop="handleDeleteUser(scope.row)"
              >删除用户</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <!-- 添加用户表单 -->
    <el-dialog
      v-model="dialogVisible"
      title="创建用户"
      width="560px"
      class="user-add-dialog"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form
        ref="createUserFormRef"
        :model="createUserForm"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="createUserForm.username"
            placeholder="请输入用户名"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="createUserForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="createUserForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="createUserForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="管理员">
          <el-switch
            v-model="createUserForm.is_admin"
            active-text="是"
            inactive-text="否"
          />
        </el-form-item>
        <el-form-item label="角色">
          <el-select
            v-model="createUserForm.user_role_id"
            placeholder="选择用户角色"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="role in userRoleList"
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
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { listUsers, deleteUser, changeUser, createUser } from '@/api/auth'
import { listUserRoles } from '@/api/auth'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

// 用户信息
const userDatas = ref([])
const isLoading = ref(false)

// dialog状态
const dialogVisible = ref(false)

// 用户角色列表
const userRoleList = ref([])

// 为不同状态的行添加不同的状态
const tableRowClassName = (row) => {
  return row.is_active !== 0 ? 'active-row' : 'inactive-row'
}

// 创建用户表单
const createUserFormRef = ref(null)
const createUserForm = ref({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  is_admin: false,
  user_role_id: ''
})

// 获取当前系统的角色
const list_role = async () => {
  try {
    const res = await listUserRoles()
    userRoleList.value = res.data || []
  } catch {
    userRoleList.value = []
  }
}

// 密码校验规则
const validatePassword = (rule, value, callbacak) => {
  if (!value) {
    callbacak(new Error('请输入密码'))
    return
  }
  if (
    !/^(?=.*[a-zA-Z])(?=.*\d)/.test(value) ||
    value.length < 5 ||
    value.length > 12
  ) {
    callbacak(new Error('密码只能包含字母和数字,并且是5-12位'))
    return
  }
  callbacak()
}

// 表单验证规则
const formRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 5, max: 12, message: '用户名长度为 5-12 个字符', trigger: 'blur' }
  ],
  password: [{ validator: validatePassword, trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== createUserForm.value.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

// 打开创建对话框
const handleOpenCreate = () => {
  createUserForm.value = {
    username: '',
    password: '',
    confirmPassword: '',
    email: '',
    is_admin: false,
    user_role_id: ''
  }
  userRoleList.value = []
  dialogVisible.value = true
  list_role()
}

// 提交创建用户
const handleCreateUser = async () => {
  if (!createUserFormRef.value) return
  try {
    await createUserFormRef.value.validate()
  } catch {
    return
  }

  try {
    isLoading.value = true
    const { confirmPassword, ...submitData } = createUserForm.value
    const res = await createUser(submitData)
    if (res.code === 200) {
      ElMessage.success('用户创建成功')
      dialogVisible.value = false
      getUserData()
    } else {
      ElMessage.error(res.detail || '创建失败')
    }
  } finally {
    isLoading.value = false
  }
}

// 获取用户信息
const getUserData = async () => {
  try {
    isLoading.value = true
    const res = await listUsers()
    userDatas.value = (res.data || []).map((user) => ({
      ...user,
      is_active: Boolean(user.is_active)
    }))
  } catch (err) {
    console.error('获取用户列表失败:', err)
    ElMessage.error('获取用户列表失败')
    userDatas.value = []
  } finally {
    isLoading.value = false
  }
}

// 查看用户详细信息
const handleShowUser = (row, column) => {
  if (column.property === 'username') {
    if (row.is_active !== 0) {
      router.push('/userdetail/' + row.username)
    } else {
      ElMessage.error('用户已禁用')
    }
  }
}

// 删除用户
const handleDeleteUser = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${row.username}" 吗？此操作不可恢复。`,
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
      ElMessage.success(`删除用户${res.data}成功`)
      getUserData()
    } else {
      ElMessage.error(`删除用户${res.data}失败`)
    }
  } catch (err) {
    ElMessage.error(err.detail)
  }
}

// 修改用户状态
const handlechangeUser = async (user_id) => {
  try {
    const res = await changeUser(user_id)
    if (res.code === 200) {
      getUserData()
      ElMessage.success(`切换用户${res.data}状态成功`)
    } else {
      ElMessage.error(`切换用户${res.data}失败`)
    }
  } catch (err) {
    ElMessage.error(err.message)
  }
}

onMounted(() => {
  getUserData()
})
</script>

<style lang="scss" scoped>
.user-info-container {
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
