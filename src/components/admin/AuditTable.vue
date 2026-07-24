<template>
  <section class="admin-panel">
    <div class="admin-filter">
      <el-input v-model="keyword" :placeholder="type === 'teacher' ? '搜索讲师姓名' : '搜索作品名称'" clearable />
      <el-select v-model="status" placeholder="审核状态" clearable>
        <el-option label="待审核" value="待审核" />
        <el-option label="已通过" value="已通过" />
        <el-option label="待补充" value="待补充" />
        <el-option label="驳回" value="驳回" />
      </el-select>
    </div>
    <el-table :data="pagedRows" border>
      <el-table-column prop="id" label="ID" width="100" />
      <el-table-column :prop="type === 'teacher' ? 'name' : 'title'" :label="type === 'teacher' ? '申请人' : '作品名称'" min-width="220" />
      <el-table-column v-if="type === 'teacher'" prop="direction" label="授课方向" />
      <el-table-column v-if="type === 'teacher'" prop="experience" label="经历" />
      <el-table-column v-if="type === 'work'" prop="teacher" label="讲师" />
      <el-table-column v-if="type === 'work'" prop="category" label="分类" />
      <el-table-column v-if="type === 'work'" prop="lessons" label="课时" width="90" />
      <el-table-column prop="status" label="状态" width="110">
        <template #default="{ row }"><el-tag :type="tagType(row.status)" effect="plain">{{ row.status }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="submittedAt" label="提交时间" width="130" />
      <el-table-column label="操作" width="220">
        <template #default="{ row }">
          <el-button text @click="openReview(row, '通过')">通过</el-button>
          <el-button text @click="openReview(row, '驳回')">驳回</el-button>
          <el-button text @click="openDetail(row)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-bar"><el-pagination v-model:current-page="page" layout="prev, pager, next" :total="filteredRows.length" :page-size="pageSize" /></div>
  </section>

  <el-dialog v-model="dialogVisible" :title="dialogTitle" width="560px">
    <el-form :model="form" label-position="top">
      <el-form-item label="审核备注">
        <el-input v-model="form.remark" type="textarea" :rows="4" placeholder="请输入审核意见" />
      </el-form-item>
    </el-form>
    <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" @click="submitReview">确认</el-button></template>
  </el-dialog>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const props = defineProps({
  rows: { type: Array, required: true },
  type: { type: String, required: true },
})

const keyword = ref('')
const status = ref('')
const page = ref(1)
const pageSize = 5
const dialogVisible = ref(false)
const dialogTitle = ref('审核')
const form = reactive({ remark: '' })

const filteredRows = computed(() => props.rows.filter((row) => {
  const name = props.type === 'teacher' ? row.name : row.title
  return (!keyword.value || name.includes(keyword.value)) && (!status.value || row.status === status.value)
}))
const pagedRows = computed(() => filteredRows.value.slice((page.value - 1) * pageSize, page.value * pageSize))

function tagType(value) {
  if (value === '已通过') return 'success'
  if (value === '待审核') return 'warning'
  if (value === '驳回') return 'danger'
  return 'info'
}
function openReview(row, action) {
  dialogTitle.value = `${action}：${props.type === 'teacher' ? row.name : row.title}`
  form.remark = action === '通过' ? '资料完整，审核通过。' : ''
  dialogVisible.value = true
}
function openDetail(row) {
  ElMessageBox.alert(JSON.stringify(row, null, 2), '详情信息', { confirmButtonText: '关闭' })
}
function submitReview() {
  dialogVisible.value = false
  ElMessage.success('审核操作已记录')
}
</script>
