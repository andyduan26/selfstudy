<template>
  <section v-if="course" class="player-page">
    <div class="player-shell">
      <div class="video-box">
        <video
          v-if="currentVideoUrl && !videoError"
          ref="videoRef"
          class="course-video"
          :poster="course.coverUrl"
          controls
          preload="metadata"
          @error="handleVideoError"
        />
        <template v-else>
          <div class="play-symbol">▶</div>
          <h1>{{ course.title }}</h1>
          <p>{{ videoError ? '视频源文件暂不可用，请重新上传或等待转码完成。' : '暂无可播放视频文件' }}</p>
        </template>
      </div>
      <aside class="lesson-sidebar">
        <h2>课程目录</h2>
        <div v-for="chapter in chapterGroups" :key="chapter.id" class="player-chapter-group">
          <h3>{{ chapter.index }}. {{ chapter.title }}</h3>
          <button
            v-for="lesson in chapter.lessons"
            :key="lesson.id"
            :class="{ 'is-active': lesson.id === activeLessonId, 'is-locked': !lesson.isFreePreview }"
            @click="handleLesson(lesson)"
          >
            <span>第 {{ lesson.index }} 节</span>
            <strong>{{ lesson.title }}</strong>
          </button>
        </div>
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
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getCourseApi } from '@/api/course'
import NotFoundView from './NotFoundView.vue'

const route = useRoute()
const router = useRouter()
const rawCourse = ref(null)
const activeLessonId = ref(null)
const videoRef = ref(null)
const hlsPlayer = ref(null)
const videoError = ref(false)
const course = computed(() => rawCourse.value ? {
  id: rawCourse.value.id,
  title: rawCourse.value.title,
  coverUrl: rawCourse.value.cover || rawCourse.value.cover_url || '',
} : null)
const chapterGroups = computed(() => (rawCourse.value?.chapters || []).map((chapter, chapterIndex) => ({
  id: chapter.id,
  index: chapterIndex + 1,
  title: chapter.title || `第 ${chapterIndex + 1} 章`,
  lessons: (chapter.videos || []).map((video, lessonIndex) => ({
    id: video.id,
    index: lessonIndex + 1,
    title: video.title || `第 ${lessonIndex + 1} 节`,
    isFreePreview: video.is_free_preview || chapter.is_free_preview || (chapterIndex === 0 && lessonIndex === 0),
    videoUrl: resolveMediaUrl(video.hls_url || video.video_file || video.video_url || ''),
    isHls: Boolean(video.hls_url),
  })),
})))
const lessons = computed(() => chapterGroups.value.flatMap((chapter) => chapter.lessons))
const currentLesson = computed(() => lessons.value.find((lesson) => lesson.id === activeLessonId.value) || lessons.value[0])
const currentVideoUrl = computed(() => currentLesson.value?.videoUrl || '')

onMounted(loadCourse)
onBeforeUnmount(destroyHls)

watch(
  () => route.params.id,
  () => loadCourse(),
)

watch(currentVideoUrl, () => setupVideoSource())

async function loadCourse() {
  rawCourse.value = null
  activeLessonId.value = null
  try {
    rawCourse.value = await getCourseApi(route.params.id)
    activeLessonId.value = lessons.value[0]?.id || null
    await setupVideoSource()
  } catch {
    rawCourse.value = null
  }
}

function handleLesson(lesson) {
  if (!lesson.isFreePreview) {
    ElMessage.warning('该节暂未开放试看，完整课程后续接入购买权限。')
    return
  }
  activeLessonId.value = lesson.id
}

async function setupVideoSource() {
  await nextTick()
  destroyHls()
  videoError.value = false
  const video = videoRef.value
  const url = currentVideoUrl.value
  if (!video || !url) return

  if (currentLesson.value?.isHls) {
    if (video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = url
      return
    }
    const { default: Hls } = await import('hls.js')
    if (Hls.isSupported()) {
      hlsPlayer.value = new Hls()
      hlsPlayer.value.on(Hls.Events.ERROR, (_, data) => {
        if (data?.fatal) handleVideoError()
      })
      hlsPlayer.value.loadSource(url)
      hlsPlayer.value.attachMedia(video)
      return
    }
    ElMessage.warning('当前浏览器不支持 HLS 播放')
    return
  }

  video.src = url
}

function handleVideoError() {
  videoError.value = true
  destroyHls()
}

function destroyHls() {
  if (hlsPlayer.value) {
    hlsPlayer.value.destroy()
    hlsPlayer.value = null
  }
}

function resolveMediaUrl(url) {
  if (!url || /^https?:\/\//.test(url)) return url
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
  return `${baseUrl.replace(/\/$/, '')}${url.startsWith('/') ? url : `/${url}`}`
}
</script>
