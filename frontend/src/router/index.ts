import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from '@/layouts/layout.vue'
// @ts-ignore
import HomePage from '@/views/Home.vue'
// @ts-ignore
import AskPage from '@/views/Ask.vue'
// @ts-ignore
import ContentPage from '@/views/content/Content.vue'
// @ts-ignore
import ContentCreate from '@/views/content/Create.vue'

const routes = [
  {
    path: '/',
    component: DashboardLayout,
    children: [
      {
        path: 'home',
        component: HomePage
      },
      {
        path: 'ask',
        component: AskPage
      },
      {
        path: 'content',
        component: ContentPage
      },
      {
        path: 'content/create',
        component: ContentCreate
      },
      {
        path: '',
        redirect: '/home'
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
