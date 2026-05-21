<template>
  <div class="user-info-container">
    <!-- 返回按钮 -->
    <el-button type="primary" plain @click="handleBack" class="back-button">
      <el-icon><ArrowLeft /></el-icon>
      返回列表
    </el-button>

    <!-- 用户信息卡片 -->
    <el-card class="user-info-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>用户信息</span>
        </div>
      </template>
      <el-form
        :model="userInfo"
        :rules="userInfoRules"
        ref="userInfoFormRef"
        label-width="120px"
        size="large"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="userInfo.username" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="员工ID" prop="user_id">
              <el-input v-model="userInfo.user_id" disabled />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="userInfo.name" placeholder="请输入姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="userInfo.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="角色" prop="is_admin">
              <el-tag :type="userInfo.is_admin ? 'primary' : 'info'">
                {{ userInfo.is_admin ? '管理员' : '普通用户' }}
              </el-tag>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="is_active">
              <el-tag :type="userInfo.is_active ? 'success' : 'danger'">
                {{ userInfo.is_active ? '正常' : '禁用' }}
              </el-tag>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="最后登录">
              <span>{{ userInfo.last_login_time || '暂无记录' }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="创建时间">
              <span>{{ userInfo.created_at || '暂无记录' }}</span>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button
            type="primary"
            @click="handleUpdateInfo"
            :loading="infoLoading"
          >
            保存修改
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 修改密码卡片 -->
    <el-card class="password-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>修改密码</span>
        </div>
      </template>

      <el-form
        :model="passwordForm"
        :rules="passwordRules"
        label-width="120px"
        size="large"
        ref="passwordFormRef"
      >
        <el-form-item label="当前密码" prop="oldPassword">
          <el-input
            v-model="passwordForm.oldPassword"
            type="password"
            show-password
            placeholder="请输入当前密码"
          />
        </el-form-item>

        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="passwordForm.newPassword"
            type="password"
            show-password
            placeholder="6-12 位字母 + 数字组合"
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            show-password
            placeholder="请再次输入新密码"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            @click="handleChangePassword"
            :loading="passwordLoading"
          >
            确认修改
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { getUserDetail, changePassword, createUser } from '@/api/auth'

const router = useRouter()
const route = useRoute()

// 加载状态
const infoLoading = ref(false)
const passwordLoading = ref(false)
const pageLoading = ref(false)

// 表单引用
const userInfoFormRef = ref(null)
const passwordFormRef = ref(null)

// 用户信息
const userInfo = ref({
  username: '',
  user_id: '',
  name: '',
  email: '',
  is_admin: false,
  is_active: true,
  last_login_time: '',
  created_at: ''
})

// 原始用户信息（用于重置）
const originalUserInfo = ref({})

// 密码修改表单
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 自定义验证器：确认密码
const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入新密码'))
  } else if (value !== passwordForm.value.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 自定义验证器：新密码格式
const validateNewPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入新密码'))
  } else if (value.length < 6 || value.length > 12) {
    callback(new Error('密码长度为6-12位'))
  } else if (!/(?=.*[a-zA-Z])(?=.*\d)/.test(value)) {
    callback(new Error('密码需包含字母和数字'))
  } else {
    callback()
  }
}

// 用户信息表单验证规则
const userInfoRules = reactive({
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度为2-20个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
})

// 密码表单验证规则
const passwordRules = reactive({
  oldPassword: [{ required: true, message: '请输入当前密码', trigger: 'blur' }],
  newPassword: [
    { required: true, validator: validateNewPassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
})

// 获取用户详情
const fetchUserDetail = async () => {
  const username = route.params.username
  if (!username) {
    ElMessage.error('缺少用户参数')
    router.push('/usermanagement')
    return
  }

  try {
    pageLoading.value = true
    const res = await getUserDetail(username)
    if (res.code === 200) {
      userInfo.value = res.data
      // 保存原始数据用于重置
      originalUserInfo.value = { ...res.data }
    } else {
      ElMessage.error(res.message || '获取用户详情失败')
    }
  } finally {
    pageLoading.value = false
  }
}

// 更新用户信息
const handleUpdateInfo = async () => {
  if (!userInfoFormRef.value) return

  try {
    await userInfoFormRef.value.validate()
    infoLoading.value = true

    const updateData = {
      name: userInfo.value.name,
      email: userInfo.value.email
    }

    const res = await createUser(userInfo.value.username, updateData)
    if (res.code === 200) {
      ElMessage.success('用户信息更新成功')
      // 更新原始数据
      originalUserInfo.value = { ...userInfo.value }
      // 重新获取用户信息
      await fetchUserDetail()
    } else {
      ElMessage.error(res.message || '更新失败')
    }
  } catch (error) {
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else if (error !== false) {
      // 表单验证失败时 error 为 false，不需要提示
      ElMessage.error('更新失败')
    }
  } finally {
    infoLoading.value = false
  }
}

// 重置表单
const handleReset = () => {
  // 恢复原始数据
  userInfo.value = { ...originalUserInfo.value }
  // 清除验证状态
  if (userInfoFormRef.value) {
    userInfoFormRef.value.clearValidate()
  }
  ElMessage.info('已重置表单')
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
    passwordLoading.value = true

    const res = await changePassword({
      username: userInfo.value.username,
      old_password: passwordForm.value.oldPassword,
      new_password: passwordForm.value.newPassword
    })

    if (res.code === 200) {
      ElMessage.success('密码修改成功')
      // 清空密码表单
      passwordForm.value = {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
      passwordFormRef.value.clearValidate()
    } else {
      ElMessage.error(res.message || '密码修改失败')
    }
  } catch (error) {
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else if (error !== false) {
      ElMessage.error('密码修改失败')
    }
  } finally {
    passwordLoading.value = false
  }
}

// 返回列表
const handleBack = () => {
  router.push('/usermanagement')
}

// 页面加载时获取用户信息
onMounted(() => {
  fetchUserDetail()
})
</script>

<style lang="scss" scoped>
.user-info-container {
  max-width: 1200px;
  margin: 10px;
  padding: 20px;

  .back-button {
    margin-bottom: 20px;
  }

  .user-info-card,
  .password-card {
    margin-bottom: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: bold;
      font-size: 16px;
    }
  }

  // 表单样式优化
  :deep(.el-form-item__label) {
    font-weight: 500;
  }

  :deep(.el-input.is-disabled .el-input__wrapper) {
    background-color: #f5f7fa;
  }

  // 标签样式
  .el-tag {
    min-width: 60px;
  }
}

// 响应式布局
@media (max-width: 768px) {
  .user-info-container {
    padding: 10px;

    .el-col {
      margin-bottom: 10px;
    }
  }
}
</style>
