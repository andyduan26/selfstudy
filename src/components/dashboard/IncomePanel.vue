<template>
  <div class="center-panel">
    <div class="panel-heading">
      <div>
        <h2>收益中心</h2>
        <p>查看课程收益明细与结算状态。</p>
      </div>
      <el-tag effect="plain">可提现 {{ money(summary.withdrawable) }}</el-tag>
    </div>

    <div class="income-summary">
      <div>
        <span>累计收益</span>
        <strong>{{ money(summary.total) }}</strong>
      </div>
      <div>
        <span>待结算</span>
        <strong>{{ money(summary.pending) }}</strong>
      </div>
      <div>
        <span>可提现</span>
        <strong>{{ money(summary.withdrawable) }}</strong>
      </div>
    </div>

    <el-table v-loading="loading" :data="rows" border>
      <el-table-column prop="createdAt" label="时间" width="170" />
      <el-table-column prop="courseTitle" label="课程" min-width="240" />
      <el-table-column prop="amount" label="金额" width="120" />
      <el-table-column prop="status" label="状态" width="120" />
    </el-table>
    <el-empty v-if="!loading && rows.length === 0" description="暂无收益明细" />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { getMyRevenueSummaryApi } from '@/api/revenue'

const loading = ref(false)
const summary = ref({
  total: 0,
  pending: 0,
  withdrawable: 0,
  settled: 0,
  rows: [],
})

const rows = computed(() => (summary.value.rows || []).map((row) => ({
  id: row.id,
  createdAt: row.created_at ? new Date(row.created_at).toLocaleString('zh-CN') : '-',
  courseTitle: row.course_detail?.title || `课程 #${row.course}`,
  amount: money(row.teacher_amount),
  status: statusLabel(row.status),
})))

onMounted(loadIncome)

async function loadIncome() {
  loading.value = true
  try {
    summary.value = await getMyRevenueSummaryApi()
  } finally {
    loading.value = false
  }
}

function money(value) {
  return `¥${Number(value || 0).toFixed(2)}`
}

function statusLabel(status) {
  const labels = {
    pending: '待结算',
    settled: '已结算',
    withdrawable: '可提现',
  }
  return labels[status] || status
}
</script>
