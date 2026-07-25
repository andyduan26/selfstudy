import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

const TOKEN_KEY = 'woyaoxue_token'
const ROLE_KEY = 'woyaoxue_role'
const USER_KEY = 'woyaoxue_user'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || '')
  const role = ref(localStorage.getItem(ROLE_KEY) || 'user')
  const user = ref(JSON.parse(localStorage.getItem(USER_KEY) || 'null'))

  const isLoggedIn = computed(() => Boolean(token.value))

  function login({ accessToken, userRole = 'user', userInfo = null }) {
    token.value = accessToken
    role.value = userRole
    if (userInfo) {
      user.value = userInfo
      localStorage.setItem(USER_KEY, JSON.stringify(userInfo))
    }
    localStorage.setItem(TOKEN_KEY, accessToken)
    localStorage.setItem(ROLE_KEY, userRole)
  }

  function updateUser(userInfo) {
    user.value = userInfo
    role.value = userInfo?.role || role.value
    localStorage.setItem(USER_KEY, JSON.stringify(userInfo))
    localStorage.setItem(ROLE_KEY, role.value)
  }

  function logout() {
    token.value = ''
    role.value = 'user'
    user.value = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(ROLE_KEY)
    localStorage.removeItem(USER_KEY)
  }

  return {
    token,
    role,
    user,
    isLoggedIn,
    login,
    updateUser,
    logout,
  }
})
