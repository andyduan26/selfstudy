<template>
  <div class="center-panel">
    <div class="panel-heading">
      <div>
        <h2>提现中心</h2>
        <p>管理提现账户，提交提现申请并查看到账记录。</p>
      </div>
      <el-button type="primary" @click="$emit('withdraw')">申请提现</el-button>
    </div>

    <div class="withdraw-card">
      <div>
        <span>当前可提现</span>
        <strong>¥5,300</strong>
      </div>
      <p>提现申请通常 1-3 个工作日处理，当前为静态演示。</p>
    </div>

    <el-table :data="withdrawRows" border>
      <el-table-column prop="id" label="提现单号" min-width="180" />
      <el-table-column prop="amount" label="金额" width="120" />
      <el-table-column prop="account" label="到账账户" min-width="200" />
      <el-table-column prop="status" label="状态" width="120" />
      <el-table-column prop="date" label="申请日期" width="130" />
    </el-table>
  </div>
</template>

<script setup>
import { withdrawRows } from '@/data/dashboard'

defineEmits(['withdraw'])
</script>
