<template>
  <div class="admin-layout">
    <aside class="admin-sidebar">
      <RouterLink class="admin-brand" to="/admin">我要自学网后台</RouterLink>
      <nav class="admin-nav">
        <RouterLink v-for="item in menus" :key="item.path" :to="item.path">
          <component :is="item.icon" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>
    </aside>
    <div class="admin-main">
      <header class="admin-topbar">
        <div>
          <strong>管理员控制台</strong>
          <span>纯前端静态后台演示</span>
        </div>
        <el-button text @click="$router.push('/')">返回前台</el-button>
      </header>
      <main class="admin-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { DataBoard, Money, Operation, Setting, Tickets, User, UserFilled } from '@element-plus/icons-vue'

const menus = [
  { path: '/admin', label: '后台首页', icon: DataBoard },
  { path: '/admin/users', label: '用户管理', icon: User },
  { path: '/admin/teachers', label: '讲师审核', icon: UserFilled },
  { path: '/admin/works', label: '作品审核', icon: Tickets },
  { path: '/admin/orders', label: '订单管理', icon: Operation },
  { path: '/admin/withdraws', label: '提现审核', icon: Money },
  { path: '/admin/settings', label: '系统配置', icon: Setting },
]
</script>
