<template>
  <header class="app-header">
    <div class="app-header__inner">
      <RouterLink class="app-header__brand" to="/">我要自学网</RouterLink>

      <nav class="app-header__nav">
        <RouterLink to="/">首页</RouterLink>
        <RouterLink to="/courses">全部课程</RouterLink>
        <RouterLink to="/courses?free=1">免费课程</RouterLink>
        <RouterLink to="/teachers/1">讲师主页</RouterLink>
        <RouterLink to="/user">个人中心</RouterLink>
      </nav>

      <div class="app-header__actions">
        <el-tag v-if="authStore.isLoggedIn" effect="plain" type="info">
          {{ roleLabel }}
        </el-tag>
        <el-button v-if="authStore.isLoggedIn" text @click="authStore.logout()">退出</el-button>
        <el-button v-else type="primary" plain @click="router.push('/login')">登录</el-button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const roleLabel = computed(() => (authStore.role === 'teacher' ? '讲师' : '普通用户'))
</script>
