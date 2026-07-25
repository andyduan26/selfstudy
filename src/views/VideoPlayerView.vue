<template>
  <section v-if="course" class="player-page">
    <div class="player-shell">
      <div class="video-box">
        <video v-if="currentVideoUrl" class="course-video" :src="currentVideoUrl" controls preload="metadata" />
        <template v-else>
          <div class="play-symbol">▶</div>
          <h1>{{ course.title }}</h1>
          <p>暂无可播放视频文件</p>
        </template>
      </div>
      <aside class="lesson-sidebar">
        <h2>课程目录</h2>
        <button
          v-for="lesson in lessons"
          :key="lesson.id"
          :class="{ 'is-active': lesson.id === activeLessonId, 'is-locked': !lesson.isFreePreview }"
          @click="handleLesson(lesson)"
        >
          <span>第 {{ lesson.index }} 讲</span>
          <strong>{{ lesson.title }}</strong>
        </button>
      </aside>
    </div>

    <div class="preview-banner">
      <div>
        <h2>试看提示</h2>
        <p>当前播放已接入后端上传视频。未开放试看章节会显示锁定提示，后续可继续接入购买权限。</p>
      </div>
      <el-button type="primary" @click="router.push(`/courses/${course.id}`)">返回课程详情</el-button>
    </div>
  </section>
  <NotFoundView v-else />
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getCourseApi } from '@/api/course'
import NotFoundView from './NotFoundView.vue'

const route = useRoute()
const router = useRouter()
const rawCourse = ref(null)
const activeLessonId = ref(null)
const course = computed(() => rawCourse.value ? { id: rawCourse.value.id, title: rawCourse.value.title } : null)
const lessons = computed(() => (rawCourse.value?.chapters || []).map((chapter, index) => ({
  id: chapter.id,
  index: index + 1,
  title: chapter.title || (index === 0 ? '试看：课程介绍' : '正式课程内容'),
  isFreePreview: chapter.is_free_preview || index === 0,
  videoUrl: chapter.videos?.[0]?.video_file || chapter.videos?.[0]?.video_url || '',
})))
const currentLesson = computed(() => lessons.value.find((lesson) => lesson.id === activeLessonId.value) || lessons.value[0])
const currentVideoUrl = computed(() => currentLesson.value?.videoUrl || '')

onMounted(loadCourse)

watch(
  () => route.params.id,
  () => loadCourse(),
)

async function loadCourse() {
  rawCourse.value = null
  activeLessonId.value = null
  try {
    rawCourse.value = await getCourseApi(route.params.id)
    activeLessonId.value = lessons.value[0]?.id || null
  } catch {
    rawCourse.value = null
  }
}

function handleLesson(lesson) {
  if (!lesson.isFreePreview) {
    ElMessage.warning('试看仅开放第 1 讲，完整课程后续接入权限。')
    return
  }
  activeLessonId.value = lesson.id
}
</script>
