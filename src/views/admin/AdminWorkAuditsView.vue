<template>
  <AdminPageHeader title="作品审核管理" desc="审核讲师提交的课程作品、目录和发布状态。" />
  <AuditTable :rows="workAudits" type="work" />
</template>

<script setup>
import AdminPageHeader from '@/components/admin/AdminPageHeader.vue'
import AuditTable from '@/components/admin/AuditTable.vue'
import { workAudits } from '@/data/admin'
</script>
