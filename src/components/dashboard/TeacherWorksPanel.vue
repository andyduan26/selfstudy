<template>
  <div class="center-panel">
    <div class="panel-heading">
      <div>
        <h2>作品管理</h2>
        <p>管理课程作品的状态、学员数和收益。</p>
      </div>
      <el-button type="primary" @click="$emit('create')">新建作品</el-button>
    </div>

    <el-table :data="teacherWorks" border>
      <el-table-column prop="title" label="课程名称" min-width="220" />
      <el-table-column prop="status" label="状态" width="110">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" effect="plain">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="students" label="学员" width="110" />
      <el-table-column prop="income" label="收益" width="120" />
      <el-table-column prop="updatedAt" label="更新时间" width="130" />
      <el-table-column label="操作" width="150">
        <template #default>
          <el-button text>编辑</el-button>
          <el-button text>预览</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { teacherWorks } from '@/data/dashboard'

defineEmits(['create'])

function statusType(status) {
  if (status === '已发布') return 'success'
  if (status === '审核中') return 'warning'
  return 'info'
}
</script>
