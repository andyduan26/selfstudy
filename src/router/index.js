import { createRouter, createWebHistory } from 'vue-router'
import BasicLayout from '@/layouts/BasicLayout.vue'
import LoginView from '@/views/LoginView.vue'
import HomeView from '@/views/HomeView.vue'
import CourseListView from '@/views/CourseListView.vue'
import CourseDetailView from '@/views/CourseDetailView.vue'
import VideoPlayerView from '@/views/VideoPlayerView.vue'
import TeacherProfileView from '@/views/TeacherProfileView.vue'
import UserCenterView from '@/views/UserCenterView.vue'
import TeacherCenterView from '@/views/TeacherCenterView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    component: BasicLayout,
    children: [
      {
        path: '',
        name: 'home',
        component: HomeView,
        meta: { title: '首页' },
      },
      {
        path: 'courses',
        name: 'courses',
        component: CourseListView,
        meta: { title: '课程分类' },
      },
      {
        path: 'courses/:id',
        name: 'course-detail',
        component: CourseDetailView,
        meta: { title: '课程详情' },
      },
      {
        path: 'courses/:id/play',
        name: 'video-player',
        component: VideoPlayerView,
        meta: { title: '视频播放' },
      },
      {
        path: 'teachers/:id',
        name: 'teacher-profile',
        component: TeacherProfileView,
        meta: { title: '讲师主页' },
      },
      {
        path: 'user',
        name: 'user-center',
        component: UserCenterView,
        meta: { title: '用户中心', requiresAuth: true, roles: ['user', 'teacher'] },
      },
      {
        path: 'teacher',
        name: 'teacher-center',
        component: TeacherCenterView,
        meta: { title: '讲师中心', requiresAuth: true, roles: ['teacher'] },
      },
    ],
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { title: '登录' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
    meta: { title: '页面不存在' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  document.title = to.meta.title ? `${to.meta.title} - 我要自学网` : '我要自学网'

  if (!to.meta.requiresAuth) return true

  if (!authStore.isLoggedIn) {
    return {
      name: 'login',
      query: { redirect: to.fullPath },
    }
  }

  const allowedRoles = to.meta.roles || []
  if (allowedRoles.length > 0 && !allowedRoles.includes(authStore.role)) {
    return { name: 'home' }
  }

  return true
})

export default router
