import { createRouter, createWebHistory } from 'vue-router'
import DiaryWrite from '../views/DiaryWrite.vue'
import DiaryList from '../views/DiaryList.vue'

const routes = [
  {
    path: '/',
    name: 'DiaryWrite',
    component: DiaryWrite
  },
  {
    path: '/list',
    name: 'DiaryList',
    component: DiaryList
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), //(process.env.BASE_URL)
  routes
})

export default router