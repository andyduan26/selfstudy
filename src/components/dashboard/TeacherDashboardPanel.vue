<template>
  <div class="center-panel">
    <div class="panel-heading">
      <div>
        <h2>数据看板</h2>
        <p>查看课程、学员、收益与评分的核心经营数据。</p>
      </div>
      <el-button type="primary" plain>导出报表</el-button>
    </div>

    <div class="stats-grid">
      <div v-for="item in teacherStats" :key="item.label" class="stat-card">
        <span>{{ item.label }}</span>
        <strong>{{ item.value }}</strong>
        <small>{{ item.desc }}</small>
      </div>
    </div>

    <div class="chart-card">
      <div class="chart-bars">
        <span v-for="bar in bars" :key="bar.label" :style="{ height: `${bar.value}%` }">
          <small>{{ bar.label }}</small>
        </span>
      </div>
      <p>近 6 个月播放趋势静态示意</p>
    </div>
  </div>
</template>

<script setup>
import { teacherStats } from '@/data/dashboard'

const bars = [
  { label: '2月', value: 42 },
  { label: '3月', value: 56 },
  { label: '4月', value: 48 },
  { label: '5月', value: 72 },
  { label: '6月', value: 64 },
  { label: '7月', value: 86 },
]
</script>
