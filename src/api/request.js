import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  timeout: 10000,
})

request.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()

    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }

    return config
  },
  (error) => Promise.reject(error),
)

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const status = error.response?.status
    const data = error.response?.data
    const isInvalidToken = status === 401 && String(data?.detail || '').includes('token')
    if (isInvalidToken) {
      const authStore = useAuthStore()
      authStore.logout()
      ElMessage.error('登录状态已过期，请重新登录')
      return Promise.reject(error)
    }

    const message = data?.message || data?.detail || Object.values(data || {})?.flat?.()?.[0] || error.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  },
)

export default request
