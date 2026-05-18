import { createRouter, createWebHistory } from 'vue-router'
import DiaryWrite from '../views/DiaryWrite.vue'
import DiaryList from '../views/DiaryList.vue'
import Login from '@/views/Login.vue'
import Singup from '@/views/Singup.vue'
import DiaryCalendar from '@/views/DiaryCalendar.vue'

const routes = [
  {
    path: '/write',
    name: 'DiaryWrite',
    component: DiaryWrite
  },
  {
    path: '/list',
    name: 'DiaryList',
    component: DiaryList
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Singup
  },
  {
    path: '/',
    name: 'calendar',
    component: DiaryCalendar
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access_token');

  if (to.path === '/') {
    next();
  }
  
  else if (to.path !== '/login' && to.path !== '/signup' && !isLoggedIn) {
    alert('로그인이 필요한 서비스입니다.');
    next('/login');
  } else {
    next();
  }
});

export default router;