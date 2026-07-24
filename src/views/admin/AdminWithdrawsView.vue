<template>
  <AdminPageHeader title="提现审核" desc="审核讲师提现申请并记录打款状态。" />
  <section class="admin-panel">
    <div class="admin-filter">
      <el-input v-model="keyword" placeholder="搜索讲师/提现单号" clearable />
      <el-select v-model="status" placeholder="提现状态" clearable>
        <el-option label="待审核" value="待审核" />
        <el-option label="已打款" value="已打款" />
        <el-option label="驳回" value="驳回" />
      </el-select>
    </div>
    <el-table :data="pagedRows" border>
      <el-table-column prop="id" label="提现单号" min-width="170" />
      <el-table-column prop="teacher" label="讲师" width="110" />
      <el-table-column prop="amount" label="金额" width="110" />
      <el-table-column prop="account" label="到账账户" min-width="220" />
      <el-table-column prop="status" label="状态" width="110" />
      <el-table-column prop="submittedAt" label="申请时间" width="130" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button text @click="approve(row)">通过</el-button>
          <el-button text @click="reject(row)">驳回</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-bar"><el-pagination v-model:current-page="page" layout="prev, pager, next" :total="filteredRows.length" :page-size="pageSize" /></div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AdminPageHeader from '@/components/admin/AdminPageHeader.vue'
import { withdrawAudits } from '@/data/admin'

const keyword = ref('')
const status = ref('')
const page = ref(1)
const pageSize = 5
const filteredRows = computed(() => withdrawAudits.filter((row) => {
  const text = `${row.id}${row.teacher}`
  return (!keyword.value || text.includes(keyword.value)) && (!status.value || row.status === status.value)
}))
const pagedRows = computed(() => filteredRows.value.slice((page.value - 1) * pageSize, page.value * pageSize))
function approve(row) {
  ElMessageBox.confirm(`确认通过 ${row.teacher} 的提现申请 ${row.amount}？`, '提现审核').then(() => ElMessage.success('提现审核已通过')).catch(() => {})
}
function reject(row) {
  ElMessageBox.prompt('请输入驳回原因', '驳回提现').then(() => ElMessage.success('提现申请已驳回')).catch(() => {})
}
</script>
