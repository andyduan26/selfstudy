<template>
  <div class="center-panel">
    <div class="panel-heading">
      <div>
        <h2>作品管理</h2>
        <p>管理课程作品的状态、学员数和收益。</p>
      </div>
      <el-button type="primary" @click="$emit('create')">新建作品</el-button>
    </div>

    <el-table v-loading="loading" :data="works" border>
      <el-table-column prop="title" label="课程名称" min-width="220" />
      <el-table-column prop="status" label="状态" width="110">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" effect="plain">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="categoryName" label="分类" width="130" />
      <el-table-column prop="priceText" label="定价" width="110" />
      <el-table-column prop="students" label="学员" width="110" />
      <el-table-column prop="viewCount" label="点播" width="110" />
      <el-table-column prop="updatedAt" label="更新时间" width="170" />
      <el-table-column label="操作" width="150">
        <template #default>
          <el-button text>编辑</el-button>
          <el-button text>预览</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-empty v-if="!loading && works.length === 0" description="暂无课程作品，上传后会显示在这里" />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { getTeacherWorksApi } from '@/api/teacher'

defineEmits(['create'])
defineExpose({ loadWorks })

const loading = ref(false)
const rawWorks = ref([])

const works = computed(() => rawWorks.value.map((course) => ({
  id: course.id,
  title: course.title,
  status: course.status,
  categoryName: course.category_detail?.name || '未分类',
  priceText: Number(course.price) > 0 ? `¥${Number(course.price).toFixed(2)}` : '免费',
  students: course.sales_count || 0,
  viewCount: course.view_count || 0,
  updatedAt: course.updated_at ? new Date(course.updated_at).toLocaleString('zh-CN') : '-',
})))

onMounted(loadWorks)

async function loadWorks() {
  loading.value = true
  try {
    rawWorks.value = await getTeacherWorksApi()
  } finally {
    loading.value = false
  }
}

function statusLabel(status) {
  const labels = {
    draft: '草稿',
    pending: '待审核',
    approved: '已通过',
    rejected: '已驳回',
    published: '已发布',
    offline: '已下架',
  }
  return labels[status] || status
}

function statusType(status) {
  if (status === 'published' || status === 'approved') return 'success'
  if (status === 'pending') return 'warning'
  if (status === 'rejected') return 'danger'
  return 'info'
}
</script>
