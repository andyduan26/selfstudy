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
          <el-tag :type="courseStatusType(row.status)" effect="plain">{{ courseStatusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="categoryName" label="分类" width="130" />
      <el-table-column prop="priceText" label="定价" width="110" />
      <el-table-column prop="students" label="学员" width="110" />
      <el-table-column prop="viewCount" label="点播" width="110" />
      <el-table-column prop="updatedAt" label="更新时间" width="170" />
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button text @click="openEdit(row)">编辑</el-button>
          <el-button text @click="previewWork(row)">预览</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-empty v-if="!loading && works.length === 0" description="暂无课程作品，上传后会显示在这里" />
  </div>

  <el-dialog v-model="editVisible" title="编辑课程作品" width="560px">
    <el-form :model="editForm" label-position="top">
      <el-form-item label="课程名称">
        <el-input v-model="editForm.title" />
      </el-form-item>
      <el-form-item label="课程分类">
        <el-input v-model="editForm.categoryName" disabled />
      </el-form-item>
      <el-form-item label="定价">
        <el-input v-model="editForm.priceText" disabled />
      </el-form-item>
      <el-form-item label="当前状态">
        <el-tag :type="courseStatusType(editForm.status)" effect="plain">{{ courseStatusLabel(editForm.status) }}</el-tag>
      </el-form-item>
      <el-alert title="当前编辑弹窗用于前端管理体验展示，课程修改保存接口将在下一阶段接入。" type="info" show-icon :closable="false" />
    </el-form>
    <template #footer>
      <el-button @click="editVisible = false">取消</el-button>
      <el-button type="primary" @click="saveEdit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { getTeacherWorksApi } from '@/api/teacher'
import { courseStatusLabel, courseStatusType, formatCourseWork } from '@/utils/courseFormat'

defineEmits(['create'])
defineExpose({ loadWorks })

const router = useRouter()
const loading = ref(false)
const rawWorks = ref([])
const editVisible = ref(false)
const editForm = reactive({
  id: '',
  title: '',
  status: '',
  categoryName: '',
  priceText: '',
})

const works = computed(() => rawWorks.value.map(formatCourseWork))

onMounted(loadWorks)

async function loadWorks() {
  loading.value = true
  try {
    rawWorks.value = await getTeacherWorksApi()
  } finally {
    loading.value = false
  }
}

function openEdit(row) {
  Object.assign(editForm, row)
  editVisible.value = true
}

function previewWork(row) {
  router.push(`/courses/${row.id}`)
}

function saveEdit() {
  editVisible.value = false
  ElMessage.success('编辑内容已暂存，后续接入课程修改接口后可保存到后端')
}
</script>
