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
      <h2>{{ featuredCourse?.title || '系统课程持续上新' }}</h2>
      <p>{{ featuredCourse ? `${featuredCourse.lessons} 节课 · ${featuredCourse.students.toLocaleString()} 人在学` : '等待后台审核发布课程' }}</p>
      <el-button text :disabled="!featuredCourse" @click="goFeaturedCourse">进入课程详情</el-button>
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
        <el-alert
          v-if="loadError"
          class="roomy"
          title="首页课程数据加载失败，请确认 Django 后端已启动。"
          type="error"
          show-icon
          :closable="false"
        />
        <div class="course-grid">
          <article v-for="course in freeCourses" :key="course.id" class="course-card" @click="router.push(`/courses/${course.id}`)">
            <div class="course-cover course-cover--image">
              <img v-if="course.coverUrl" :src="course.coverUrl" :alt="course.title" />
              <span v-else>{{ course.cover }}</span>
              <div class="course-cover__overlay">
                <strong>{{ course.title }}</strong>
              </div>
            </div>
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
        <el-empty v-if="!loading && !freeCourses.length" description="暂无已发布课程" />
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
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getCoursesApi } from '@/api/course'
import { categories, teachers } from '@/data/platform'

const router = useRouter()
const activeCategory = ref('frontend')
const backendCourses = ref([])
const loading = ref(false)
const loadError = ref(false)

onMounted(loadCourses)

const courses = computed(() => backendCourses.value.map((course) => ({
  id: course.id,
  title: course.title,
  category: course.category_detail?.slug || course.category_detail?.name || course.category,
  categoryText: course.category_detail?.name || '综合课程',
  teacher: course.teacher_detail?.real_name || '平台讲师',
  price: Number(course.price) > 0 ? `¥${Number(course.price).toFixed(0)}` : '免费',
  lessons: course.chapters?.length || 1,
  students: course.sales_count || 0,
  summary: course.description || course.subtitle || '课程已通过平台审核，更多介绍请进入详情页查看。',
  cover: (course.title || '课程').slice(0, 3).toUpperCase(),
  coverUrl: course.cover || course.cover_url || '',
  isFree: Number(course.price) <= 0 || course.is_free,
})))
const featuredCourse = computed(() => hotCourses.value[0] || courses.value[0] || null)
const freeCourses = computed(() => {
  const freeItems = courses.value.filter((course) => course.isFree)
  return (freeItems.length ? freeItems : courses.value).slice(0, 4)
})
const hotCourses = computed(() => [...courses.value].sort((a, b) => b.students - a.students).slice(0, 5))
const hotTeachers = computed(() => [...teachers].sort((a, b) => b.students - a.students).slice(0, 5))

function categoryName(id) {
  return categories.find((item) => item.id === id)?.name || courses.value.find((item) => item.category === id)?.categoryText || '综合课程'
}

function showCourseTip(course) {
  ElMessage.info(`《${course.title}》已有 ${course.students.toLocaleString()} 人学习`)
}

function goFeaturedCourse() {
  if (featuredCourse.value) {
    router.push(`/courses/${featuredCourse.value.id}`)
  }
}

async function loadCourses() {
  loading.value = true
  loadError.value = false
  try {
    backendCourses.value = await getCoursesApi()
  } catch {
    backendCourses.value = []
    loadError.value = true
  } finally {
    loading.value = false
  }
}
</script>
