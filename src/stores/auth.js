import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

const TOKEN_KEY = 'woyaoxue_token'
const ROLE_KEY = 'woyaoxue_role'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || '')
  const role = ref(localStorage.getItem(ROLE_KEY) || 'user')

  const isLoggedIn = computed(() => Boolean(token.value))

  function login({ accessToken, userRole = 'user' }) {
    token.value = accessToken
    role.value = userRole
    localStorage.setItem(TOKEN_KEY, accessToken)
    localStorage.setItem(ROLE_KEY, userRole)
  }

  function logout() {
    token.value = ''
    role.value = 'user'
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(ROLE_KEY)
  }

  return {
    token,
    role,
    isLoggedIn,
    login,
    logout,
  }
})
