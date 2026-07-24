<template>
  <section class="page-section hero-section">
    <p class="section-kicker">Learning Platform</p>
    <h1>干净、稳定、可持续迭代的前端基础架构</h1>
    <p class="section-desc">已预留普通用户与讲师权限结构，后续可逐步接入课程、订单、学习记录等业务模块。</p>
  </section>

  <section class="page-section">
    <el-row :gutter="24">
      <el-col :xs="24" :md="8">
        <div class="feature-block">
          <h2>路由系统</h2>
          <p>使用 Vue Router 管理页面和基础布局。</p>
        </div>
      </el-col>
      <el-col :xs="24" :md="8">
        <div class="feature-block">
          <h2>请求封装</h2>
          <p>使用 Axios 统一处理接口地址、Token 和错误提示。</p>
        </div>
      </el-col>
      <el-col :xs="24" :md="8">
        <div class="feature-block">
          <h2>权限预留</h2>
          <p>预留 user 与 teacher 两种身份，支持后续扩展。</p>
        </div>
      </el-col>
    </el-row>
  </section>
</template>
