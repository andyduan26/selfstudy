<template>
  <section v-if="course" class="player-page">
    <div class="player-shell">
      <div class="video-box">
        <div class="play-symbol">▶</div>
        <h1>{{ course.title }}</h1>
        <p>第 1 讲 · 试看课程</p>
      </div>
      <aside class="lesson-sidebar">
        <h2>课程目录</h2>
        <button v-for="lesson in lessons" :key="lesson" :class="{ 'is-active': lesson === 1, 'is-locked': lesson > 1 }" @click="handleLesson(lesson)">
          <span>第 {{ lesson }} 讲</span>
          <strong>{{ lesson === 1 ? '试看：课程介绍' : '正式课程内容' }}</strong>
        </button>
      </aside>
    </div>

    <div class="preview-banner">
      <div>
        <h2>试看提示</h2>
        <p>当前页面为静态视频播放 UI，第 2 讲起展示锁定状态，后续可对接学习进度和购买权限。</p>
      </div>
      <el-button type="primary" @click="router.push(`/courses/${course.id}`)">返回课程详情</el-button>
    </div>
  </section>
  <NotFoundView v-else />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { courses } from '@/data/platform'
import NotFoundView from './NotFoundView.vue'

const route = useRoute()
const router = useRouter()
const course = computed(() => courses.find((item) => item.id === Number(route.params.id)))
const lessons = [1, 2, 3, 4, 5, 6]

function handleLesson(lesson) {
  if (lesson > 1) {
    ElMessage.warning('试看仅开放第 1 讲，完整课程后续接入权限。')
  }
}
</script>
