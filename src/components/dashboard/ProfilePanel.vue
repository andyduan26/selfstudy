<template>
  <div class="center-panel">
    <div class="panel-heading">
      <div>
        <h2>个人资料</h2>
        <p>查看账号资料、注册时间，并维护昵称、手机号和简介。</p>
      </div>
      <el-button type="primary" @click="openEdit">修改资料</el-button>
    </div>

    <div class="profile-summary">
      <div class="profile-avatar">{{ displayName.slice(0, 1).toUpperCase() }}</div>
      <div>
        <h3>{{ displayName }}</h3>
        <p>{{ roleLabel }}</p>
      </div>
    </div>

    <div class="profile-grid">
      <div class="profile-field">
        <span>账号</span>
        <strong>{{ user?.username || '-' }}</strong>
      </div>
      <div class="profile-field">
        <span>昵称</span>
        <strong>{{ user?.nickname || '-' }}</strong>
      </div>
      <div class="profile-field">
        <span>邮箱</span>
        <strong>{{ user?.email || '-' }}</strong>
      </div>
      <div class="profile-field">
        <span>手机号</span>
        <strong>{{ user?.phone || '-' }}</strong>
      </div>
      <div class="profile-field">
        <span>注册时间</span>
        <strong>{{ joinedAt }}</strong>
      </div>
      <div class="profile-field profile-field--wide">
        <span>个人简介</span>
        <strong>{{ user?.bio || '暂无简介' }}</strong>
      </div>
    </div>
  </div>

  <el-dialog v-model="dialogVisible" title="修改个人资料" width="520px">
    <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
      <el-form-item label="昵称" prop="nickname">
        <el-input v-model="form.nickname" placeholder="请输入昵称" />
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email" placeholder="请输入邮箱" />
      </el-form-item>
      <el-form-item label="手机号" prop="phone">
        <el-input v-model="form.phone" placeholder="请输入 11 位手机号" maxlength="11" />
      </el-form-item>
      <el-form-item label="个人简介">
        <el-input v-model="form.bio" type="textarea" :rows="4" placeholder="简单介绍一下自己" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="submitProfile">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { updateCurrentUserApi } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  user: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['updated'])
const authStore = useAuthStore()
const dialogVisible = ref(false)
const formRef = ref()
const form = reactive({
  nickname: '',
  email: '',
  phone: '',
  bio: '',
})

const rules = {
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' },
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的中国大陆手机号', trigger: 'blur' },
  ],
}

const displayName = computed(() => props.user?.nickname || props.user?.username || '用户')
const roleLabel = computed(() => (props.user?.role === 'teacher' ? '认证讲师' : props.user?.role === 'admin' ? '管理员' : '普通用户'))
const joinedAt = computed(() => (props.user?.date_joined ? new Date(props.user.date_joined).toLocaleString('zh-CN') : '-'))

function openEdit() {
  Object.assign(form, {
    nickname: props.user?.nickname || '',
    email: props.user?.email || '',
    phone: props.user?.phone || '',
    bio: props.user?.bio || '',
  })
  dialogVisible.value = true
}

async function submitProfile() {
  try {
    await formRef.value.validate()
    const user = await updateCurrentUserApi(form)
    authStore.updateUser(user)
    emit('updated', user)
    dialogVisible.value = false
    ElMessage.success('个人资料已更新')
  } catch {
    // Element Plus and Axios already show validation/request messages.
  }
}
</script>
