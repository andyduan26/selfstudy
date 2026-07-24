<template>
  <div class="center-panel">
    <div class="panel-heading">
      <div>
        <h2>收益中心</h2>
        <p>查看课程收益明细与结算状态。</p>
      </div>
      <el-tag effect="plain">可提现 ¥5,300</el-tag>
    </div>

    <div class="income-summary">
      <div>
        <span>累计收益</span>
        <strong>¥18,920</strong>
      </div>
      <div>
        <span>待结算</span>
        <strong>¥4,200</strong>
      </div>
      <div>
        <span>已提现</span>
        <strong>¥5,200</strong>
      </div>
    </div>

    <el-table :data="incomeRows" border>
      <el-table-column prop="month" label="月份" width="120" />
      <el-table-column prop="course" label="课程" min-width="240" />
      <el-table-column prop="amount" label="金额" width="120" />
      <el-table-column prop="status" label="状态" width="120" />
    </el-table>
  </div>
</template>

<script setup>
import { incomeRows } from '@/data/dashboard'
</script>
