<template>
  <AdminPageHeader title="用户管理" desc="管理平台用户状态、角色和基础信息。">
    <el-button type="primary" @click="openDialog()">新增用户</el-button>
  </AdminPageHeader>
  <section class="admin-panel">
    <div class="admin-filter">
      <el-input v-model="keyword" placeholder="搜索用户姓名/手机号" clearable />
      <el-select v-model="status" placeholder="用户状态" clearable>
        <el-option label="正常" value="正常" />
        <el-option label="禁用" value="禁用" />
      </el-select>
    </div>
    <el-table :data="pagedRows" border>
      <el-table-column prop="id" label="ID" width="100" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="phone" label="手机号" />
      <el-table-column prop="role" label="角色" />
      <el-table-column prop="status" label="状态" />
      <el-table-column prop="orders" label="订单数" />
      <el-table-column prop="createdAt" label="注册时间" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button text @click="openDialog(row)">编辑</el-button>
          <el-button text @click="toggleUser(row)">{{ row.status === '正常' ? '禁用' : '启用' }}</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-bar"><el-pagination v-model:current-page="page" layout="prev, pager, next" :total="filteredRows.length" :page-size="pageSize" /></div>
  </section>
  <el-dialog v-model="dialogVisible" :title="editing ? '编辑用户' : '新增用户'" width="520px">
    <el-form :model="form" label-position="top">
      <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
      <el-form-item label="角色">
        <el-select v-model="form.role"><el-option label="普通用户" value="普通用户" /><el-option label="讲师" value="讲师" /></el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-radio-group v-model="form.status"><el-radio-button label="正常" /><el-radio-button label="禁用" /></el-radio-group>
      </el-form-item>
    </el-form>
    <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" @click="save">保存</el-button></template>
  </el-dialog>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AdminPageHeader from '@/components/admin/AdminPageHeader.vue'
import { adminUsers } from '@/data/admin'

const keyword = ref('')
const status = ref('')
const page = ref(1)
const pageSize = 5
const dialogVisible = ref(false)
const editing = ref(false)
const form = reactive({ name: '', role: '普通用户', status: '正常' })

const filteredRows = computed(() => adminUsers.filter((row) => {
  const text = `${row.name}${row.phone}`
  return (!keyword.value || text.includes(keyword.value)) && (!status.value || row.status === status.value)
}))
const pagedRows = computed(() => filteredRows.value.slice((page.value - 1) * pageSize, page.value * pageSize))

function openDialog(row) {
  editing.value = Boolean(row)
  Object.assign(form, row || { name: '', role: '普通用户', status: '正常' })
  dialogVisible.value = true
}
function save() {
  dialogVisible.value = false
  ElMessage.success('用户信息已保存')
}
function toggleUser(row) {
  ElMessageBox.confirm(`确认${row.status === '正常' ? '禁用' : '启用'}用户 ${row.name}？`, '操作确认').then(() => {
    ElMessage.success('操作已完成')
  }).catch(() => {})
}
</script>
