import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userLogin } from '@/api/auth'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

export const useUserStore = defineStore('user', () => {
  const router = useRouter()
  // 存储用户信息
  const access_token = ref(localStorage.getItem('access_token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('user_info') || '{}'))

  // 登录状态
  const isLogin = computed(() => {
    return access_token.value !== ''
  })

  // 是否是管理员
  const isAdmin = computed(() => {
    return userInfo.value?.is_admin
  })

  // 登录请求
  const login = async (data) => {
    try {
      // 发送请求
      const res = await userLogin(data)
      if (res.code === 200) {
        // 登录成功，存储token，路由跳转
        access_token.value = res.data.access_token
        localStorage.setItem('access_token', access_token.value)
        userInfo.value = res?.data.user || {}
        localStorage.setItem('user_info', JSON.stringify(res.data.user))
        // 使用replace而不是push，避免历史记录问题
        router.replace('/')
        ElMessage({
          message: '登录成功',
          type: 'success'
        })
        return res
      }
    } catch (error) {
      console.log(error)
    }
  }

  // 退出登录请求
  const logout = () => {
    access_token.value = ''
    localStorage.removeItem('access_token')
    userInfo.value = ''
    localStorage.removeItem('user_info')
  }
  return { access_token, userInfo, isLogin, login, logout, isAdmin }
})
