<template>
  <AdminPageHeader title="讲师审核管理" desc="审核普通用户提交的讲师入驻申请。" />
  <AuditTable :rows="teacherAudits" type="teacher" />
</template>

<script setup>
import AdminPageHeader from '@/components/admin/AdminPageHeader.vue'
import AuditTable from '@/components/admin/AuditTable.vue'
import { teacherAudits } from '@/data/admin'
</script>
