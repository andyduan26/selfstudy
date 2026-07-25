<template>
  <section class="page-section personal-center">
    <div class="center-header">
      <div>
        <p class="section-kicker">Personal Center</p>
        <h1>{{ isTeacher ? '讲师工作台' : '个人中心' }}</h1>
        <p class="section-desc">
          {{ userSummary }}
        </p>
      </div>
      <div class="identity-switch">
        <span>当前身份</span>
        <el-segmented v-model="currentRole" :options="roleOptions" @change="handleRoleChange" />
      </div>
    </div>

    <div class="center-shell">
      <aside class="center-sidebar">
        <button
          v-for="item in visibleMenus"
          :key="item.key"
          class="center-menu-item"
          :class="{ 'is-active': activeMenu === item.key }"
          @click="activeMenu = item.key"
        >
          <component :is="item.icon" />
          <span>{{ item.label }}</span>
        </button>
      </aside>

      <main class="center-content">
        <ProfilePanel v-if="activeMenu === 'profile'" :user="profileUser" @updated="profileUser = $event" />
        <TeacherApplyPanel v-if="activeMenu === 'apply'" />
        <TeacherDashboardPanel v-if="activeMenu === 'dashboard'" />
        <TeacherWorksPanel v-if="activeMenu === 'works'" ref="teacherWorksRef" @create="workDialogVisible = true" />
        <IncomePanel v-if="activeMenu === 'income'" />
        <WithdrawPanel v-if="activeMenu === 'withdraw'" @withdraw="withdrawDialogVisible = true" />
      </main>
    </div>
  </section>

  <el-dialog v-model="workDialogVisible" title="上传课程作品" width="760px">
    <el-form ref="workFormRef" :model="workForm" :rules="workRules" label-position="top">
      <el-row :gutter="18">
        <el-col :span="12">
          <el-form-item label="课程名称" prop="title">
            <el-input v-model="workForm.title" placeholder="请输入课程名称" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="课程分类" prop="categoryName">
            <el-input v-model="workForm.categoryName" placeholder="例如：前端开发、后端开发、AI 工具" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="课程说明" prop="description">
        <el-input v-model="workForm.description" type="textarea" :rows="4" placeholder="请填写课程介绍、适合人群和学习目标" />
      </el-form-item>
      <el-form-item label="定价">
        <el-input-number v-model="workForm.price" :min="0" :step="10" />
      </el-form-item>
      <el-form-item label="课程封面">
        <el-upload :auto-upload="false" :limit="1" :on-change="handleCover" :on-remove="() => (workForm.cover = null)">
          <el-button>选择封面图片</el-button>
        </el-upload>
      </el-form-item>
      <div class="chapter-upload-section">
        <div class="section-heading small">
          <h2>课程章节</h2>
          <el-button type="primary" plain @click="addChapter">添加章节</el-button>
        </div>
        <article v-for="(chapter, index) in workForm.chapters" :key="chapter.uid" class="chapter-upload-card">
          <div class="chapter-upload-card__head">
            <strong>第 {{ index + 1 }} 章</strong>
            <el-button v-if="workForm.chapters.length > 1" text type="danger" @click="removeChapter(index)">删除</el-button>
          </div>
          <el-row :gutter="16">
            <el-col :span="12">
              <el-form-item :label="`章节标题`" :prop="`chapters.${index}.title`" :rules="chapterTitleRules">
                <el-input v-model="chapter.title" placeholder="例如：课程介绍与学习路径" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item :label="`视频标题`" :prop="`chapters.${index}.videoTitle`" :rules="chapterVideoTitleRules">
                <el-input v-model="chapter.videoTitle" placeholder="例如：试看导学" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="章节简介">
            <el-input v-model="chapter.summary" placeholder="简要说明本章学习内容" />
          </el-form-item>
          <div class="chapter-upload-card__foot">
            <el-upload :auto-upload="false" :limit="1" :on-change="(file) => handleChapterVideo(index, file)" :on-remove="() => (chapter.videoFile = null)">
              <el-button>选择本章视频</el-button>
            </el-upload>
            <el-switch v-model="chapter.isFreePreview" active-text="允许试看" />
          </div>
        </article>
      </div>
      <el-form-item label="课程附件（文档/图片/音频/压缩包等）">
        <el-upload :auto-upload="false" :limit="1" :on-change="handleAttachment" :on-remove="() => (workForm.attachmentFile = null)">
          <el-button>选择附件</el-button>
        </el-upload>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="workDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitWork">提交审核</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="withdrawDialogVisible" title="申请提现" width="520px">
    <el-form ref="withdrawFormRef" :model="withdrawForm" :rules="withdrawRules" label-position="top">
      <el-form-item label="提现金额" prop="amount">
        <el-input v-model="withdrawForm.amount" placeholder="最低 100 元" />
      </el-form-item>
      <el-form-item label="提现账户" prop="account">
        <el-select v-model="withdrawForm.account" placeholder="选择到账账户">
          <el-option label="招商银行 尾号 0826" value="bank" />
          <el-option label="支付宝 duan***@mail.com" value="alipay" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="withdrawDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitWithdraw">提交申请</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, nextTick, reactive, ref, watch } from 'vue'
import { onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { DataAnalysis, Document, Money, Promotion, User, Wallet } from '@element-plus/icons-vue'
import { getCurrentUserApi } from '@/api/auth'
import { uploadTeacherWorkApi } from '@/api/teacher'
import { useAuthStore } from '@/stores/auth'
import ProfilePanel from './ProfilePanel.vue'
import TeacherApplyPanel from './TeacherApplyPanel.vue'
import TeacherDashboardPanel from './TeacherDashboardPanel.vue'
import TeacherWorksPanel from './TeacherWorksPanel.vue'
import IncomePanel from './IncomePanel.vue'
import WithdrawPanel from './WithdrawPanel.vue'

const authStore = useAuthStore()
const currentRole = ref(authStore.role)
const activeMenu = ref('profile')
const profileUser = ref(authStore.user)
const workDialogVisible = ref(false)
const withdrawDialogVisible = ref(false)
const withdrawFormRef = ref()
const workFormRef = ref()
const teacherWorksRef = ref()

const roleOptions = [
  { label: '普通用户', value: 'user' },
  { label: '认证讲师', value: 'teacher' },
]

const allMenus = [
  { key: 'profile', label: '个人资料', role: 'all', icon: User },
  { key: 'apply', label: '讲师入驻申请', role: 'user', icon: Promotion },
  { key: 'dashboard', label: '数据看板', role: 'teacher', icon: DataAnalysis },
  { key: 'works', label: '作品管理', role: 'teacher', icon: Document },
  { key: 'income', label: '收益中心', role: 'teacher', icon: Money },
  { key: 'withdraw', label: '提现中心', role: 'teacher', icon: Wallet },
]

const workForm = reactive({
  title: '',
  categoryName: '',
  description: '',
  price: 0,
  cover: null,
  attachmentFile: null,
  chapters: [createChapter()],
})

const workRules = {
  title: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  categoryName: [{ required: true, message: '请输入课程分类', trigger: 'blur' }],
  description: [{ required: true, min: 10, message: '请至少填写 10 个字说明', trigger: 'blur' }],
}
const chapterTitleRules = [{ required: true, message: '请输入章节标题', trigger: 'blur' }]
const chapterVideoTitleRules = [{ required: true, message: '请输入视频标题', trigger: 'blur' }]

const withdrawForm = reactive({
  amount: '',
  account: '',
})

const withdrawRules = {
  amount: [
    { required: true, message: '请输入提现金额', trigger: 'blur' },
    {
      validator: (_rule, value, callback) => {
        if (Number(value) >= 100) callback()
        else callback(new Error('提现金额不能低于 100 元'))
      },
      trigger: 'blur',
    },
  ],
  account: [{ required: true, message: '请选择提现账户', trigger: 'change' }],
}

const isTeacherCertified = computed(() => Boolean(profileUser.value?.is_verified_teacher || authStore.user?.is_verified_teacher))
const effectiveRole = computed(() => (currentRole.value === 'teacher' && isTeacherCertified.value ? 'teacher' : 'user'))
const isTeacher = computed(() => effectiveRole.value === 'teacher')
const visibleMenus = computed(() => allMenus.filter((item) => item.role === 'all' || item.role === effectiveRole.value))
const userSummary = computed(() => {
  const user = profileUser.value
  if (!user) return '正在读取你的账号资料。'
  const name = user.nickname || user.username
  return `${name}，账号 ${user.username}，注册时间 ${new Date(user.date_joined).toLocaleDateString('zh-CN')}`
})

onMounted(async () => {
  try {
    const user = await getCurrentUserApi()
    profileUser.value = user
    authStore.updateUser(user)
    if (authStore.role === 'teacher' && user.is_verified_teacher) {
      currentRole.value = 'teacher'
      activeMenu.value = 'dashboard'
    } else {
      currentRole.value = 'user'
    }
  } catch {
    // Request interceptor already shows errors.
  }
})

watch(
  () => authStore.role,
  (role) => {
    currentRole.value = role
    if (!visibleMenus.value.some((item) => item.key === activeMenu.value)) {
      activeMenu.value = 'profile'
    }
  },
)

function handleRoleChange(role) {
  if (role === 'teacher' && !isTeacherCertified.value) {
    currentRole.value = 'user'
    ElMessageBox.alert('抱歉，请先申请认证教师', '无法切换身份', {
      confirmButtonText: '去申请',
      type: 'warning',
    }).then(() => {
      activeMenu.value = 'apply'
    })
    return
  }
  authStore.login({ accessToken: authStore.token || 'demo-token', userRole: role })
  ElMessage.success(role === 'teacher' ? '已切换为认证讲师' : '已切换为普通用户')
  activeMenu.value = role === 'teacher' ? 'dashboard' : 'profile'
}

function handleCover(file) {
  workForm.cover = file.raw
}

function handleAttachment(file) {
  workForm.attachmentFile = file.raw
}

function createChapter() {
  const uid = Date.now() + Math.random()
  return {
    uid,
    title: '',
    summary: '',
    videoTitle: '',
    videoFile: null,
    isFreePreview: false,
  }
}

function addChapter() {
  workForm.chapters.push(createChapter())
}

function removeChapter(index) {
  workForm.chapters.splice(index, 1)
}

function handleChapterVideo(index, file) {
  workForm.chapters[index].videoFile = file.raw
}

async function submitWork() {
  try {
    await workFormRef.value.validate()
    const formData = new FormData()
    formData.append('title', workForm.title)
    formData.append('category_name', workForm.categoryName)
    formData.append('description', workForm.description)
    formData.append('price', workForm.price)
    if (workForm.cover) formData.append('cover', workForm.cover)
    formData.append('chapters', JSON.stringify(workForm.chapters.map((chapter, index) => ({
      title: chapter.title,
      summary: chapter.summary,
      videoTitle: chapter.videoTitle,
      isFreePreview: chapter.isFreePreview,
      sortWeight: index + 1,
    }))))
    workForm.chapters.forEach((chapter, index) => {
      if (chapter.videoFile) formData.append(`chapter_video_${index}`, chapter.videoFile)
    })
    if (workForm.attachmentFile) formData.append('attachment_file', workForm.attachmentFile)
    await uploadTeacherWorkApi(formData)
    workDialogVisible.value = false
    activeMenu.value = 'works'
    await nextTick()
    await teacherWorksRef.value?.loadWorks?.()
    ElMessage.success('作品已上传，等待后台审核')
  } catch {
    // Element Plus and Axios already show errors.
  }
}

async function submitWithdraw() {
  try {
    await withdrawFormRef.value.validate()
    withdrawDialogVisible.value = false
    ElMessage.success('提现申请已提交')
  } catch {
    // Element Plus renders validation messages in the dialog.
  }
}
</script>
