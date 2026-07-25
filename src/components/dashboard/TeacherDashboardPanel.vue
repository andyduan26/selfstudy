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

    <div class="teacher-dashboard-grid">
      <section class="dashboard-block dashboard-block--wide">
        <div class="section-heading small">
          <h2>我的作品</h2>
          <el-tag effect="plain">按更新时间排序</el-tag>
        </div>
        <div v-loading="loading" class="work-strip">
          <article v-for="work in works" :key="work.id" class="work-card">
            <div>
              <el-tag :type="courseStatusType(work.status)" effect="plain">{{ courseStatusLabel(work.status) }}</el-tag>
              <h3>{{ work.title }}</h3>
            </div>
            <div class="work-card__meta">
              <span>{{ work.students.toLocaleString() }} 学员</span>
              <strong>{{ work.priceText }}</strong>
              <small>{{ work.updatedAt }} 更新</small>
            </div>
          </article>
          <el-empty v-if="!loading && works.length === 0" description="暂无课程作品" />
        </div>
      </section>

      <section class="dashboard-block">
        <div class="section-heading small">
          <h2>用户评价</h2>
          <el-tag type="success" effect="plain">近 7 天</el-tag>
        </div>
        <div class="review-list">
          <article v-for="review in teacherReviews" :key="review.id" class="review-card">
            <div class="review-card__top">
              <strong>{{ review.user }}</strong>
              <span>{{ review.rating }}</span>
            </div>
            <p>{{ review.content }}</p>
            <small>{{ review.course }} · {{ review.date }}</small>
          </article>
        </div>
      </section>

      <section class="dashboard-block">
        <div class="section-heading small">
          <h2>待办事项</h2>
          <el-tag type="warning" effect="plain">需要关注</el-tag>
        </div>
        <div class="todo-list">
          <button v-for="todo in teacherTodos" :key="todo.id" type="button" class="todo-card">
            <span>{{ todo.title }}</span>
            <strong>{{ todo.value }}</strong>
            <small>{{ todo.desc }}</small>
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { getTeacherWorksApi } from '@/api/teacher'
import { teacherReviews, teacherStats, teacherTodos } from '@/data/dashboard'
import { courseStatusLabel, courseStatusType, formatCourseWork } from '@/utils/courseFormat'

const loading = ref(false)
const rawWorks = ref([])
const works = computed(() => rawWorks.value.map(formatCourseWork))

const bars = [
  { label: '2月', value: 42 },
  { label: '3月', value: 56 },
  { label: '4月', value: 48 },
  { label: '5月', value: 72 },
  { label: '6月', value: 64 },
  { label: '7月', value: 86 },
]

onMounted(loadWorks)

async function loadWorks() {
  loading.value = true
  try {
    rawWorks.value = await getTeacherWorksApi()
  } finally {
    loading.value = false
  }
}
</script>
