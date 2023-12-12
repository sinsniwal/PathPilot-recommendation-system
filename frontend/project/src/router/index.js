import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Recommend from "../components/Recommend.vue"
//import FeedbackComponent from '../views/FeedBackView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  { 
    path: '/recommend',
    name: 'recommend',
    component: Recommend
  },
  {
    path: '/login',
    name:'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name:'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/course/feedback/:course_code',
    name: 'feedback',
    component: () => import('../views/FeedBackView.vue')
  },
  {
    path: '/course/feedback',
    name: 'student-feedback',
    component: () => import('../views/StudentFeedBackView.vue')
  },
  {
    path: '/course/feedback/modify/:feedbackId',
    name: 'edit-delete-feedback',
    component: () => import('../views/EditDeleteFeedBackView.vue'),
  },
  {
    path: '/course/post/feedback',
    name: 'post-feedback',
    component: () => import('../views/PostFeedBackView.vue'),
  },
  {
    path: '/course/stats/course/:course_code',
    name: 'course-stats',
    component: () => import('../views/CourseStatsView.vue'),
  },
  {
    path: '/course/stats/level/:level',
    name: 'course-stats',
    component: () => import('../views/LevelStatsView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
