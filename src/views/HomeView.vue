<template>
  <section class="learning-hero">
    <div>
      <p class="section-kicker">Knowledge Platform</p>
      <h1>从零开始，系统学习真正用得上的技能</h1>
      <p class="section-desc">精选前端、后端、办公效率、AI 工具与设计课程，用清晰路径帮助你稳步成长。</p>
      <div class="hero-actions">
        <el-button type="primary" size="large" @click="router.push('/courses')">查看全部课程</el-button>
        <el-button size="large" @click="router.push('/courses?free=1')">免费试看课程</el-button>
      </div>
    </div>
    <div class="hero-panel">
      <div class="hero-panel__top">
        <span>今日推荐</span>
        <el-tag effect="plain">零基础</el-tag>
      </div>
      <h2>Vue3 零基础入门到项目实战</h2>
      <p>48 节课 · 12 小时 · 12,860 人在学</p>
      <el-button text @click="router.push('/courses/1')">进入课程详情</el-button>
    </div>
  </section>

  <section class="page-section compact-section">
    <div class="section-heading">
      <div>
        <p class="section-kicker">Categories</p>
        <h2>全部分类导航</h2>
      </div>
      <el-button text @click="router.push('/courses')">全部课程</el-button>
    </div>
    <div class="category-grid">
      <button
        v-for="item in categories"
        :key="item.id"
        class="category-card"
        :class="{ 'is-active': activeCategory === item.id }"
        @click="activeCategory = item.id"
      >
        <span>{{ item.name }}</span>
        <strong>{{ item.count }} 门课程</strong>
        <small>{{ item.desc }}</small>
      </button>
    </div>
  </section>

  <section class="page-section home-grid-section">
    <div class="content-grid">
      <div>
        <div class="section-heading">
          <div>
            <p class="section-kicker">Free Courses</p>
            <h2>免费课程区</h2>
          </div>
          <el-button text @click="router.push('/courses?free=1')">查看更多</el-button>
        </div>
        <div class="course-grid">
          <article v-for="course in freeCourses" :key="course.id" class="course-card" @click="router.push(`/courses/${course.id}`)">
            <div class="course-cover">{{ course.cover }}</div>
            <div class="course-card__body">
              <el-tag size="small" effect="plain">{{ categoryName(course.category) }}</el-tag>
              <h3>{{ course.title }}</h3>
              <p>{{ course.summary }}</p>
              <div class="course-meta">
                <span>{{ course.teacher }}</span>
                <span>{{ course.students.toLocaleString() }} 人学过</span>
              </div>
            </div>
          </article>
        </div>
      </div>

      <aside class="ranking-column">
        <div class="ranking-panel">
          <div class="section-heading small">
            <h2>热门课程榜单</h2>
          </div>
          <button v-for="(course, index) in hotCourses" :key="course.id" class="ranking-item" @click="showCourseTip(course)">
            <strong>{{ index + 1 }}</strong>
            <span>{{ course.title }}</span>
            <small>{{ course.students.toLocaleString() }} 人</small>
          </button>
        </div>
        <div class="ranking-panel">
          <div class="section-heading small">
            <h2>热门讲师榜单</h2>
          </div>
          <button v-for="(teacher, index) in hotTeachers" :key="teacher.id" class="teacher-rank" @click="router.push(`/teachers/${teacher.id}`)">
            <strong>{{ index + 1 }}</strong>
            <span>{{ teacher.name }}</span>
            <small>{{ teacher.field }}</small>
          </button>
        </div>
      </aside>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { categories, courses, teachers } from '@/data/platform'

const router = useRouter()
const activeCategory = ref('frontend')

const freeCourses = computed(() => courses.filter((course) => course.isFree).slice(0, 4))
const hotCourses = computed(() => [...courses].sort((a, b) => b.students - a.students).slice(0, 5))
const hotTeachers = computed(() => [...teachers].sort((a, b) => b.students - a.students).slice(0, 5))

function categoryName(id) {
  return categories.find((item) => item.id === id)?.name || '综合课程'
}

function showCourseTip(course) {
  ElMessage.info(`《${course.title}》已有 ${course.students.toLocaleString()} 人学习`)
}
</script>
