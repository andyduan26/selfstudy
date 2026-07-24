<template>
  <AdminPageHeader title="后台首页" desc="查看平台关键运营数据、审核事项与系统状态。" />
  <div class="admin-stats">
    <div v-for="item in adminStats" :key="item.label" class="admin-stat-card">
      <span>{{ item.label }}</span>
      <strong>{{ item.value }}</strong>
      <small>{{ item.desc }}</small>
    </div>
  </div>
  <div class="admin-grid">
    <section class="admin-panel">
      <h2>待处理事项</h2>
      <button v-for="item in todoItems" :key="item.label" class="admin-todo" @click="ElMessage.info(item.tip)">
        <span>{{ item.label }}</span>
        <strong>{{ item.count }}</strong>
      </button>
    </section>
    <section class="admin-panel">
      <h2>系统状态</h2>
      <div class="admin-info-line"><span>运行模式</span><strong>静态演示</strong></div>
      <div class="admin-info-line"><span>前端版本</span><strong>0.4.0</strong></div>
      <div class="admin-info-line"><span>接口状态</span><strong>未接入</strong></div>
    </section>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import AdminPageHeader from '@/components/admin/AdminPageHeader.vue'
import { adminStats } from '@/data/admin'

const todoItems = [
  { label: '讲师入驻审核', count: 18, tip: '可进入讲师审核页面处理' },
  { label: '作品内容审核', count: 42, tip: '可进入作品审核页面处理' },
  { label: '提现待审核', count: 9, tip: '可进入提现审核页面处理' },
]
</script>
