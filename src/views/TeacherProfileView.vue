<template>
  <section v-if="teacher" class="page-section">
    <div class="teacher-profile">
      <div class="avatar-mark">{{ teacher.name.slice(0, 1) }}</div>
      <div>
        <p class="section-kicker">Teacher</p>
        <h1>{{ teacher.name }}</h1>
        <p class="section-desc">{{ teacher.title }} · {{ teacher.field }}</p>
        <p>{{ teacher.intro }}</p>
        <div class="tag-row roomy">
          <el-tag effect="plain">{{ teacher.courses }} 门课程</el-tag>
          <el-tag effect="plain">{{ teacher.students.toLocaleString() }} 名学员</el-tag>
        </div>
      </div>
    </div>

    <div class="section-heading">
      <div>
        <p class="section-kicker">Courses</p>
        <h2>讲师课程</h2>
      </div>
    </div>
    <div class="course-grid">
      <article v-for="course in teacherCourses" :key="course.id" class="course-card" @click="router.push(`/courses/${course.id}`)">
        <div class="course-cover">{{ course.cover }}</div>
        <div class="course-card__body">
          <el-tag size="small" effect="plain">{{ course.level }}</el-tag>
          <h3>{{ course.title }}</h3>
          <p>{{ course.summary }}</p>
          <div class="course-meta">
            <span>{{ course.price }}</span>
            <span>{{ course.students.toLocaleString() }} 人学习</span>
          </div>
        </div>
      </article>
    </div>
  </section>
  <NotFoundView v-else />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { courses, teachers } from '@/data/platform'
import NotFoundView from './NotFoundView.vue'

const route = useRoute()
const router = useRouter()
const teacher = computed(() => teachers.find((item) => item.id === Number(route.params.id)))
const teacherCourses = computed(() => courses.filter((item) => item.teacherId === teacher.value?.id))
</script>
