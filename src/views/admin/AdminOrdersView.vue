<template>
  <AdminPageHeader title="订单管理" desc="查看课程订单、支付状态与退款处理。" />
  <section class="admin-panel">
    <div class="admin-filter">
      <el-input v-model="keyword" placeholder="搜索订单/用户/课程" clearable />
      <el-select v-model="status" placeholder="订单状态" clearable>
        <el-option label="已支付" value="已支付" />
        <el-option label="退款中" value="退款中" />
        <el-option label="已完成" value="已完成" />
      </el-select>
    </div>
    <el-table :data="pagedRows" border>
      <el-table-column prop="id" label="订单号" min-width="170" />
      <el-table-column prop="user" label="用户" width="110" />
      <el-table-column prop="course" label="课程" min-width="220" />
      <el-table-column prop="amount" label="金额" width="100" />
      <el-table-column prop="status" label="状态" width="110" />
      <el-table-column prop="paidAt" label="支付时间" width="130" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button text @click="openOrder(row)">详情</el-button>
          <el-button text @click="refund(row)">退款</el-button>
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
import { adminOrders } from '@/data/admin'

const keyword = ref('')
const status = ref('')
const page = ref(1)
const pageSize = 5
const filteredRows = computed(() => adminOrders.filter((row) => {
  const text = `${row.id}${row.user}${row.course}`
  return (!keyword.value || text.includes(keyword.value)) && (!status.value || row.status === status.value)
}))
const pagedRows = computed(() => filteredRows.value.slice((page.value - 1) * pageSize, page.value * pageSize))
function openOrder(row) {
  ElMessageBox.alert(`订单号：${row.id}\n用户：${row.user}\n课程：${row.course}\n金额：${row.amount}`, '订单详情')
}
function refund(row) {
  ElMessageBox.confirm(`确认处理订单 ${row.id} 的退款？`, '退款确认').then(() => ElMessage.success('退款操作已记录')).catch(() => {})
}
</script>
