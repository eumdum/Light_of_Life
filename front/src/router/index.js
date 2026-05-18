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
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

<<<<<<< Updated upstream
export default router
=======
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
>>>>>>> Stashed changes
