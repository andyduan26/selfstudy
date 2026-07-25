<template>
  <main class="login-page">
    <section class="auth-shell">
      <div class="auth-intro">
        <p class="section-kicker">Account</p>
        <h1>开始你的系统学习</h1>
        <p class="section-desc">登录或注册后可进入用户中心、讲师中心。账号会通过 Django 后端保存，登录使用 JWT。</p>
      </div>

      <div class="login-panel">
        <el-tabs v-model="activeTab" stretch>
          <el-tab-pane label="登录" name="login">
            <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-position="top" class="login-form">
              <el-form-item label="账号 / 邮箱 / 手机号 / 昵称" prop="account">
                <el-input v-model="loginForm.account" placeholder="请输入账号、邮箱、手机号或昵称" />
              </el-form-item>
              <el-form-item label="密码" prop="password">
                <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" show-password />
              </el-form-item>
              <el-form-item label="登录身份">
                <el-radio-group v-model="selectedRole">
                  <el-radio-button label="user">普通用户</el-radio-button>
                  <el-radio-button label="teacher">讲师</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-button type="primary" class="login-button" @click="handleLogin">登录</el-button>
            </el-form>
          </el-tab-pane>

          <el-tab-pane label="注册" name="register">
            <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" label-position="top" class="login-form">
              <el-form-item label="昵称" prop="nickname">
                <el-input v-model="registerForm.nickname" placeholder="请输入昵称" />
              </el-form-item>
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="registerForm.email" placeholder="请输入邮箱" />
              </el-form-item>
              <el-form-item label="手机号" prop="phone">
                <el-input v-model="registerForm.phone" placeholder="请输入 11 位手机号" maxlength="11" />
              </el-form-item>
              <el-form-item label="密码" prop="password">
                <el-input v-model="registerForm.password" type="password" placeholder="至少 8 位，建议包含字母和数字" show-password />
              </el-form-item>
              <el-form-item label="注册身份">
                <el-select v-model="selectedRole">
                  <el-option label="普通用户" value="user" />
                  <el-option label="讲师" value="teacher" />
                </el-select>
              </el-form-item>
              <el-button type="primary" class="login-button" @click="handleRegister">注册并进入</el-button>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>
    </section>
  </main>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { loginApi, registerApi } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const activeTab = ref('login')
const selectedRole = ref('user')
const loginFormRef = ref()
const registerFormRef = ref()

const loginForm = reactive({
  account: 'andyduan26',
  password: 'Ay281988',
})

const registerForm = reactive({
  nickname: '',
  email: '',
  phone: '',
  password: '',
})

const loginRules = {
  account: [{ required: true, message: '请输入账号、邮箱、手机号或昵称', trigger: 'blur' }],
  password: [{ required: true, min: 8, message: '请输入至少 8 位密码', trigger: 'blur' }],
}

const registerRules = {
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' },
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的中国大陆手机号', trigger: 'blur' },
  ],
  password: [{ required: true, min: 8, message: '请输入至少 8 位密码', trigger: 'blur' }],
}

async function handleLogin() {
  try {
    await loginFormRef.value.validate()
    const data = await loginApi(loginForm)
    signIn({
      message: '登录成功',
      accessToken: data.access,
      userRole: data.user?.role || selectedRole.value,
      userInfo: data.user,
    })
  } catch (error) {
    if (!error?.response) {
      // Element Plus has already rendered field-level validation messages.
    }
  }
}

async function handleRegister() {
  try {
    await registerFormRef.value.validate()
    const data = await registerApi({
      ...registerForm,
      role: selectedRole.value,
    })
    signIn({
      message: '注册成功',
      accessToken: data.access,
      userRole: data.user?.role || selectedRole.value,
      userInfo: data.user,
    })
  } catch (error) {
    if (!error?.response) {
      // Element Plus has already rendered field-level validation messages.
    }
  }
}

function signIn({ message, accessToken, userRole, userInfo }) {
  authStore.login({
    accessToken,
    userRole,
    userInfo,
  })
  ElMessage.success(message)
  router.push(route.query.redirect || '/')
}
</script>
