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
        <div class="course-cover large course-detail-cover">
          <img v-if="course.coverUrl" :src="course.coverUrl" :alt="course.title" />
          <span v-else>{{ course.cover }}</span>
        </div>
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
            <el-button size="large" @click="openPayDialog">{{ course.isFree ? '免费加入' : '开通学习' }}</el-button>
            <el-button size="large" @click="dialogVisible = true">加入学习计划</el-button>
          </div>
        </div>
      </div>

      <el-tabs class="detail-tabs">
        <el-tab-pane label="课程介绍">
          <p>{{ course.summary }} 课程采用循序渐进的方式讲解，适合希望系统补齐基础并完成项目练习的学习者。</p>
        </el-tab-pane>
        <el-tab-pane label="课程目录">
          <div v-for="chapter in chapterGroups" :key="chapter.id" class="chapter-directory">
            <h3>{{ chapter.index }}. {{ chapter.title }}</h3>
            <div v-for="lesson in chapter.lessons" :key="lesson.id" class="lesson-row">
              <span>第 {{ lesson.index }} 节</span>
              <strong>{{ lesson.title }}</strong>
              <el-tag v-if="lesson.isFreePreview" size="small" type="success" effect="plain">可试看</el-tag>
              <el-button size="small" type="primary" plain @click="playLesson(lesson)">
                {{ lesson.isFreePreview ? '播放' : '试看' }}
              </el-button>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="适合人群">
          <p>适合零基础学习者、转行入门者，以及希望用完整项目巩固技能的自学用户。</p>
        </el-tab-pane>
      </el-tabs>

      <section class="comment-section">
        <div class="section-heading compact-heading">
          <div>
            <p class="section-kicker">Course Reviews</p>
            <h2>学员评论</h2>
          </div>
          <span>{{ comments.length }} 条可见评论</span>
        </div>

        <div class="comment-editor">
          <el-rate v-model="commentForm.rating" />
          <el-input
            v-model="commentForm.content"
            type="textarea"
            :rows="4"
            maxlength="300"
            show-word-limit
            placeholder="写下你的学习感受，提交后会立即展示"
          />
          <div class="comment-actions">
            <span>评论提交后会立即展示在课程页。</span>
            <el-button type="primary" :loading="commentSubmitting" @click="submitComment">提交评论</el-button>
          </div>
        </div>

        <div v-if="comments.length" class="comment-list">
          <article v-for="item in comments" :key="item.id" class="comment-card">
            <div>
              <strong>{{ item.user_detail?.nickname || item.user_detail?.username || '学员' }}</strong>
              <span>{{ formatDate(item.created_at) }}</span>
            </div>
            <el-rate :model-value="item.rating" disabled />
            <p>{{ item.content }}</p>
          </article>
        </div>
        <el-empty v-else description="暂无已通过评论" />
      </section>
    </div>

    <aside class="side-card">
      <h2>课程信息</h2>
      <div class="info-line"><span>讲师</span><RouterLink :to="`/teachers/${teacher?.id || 1}`">{{ course.teacher }}</RouterLink></div>
      <div class="info-line"><span>课时</span><strong>{{ course.lessons }} 节</strong></div>
      <div class="info-line"><span>学习人数</span><strong>{{ course.students.toLocaleString() }}</strong></div>
      <div class="info-line"><span>评分</span><strong>{{ course.rating }}</strong></div>
      <el-button class="side-card__button" type="primary" @click="openPayDialog">{{ course.isFree ? '免费加入学习' : '开通后学习完整课程' }}</el-button>
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

  <el-dialog v-model="payDialogVisible" title="开通学习权限" width="460px">
    <div v-if="course" class="pay-dialog">
      <div class="pay-dialog__row">
        <span>课程</span>
        <strong>{{ course.title }}</strong>
      </div>
      <div class="pay-dialog__row">
        <span>金额</span>
        <strong>{{ course.price }}</strong>
      </div>
      <el-radio-group v-model="payForm.pay_method" class="pay-methods">
        <el-radio-button label="alipay">支付宝</el-radio-button>
        <el-radio-button label="wechat" disabled>微信</el-radio-button>
      </el-radio-group>
      <div v-if="qrcodeDataUrl" class="qrcode-pay">
        <img :src="qrcodeDataUrl" alt="支付宝扫码支付二维码" />
        <p>请使用支付宝沙箱 App 扫码支付，支付成功后页面会自动进入学习。</p>
      </div>
      <p v-else>当前接入支付宝当面付沙箱。点击后生成扫码支付二维码，支付成功后由支付宝异步通知后端完成订单和收益结算。</p>
    </div>
    <template #footer>
      <el-button @click="closePayDialog">取消</el-button>
      <el-button v-if="qrcodeDataUrl" :loading="pollingPayment" @click="checkPaymentStatus">我已支付</el-button>
      <el-button type="primary" :loading="paying" @click="submitPayment">{{ qrcodeDataUrl ? '重新生成' : '生成支付二维码' }}</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import QRCode from 'qrcode'
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { createCourseCommentApi, getCourseCommentsApi } from '@/api/comment'
import { getCourseApi } from '@/api/course'
import { createAlipayQrcodeApi, getOrderStatusApi } from '@/api/order'
import { useAuthStore } from '@/stores/auth'
import { categories } from '@/data/platform'
import NotFoundView from './NotFoundView.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const dialogVisible = ref(false)
const payDialogVisible = ref(false)
const loading = ref(false)
const paying = ref(false)
const pollingPayment = ref(false)
const commentSubmitting = ref(false)
const rawCourse = ref(null)
const comments = ref([])
const payForm = ref({ pay_method: 'alipay' })
const currentOrder = ref(null)
const qrcodeDataUrl = ref('')
const paymentTimer = ref(null)
const commentForm = ref({ rating: 5, content: '' })
const course = computed(() => (rawCourse.value ? mapCourse(rawCourse.value) : null))
const teacher = computed(() => rawCourse.value?.teacher_detail || null)
const chapterGroups = computed(() => {
  const chapters = rawCourse.value?.chapters || []
  if (!chapters.length) {
    return [{ id: 'default', index: 1, title: '默认章节', lessons: [{ id: 'default-lesson', index: 1, title: '课程试看：学习路线介绍', isFreePreview: true }] }]
  }
  return chapters.map((chapter, chapterIndex) => ({
    id: chapter.id,
    index: chapterIndex + 1,
    title: chapter.title || `第 ${chapterIndex + 1} 章`,
    lessons: (chapter.videos || []).map((video, lessonIndex) => ({
      id: video.id,
      index: lessonIndex + 1,
      title: video.title || `第 ${lessonIndex + 1} 节`,
      isFreePreview: video.is_free_preview || chapter.is_free_preview || (chapterIndex === 0 && lessonIndex === 0),
    })),
  }))
})

