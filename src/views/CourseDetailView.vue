<template>
  <section v-if="loading" class="page-section">
    <el-skeleton :rows="8" animated />
  </section>

  <section v-else-if="course" class="page-section detail-layout">
    <div>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/courses' }">课程</el-breadcrumb-item>
        <el-breadcrumb-item>{{ course.title }}</el-breadcrumb-item>
      </el-breadcrumb>

      <div class="detail-hero">
        <div class="course-cover large">{{ course.cover }}</div>
        <div>
          <p class="section-kicker">{{ categoryName(course.category) }}</p>
          <h1>{{ course.title }}</h1>
          <p class="section-desc">{{ course.summary }}</p>
          <div class="tag-row roomy">
            <el-tag effect="plain">{{ course.level }}</el-tag>
            <el-tag effect="plain">{{ course.duration }}</el-tag>
            <el-tag :type="course.isFree ? 'success' : 'warning'" effect="plain">{{ course.price }}</el-tag>
          </div>
          <div class="hero-actions">
            <el-button type="primary" size="large" @click="handlePreview">立即试看</el-button>
            <el-button size="large" @click="dialogVisible = true">加入学习计划</el-button>
          </div>
        </div>
      </div>

      <el-tabs class="detail-tabs">
        <el-tab-pane label="课程介绍">
          <p>{{ course.summary }} 课程采用循序渐进的方式讲解，适合希望系统补齐基础并完成项目练习的学习者。</p>
        </el-tab-pane>
        <el-tab-pane label="课程目录">
          <div v-for="lesson in lessons" :key="lesson" class="lesson-row">
            <span>第 {{ lesson }} 讲</span>
            <strong>{{ lesson === 1 ? '课程试看：学习路线介绍' : '核心知识点讲解与练习' }}</strong>
            <el-tag v-if="lesson === 1" size="small" type="success" effect="plain">可试看</el-tag>
          </div>
        </el-tab-pane>
        <el-tab-pane label="适合人群">
          <p>适合零基础学习者、转行入门者，以及希望用完整项目巩固技能的自学用户。</p>
        </el-tab-pane>
      </el-tabs>
    </div>

    <aside class="side-card">
      <h2>课程信息</h2>
      <div class="info-line"><span>讲师</span><RouterLink :to="`/teachers/${teacher?.id || 1}`">{{ course.teacher }}</RouterLink></div>
      <div class="info-line"><span>课时</span><strong>{{ course.lessons }} 节</strong></div>
      <div class="info-line"><span>学习人数</span><strong>{{ course.students.toLocaleString() }}</strong></div>
      <div class="info-line"><span>评分</span><strong>{{ course.rating }}</strong></div>
    </aside>
  </section>
  <NotFoundView v-else />

  <el-dialog v-model="dialogVisible" title="加入学习计划" width="420px">
    <p>当前是静态页面演示，学习计划功能已预留交互位置。</p>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="dialogVisible = false">确认</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { getCourseApi } from '@/api/course'
import { categories } from '@/data/platform'
import NotFoundView from './NotFoundView.vue'

const route = useRoute()
const router = useRouter()
const dialogVisible = ref(false)
const loading = ref(false)
const rawCourse = ref(null)
const course = computed(() => (rawCourse.value ? mapCourse(rawCourse.value) : null))
const teacher = computed(() => rawCourse.value?.teacher_detail || null)
const lessons = computed(() => {
  const count = rawCourse.value?.chapters?.length || 1
  return Array.from({ length: Math.max(count, 1) }, (_item, index) => index + 1)
})

onMounted(loadCourse)

watch(
  () => route.params.id,
  () => loadCourse(),
)

function categoryName(id) {
  return categories.find((item) => item.id === id)?.name || course.value?.categoryText || '综合课程'
}

function handlePreview() {
  if (course.value?.isFree) {
    router.push(`/courses/${course.value.id}/play`)
    return
  }

  ElMessageBox.alert('该课程当前只开放第 1 讲试看，完整内容后续接入购买流程。', '试看提示', {
    confirmButtonText: '进入试看',
    callback: () => router.push(`/courses/${course.value.id}/play`),
  })
}

async function loadCourse() {
  loading.value = true
  rawCourse.value = null
  try {
    rawCourse.value = await getCourseApi(route.params.id)
  } catch {
    rawCourse.value = null
  } finally {
    loading.value = false
  }
}

function mapCourse(item) {
  const price = Number(item.price || 0)
  return {
    id: item.id,
    title: item.title,
    category: item.category_detail?.slug || item.category_detail?.name || item.category,
    categoryText: item.category_detail?.name || '综合课程',
    teacher: item.teacher_detail?.real_name || '平台讲师',
    level: levelLabel(item.level),
    duration: `${item.chapters?.length || 1} 节`,
    lessons: item.chapters?.length || 1,
    students: item.sales_count || 0,
    rating: Number(item.rating || 0).toFixed(1),
    summary: item.description || item.subtitle || '课程已通过平台审核，更多内容请参考课程目录。',
    cover: (item.title || '课程').slice(0, 3).toUpperCase(),
    price: price > 0 ? `¥${price.toFixed(0)}` : '免费',
    isFree: price <= 0 || item.is_free,
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
