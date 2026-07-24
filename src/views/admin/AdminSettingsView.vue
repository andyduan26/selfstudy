<template>
  <AdminPageHeader title="系统配置" desc="维护平台基础配置、审核规则和提现参数。">
    <el-button type="primary" @click="saveSettings">保存配置</el-button>
  </AdminPageHeader>
  <section class="admin-panel">
    <el-form :model="settings" label-position="top" class="admin-settings-form">
      <el-row :gutter="24">
        <el-col :span="12"><el-form-item label="平台名称"><el-input v-model="settings.siteName" /></el-form-item></el-col>
        <el-col :span="12"><el-form-item label="客服电话"><el-input v-model="settings.phone" /></el-form-item></el-col>
      </el-row>
      <el-form-item label="讲师审核">
        <el-switch v-model="settings.teacherAudit" active-text="开启" inactive-text="关闭" />
      </el-form-item>
      <el-form-item label="作品审核">
        <el-switch v-model="settings.workAudit" active-text="开启" inactive-text="关闭" />
      </el-form-item>
      <el-form-item label="最低提现金额">
        <el-input-number v-model="settings.minWithdraw" :min="100" :step="100" />
      </el-form-item>
      <el-form-item label="平台公告">
        <el-input v-model="settings.notice" type="textarea" :rows="4" />
      </el-form-item>
    </el-form>
  </section>
</template>

<script setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import AdminPageHeader from '@/components/admin/AdminPageHeader.vue'

const settings = reactive({
  siteName: '我要自学网',
  phone: '400-800-2026',
  teacherAudit: true,
  workAudit: true,
  minWithdraw: 100,
  notice: '欢迎使用我要自学网后台管理系统。',
})

function saveSettings() {
  ElMessage.success('系统配置已保存')
}
</script>