onMounted(loadCourse)
onBeforeUnmount(stopPaymentPolling)

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

function playLesson(lesson) {
  if (!lesson.isFreePreview) {
    ElMessageBox.alert('该节暂未开放试看，购买后可观看完整内容。', '播放提示', {
      confirmButtonText: '知道了',
    })
    return
  }
  router.push(`/courses/${course.value.id}/play`)
}

async function loadCourse() {
  loading.value = true
  rawCourse.value = null
  comments.value = []
  try {
    rawCourse.value = await getCourseApi(route.params.id)
    await loadComments()
  } catch {
    rawCourse.value = null
  } finally {
    loading.value = false
  }
}

async function loadComments() {
  comments.value = await getCourseCommentsApi(route.params.id)
}

function openPayDialog() {
  if (!authStore.isLoggedIn) {
    router.push(`/login?redirect=/courses/${course.value.id}`)
    return
  }
  qrcodeDataUrl.value = ''
  currentOrder.value = null
  payDialogVisible.value = true
}

async function submitPayment() {
  paying.value = true
  try {
    const data = await createAlipayQrcodeApi({
      course_id: course.value.id,
    })
    currentOrder.value = data
    if (data.paid) {
      ElMessage.success('免费课程已开通')
      payDialogVisible.value = false
      router.push(`/courses/${course.value.id}/play`)
      return
    }
    qrcodeDataUrl.value = await QRCode.toDataURL(data.qr_code, { width: 220, margin: 1 })
    startPaymentPolling()
  } finally {
    paying.value = false
  }
}

function closePayDialog() {
  payDialogVisible.value = false
  qrcodeDataUrl.value = ''
  currentOrder.value = null
  stopPaymentPolling()
}

function startPaymentPolling() {
  stopPaymentPolling()
  paymentTimer.value = window.setInterval(checkPaymentStatus, 3000)
}

function stopPaymentPolling() {
  if (paymentTimer.value) {
    window.clearInterval(paymentTimer.value)
    paymentTimer.value = null
  }
}

async function checkPaymentStatus() {
  if (!currentOrder.value?.id || pollingPayment.value) return
  pollingPayment.value = true
  try {
    const data = await getOrderStatusApi(currentOrder.value.id)
    if (data.paid) {
      stopPaymentPolling()
      payDialogVisible.value = false
      ElMessage.success('支付成功，正在进入课程')
      router.push(`/courses/${course.value.id}/play`)
    }
  } finally {
    pollingPayment.value = false
  }
}

async function submitComment() {
  if (!authStore.isLoggedIn) {
    router.push(`/login?redirect=/courses/${course.value.id}`)
    return
  }
  if (!commentForm.value.content.trim()) {
    ElMessage.warning('请先填写评论内容')
    return
  }
  commentSubmitting.value = true
  try {
    await createCourseCommentApi({
      course: course.value.id,
      rating: commentForm.value.rating,
      content: commentForm.value.content.trim(),
    })
    commentForm.value = { rating: 5, content: '' }
    ElMessage.success('评论发布成功')
    await loadComments()
  } finally {
    commentSubmitting.value = false
  }
}

function formatDate(value) {
  if (!value) return ''
  return new Date(value).toLocaleDateString('zh-CN')
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
    coverUrl: item.cover || item.cover_url || '',
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
