<template>
  <div class="login-page">
    <div class="main">
      <el-form
        :model="form"
        ref="loginFormRef"
        :rules="rules"
        @submit.prevent="handleSubmit"
      >
        <h1>登录</h1>
        <p>访问您的Kubernetes仪表盘</p>
        <p>默认用户名密码：admin/admin123</p>
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            prefix-icon="User"
            placeholder="请输入用户名"
            maxlength="12"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            prefix-icon="Lock"
            type="password"
            show-password
            placeholder="6-12位字母+数字组合"
            maxlength="12"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            class="!ml-0"
            :plain="true"
            type="primary"
            native-type="submit"
            :loading="isLoading"
            round
            >使用密码登录</el-button
          >
        </el-form-item>
        <p>忘记密码请联系管理员重置</p>
      </el-form>
    </div>
    <div class="footer">
      <div class="left">
        <span>@ 2026 Knext</span>
      </div>
      <div class="right">
        <a href="https://github.com/jiuqi12/Knext">Github</a>
      </div>
    </div>
  </div>
</template>

<script setup>
defineOptions({
  name: 'LoginIndex'
})
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const form = reactive({
  username: '',
  password: ''
})

// 表单校验
const loginFormRef = ref(null)

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

// 表单规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 5, max: 12, message: '请输入正确的用户名', trigger: 'blur' }
  ],
  password: [
    {
      validator: validatePassword,
      trigger: 'blur'
    }
  ]
}
const isLoading = ref(false)
// 提交表单
const userStore = useUserStore()
const handleSubmit = () => {
  loginFormRef.value?.validate(async (valid) => {
    try {
      isLoading.value = true
      if (valid) {
        isLoading.value = true
        await userStore.login(form)
      } else {
        ElMessage('请输入用户名和密码')
      }
    } finally {
      isLoading.value = false
    }
  })
}
</script>

<style lang="scss" scoped>
.login-page {
  background-image: url('@/assets/login.png');
  background-repeat: no-repeat;
  background-size: cover;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  .main {
    flex: 1;
    padding: 0px;
    display: flex;
    justify-content: center;
    align-items: center;
    .el-form {
      background-color: #fff;
      height: 400px;
      width: 400px;
      padding: 15px 30px;
      border: 1px solid #e4e4e7;
      border-radius: 15px;
      text-align: center;
      opacity: 0.8;
      h1 {
        line-height: 100px;
      }
      p {
        line-height: 30px;
      }
      .el-form-item {
        margin-top: 15px;
        .el-input {
          background-color: #fff;
        }
      }
      .el-button {
        margin-top: 15px;
        width: 100%;
      }
    }
  }
  .footer {
    background-color: #fff;
    color: #333;
    opacity: 0.8;
    text-align: center;
    line-height: 60px;
    height: 60px;
    display: flex;
    justify-content: space-evenly;
    padding: 0px 100px;
    border-top: 1px solid #e4e4e7;
    .left {
      margin-right: auto;
    }
    .right {
      margin-left: auto;
      a {
        text-decoration: none;
      }
    }
  }
}
</style>
