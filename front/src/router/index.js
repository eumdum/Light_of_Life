import { createRouter, createWebHistory } from 'vue-router'
import StoreRegister from '../views/StoreRegister.vue'
import StoreList from '../views/StoreList.vue'

const routes = [
  {
    path: '/',
    name: 'StoreRegister',
    component: StoreRegister
  },
  {
    path: '/list',
    name: 'StoreList',
    component: StoreList
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), //(process.env.BASE_URL)
  routes
})

export default router