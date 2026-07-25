<template>
  <section class="page-section">
    <div class="section-heading">
      <div>
        <p class="section-kicker">Courses</p>
        <h1>课程分类</h1>
        <p class="section-desc">通过分类、难度和价格筛选适合你的课程，当前为纯前端静态演示。</p>
      </div>
      <el-button type="primary" @click="previewVisible = true">试看提示</el-button>
    </div>

    <div class="filter-panel">
      <el-form :inline="true">
        <el-form-item label="分类">
          <el-select v-model="filters.category" placeholder="全部分类" clearable>
            <el-option v-for="item in categoryOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="filters.level" placeholder="全部难度" clearable>
            <el-option label="入门" value="入门" />
            <el-option label="进阶" value="进阶" />
            <el-option label="实战" value="实战" />
          </el-select>
        </el-form-item>
        <el-form-item label="价格">
          <el-radio-group v-model="filters.free">
            <el-radio-button label="">全部</el-radio-button>
            <el-radio-button label="1">免费</el-radio-button>
            <el-radio-button label="0">付费</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-input v-model="filters.keyword" placeholder="搜索课程名称" clearable />
        </el-form-item>
      </el-form>
    </div>

    <el-alert
      v-if="loadError"
      class="roomy"
      title="课程数据加载失败，请确认 Django 后端已启动。"
      type="error"
      show-icon
      :closable="false"
    />

    <div v-loading="loading" class="course-grid course-grid--list">
      <article v-for="course in pagedCourses" :key="course.id" class="course-card" @click="router.push(`/courses/${course.id}`)">
        <div class="course-cover">{{ course.cover }}</div>
        <div class="course-card__body">
          <div class="tag-row">
            <el-tag size="small" effect="plain">{{ categoryName(course.category) }}</el-tag>
            <el-tag size="small" :type="course.isFree ? 'success' : 'warning'" effect="plain">{{ course.price }}</el-tag>
          </div>
          <h3>{{ course.title }}</h3>
          <p>{{ course.summary }}</p>
          <div class="course-meta">
            <span>{{ course.teacher }}</span>
            <span>{{ course.lessons }} 节</span>
            <span>{{ course.students.toLocaleString() }} 人学习</span>
          </div>
        </div>
      </article>
    </div>

    <el-empty v-if="!loading && filteredCourses.length === 0" description="暂无已审核通过的课程" />

    <div class="pagination-bar">
      <el-pagination layout="prev, pager, next" :total="filteredCourses.length" :page-size="pageSize" v-model:current-page="currentPage" />
    </div>
  </section>

  <el-dialog v-model="previewVisible" title="试看提示" width="420px">
    <p>免费课程可直接进入播放页试看；付费课程当前仅展示详情页，后续可接入购买流程。</p>
    <template #footer>
      <el-button @click="previewVisible = false">知道了</el-button>
      <el-button type="primary" @click="goFreeCourses">查看免费课程</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCoursesApi } from '@/api/course'
import { categories } from '@/data/platform'

const route = useRoute()
const router = useRouter()
const pageSize = 4
const currentPage = ref(1)
const previewVisible = ref(false)
const loading = ref(false)
const loadError = ref(false)
const backendCourses = ref([])
const filters = reactive({
  category: '',
  level: '',
  free: '',
  keyword: '',
})

watchEffect(() => {
  filters.free = route.query.free === '1' ? '1' : ''
})

onMounted(loadCourses)

const courses = computed(() => backendCourses.value.map((course) => ({
  id: course.id,
  title: course.title,
  category: course.category_detail?.slug || course.category_detail?.name || course.category,
  categoryText: course.category_detail?.name || '综合课程',
  teacher: course.teacher_detail?.real_name || '平台讲师',
  level: levelLabel(course.level),
  price: Number(course.price) > 0 ? `¥${Number(course.price).toFixed(0)}` : '免费',
  lessons: course.chapters?.length || 1,
  students: course.sales_count || 0,
  summary: course.description || course.subtitle || '课程已通过平台审核，更多介绍请进入详情页查看。',
  cover: (course.title || '课程').slice(0, 3).toUpperCase(),
  isFree: Number(course.price) <= 0 || course.is_free,
})))

const categoryOptions = computed(() => {
  const options = categories.map((item) => ({ id: item.id, name: item.name }))
  backendCourses.value.forEach((course) => {
    const id = course.category_detail?.slug || course.category_detail?.name || course.category
    const name = course.category_detail?.name || '综合课程'
    if (id && !options.some((item) => item.id === id)) {
      options.push({ id, name })
    }
  })
  return options
})

const filteredCourses = computed(() => courses.value.filter((course) => {
  const matchesCategory = !filters.category || course.category === filters.category
  const matchesLevel = !filters.level || course.level === filters.level
  const matchesFree = filters.free === '' || String(Number(course.isFree)) === filters.free
  const matchesKeyword = !filters.keyword || course.title.includes(filters.keyword)
  return matchesCategory && matchesLevel && matchesFree && matchesKeyword
}))

const pagedCourses = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredCourses.value.slice(start, start + pageSize)
})

function categoryName(id) {
  return categories.find((item) => item.id === id)?.name || courses.value.find((item) => item.category === id)?.categoryText || '综合课程'
}

function goFreeCourses() {
  previewVisible.value = false
  router.push('/courses?free=1')
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

function levelLabel(level) {
  const labels = {
    beginner: '入门',
    intermediate: '进阶',
    advanced: '实战',
  }
  return labels[level] || level || '入门'
}
</script>
