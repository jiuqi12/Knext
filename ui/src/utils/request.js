import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api/v1',
  timeout: 5000
})

request.interceptors.request.use(
  (config) => {
    const access_token = localStorage.getItem('access_token')
    if (access_token) {
      config.headers['Authorization'] = `Bearer ${access_token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

request.interceptors.response.use(
  (response) => {
    const res = response.data
    // 后端统一返回 { code, msg, data }，通过 code 判断业务状态
    if (res.code === 200) {
      return res
    }
    // 401 跳转登录
    if (res.code === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_info')
      ElMessage.error(res.msg || '登录已失效，请重新登录')
      window.location.href = '/login'
      return Promise.reject(res)
    }
    ElMessage.error(res.msg || res.detail || '请求失败')
    return Promise.reject(res)
  },
  (error) => {
    // HTTP 层面的错误（网络断开、超时、服务器无响应等）
    const status = error.response?.status
    const detail = error.response?.data?.detail || error.response?.data?.msg

    if (status === 401) {
      localStorage.removeItem('access_token')
      ElMessage.error('登录已失效，请重新登录')
      window.location.href = '/login'
    } else if (status === 403) {
      ElMessage.error(detail || '无权访问')
    } else if (status === 400) {
      ElMessage.error(detail || '请求参数错误')
    } else if (status === 404) {
      ElMessage.error(detail || '资源不存在')
    } else if (status === 409) {
      ElMessage.error(detail || '资源冲突，可能已存在')
    } else if (status === 422) {
      ElMessage.error(detail || '数据验证失败')
    } else if (status >= 500) {
      ElMessage.error(detail || '服务器内部错误')
    } else {
      ElMessage.error(detail || '网络连接失败')
    }
    return Promise.reject(error)
  }
)

export default request
