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
        <TeacherWorksPanel v-if="activeMenu === 'works'" @create="workDialogVisible = true" />
        <IncomePanel v-if="activeMenu === 'income'" />
        <WithdrawPanel v-if="activeMenu === 'withdraw'" @withdraw="withdrawDialogVisible = true" />
      </main>
    </div>
  </section>

  <el-dialog v-model="workDialogVisible" title="新建作品" width="520px">
    <el-form :model="workForm" label-position="top">
      <el-form-item label="课程名称">
        <el-input v-model="workForm.title" placeholder="请输入课程名称" />
      </el-form-item>
      <el-form-item label="课程分类">
        <el-select v-model="workForm.category" placeholder="选择分类">
          <el-option label="前端开发" value="frontend" />
          <el-option label="后端开发" value="backend" />
          <el-option label="办公效率" value="office" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="workDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitWork">保存草稿</el-button>
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
import { computed, reactive, ref, watch } from 'vue'
import { onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { DataAnalysis, Document, Money, Promotion, User, Wallet } from '@element-plus/icons-vue'
import { getCurrentUserApi } from '@/api/auth'
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
  category: '',
})

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

const isTeacher = computed(() => authStore.role === 'teacher')
const visibleMenus = computed(() => allMenus.filter((item) => item.role === 'all' || item.role === authStore.role))
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
  authStore.login({ accessToken: authStore.token || 'demo-token', userRole: role })
  ElMessage.success(role === 'teacher' ? '已切换为认证讲师' : '已切换为普通用户')
}

function submitWork() {
  workDialogVisible.value = false
  ElMessage.success('作品草稿已保存')
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
