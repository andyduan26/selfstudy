<template>
  <main class="login-page">
    <section class="login-panel">
      <p class="section-kicker">Account</p>
      <h1>登录演示</h1>
      <p class="section-desc">当前阶段只做前端架构，点击按钮会写入本地演示身份。</p>

      <el-form label-position="top" class="login-form">
        <el-form-item label="登录身份">
          <el-radio-group v-model="selectedRole">
            <el-radio-button label="user">普通用户</el-radio-button>
            <el-radio-button label="teacher">讲师</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-button type="primary" class="login-button" @click="handleLogin">进入系统</el-button>
      </el-form>
    </section>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const selectedRole = ref('user')

function handleLogin() {
  authStore.login({
    accessToken: 'demo-token',
    userRole: selectedRole.value,
  })

  router.push(route.query.redirect || '/')
}
</script>
