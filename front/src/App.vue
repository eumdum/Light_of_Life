<template>
  <div id="app">
    <nav class="header-nav">
      <div class="nav-content">
        <router-link to="/" class="logo">🌿 마음일기</router-link>
        
        <div class="auth-menu">
          <template v-if="isLoggedIn">
            <span class="user-name"><strong>{{ userId }}</strong>님! 반가워요!</span>
            <button @click="logout" class="auth-btn logout">로그아웃</button>
          </template>
          <template v-else>
            <router-link to="/login" class="auth-btn">로그인</router-link>
            <router-link to="/signup" class="auth-btn signup">회원가입</router-link>
          </template>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const isLoggedIn = ref(false);
const userId = ref('');
const router = useRouter();
const route = useRoute();

const updateAuthStatus = () => {
  const token = localStorage.getItem('access_token');
  isLoggedIn.value = !!token;
  
  // [추가] 로그인 상태라면 저장된 ID 꺼내오기
  if (isLoggedIn.value) {
    userId.value = localStorage.getItem('user_id') || '사용자';
  }
};

const logout = () => {
  alert('오늘 하루도 수고 많았어요. 다음에 또 만나요! 👋');
  localStorage.removeItem('access_token');
  localStorage.removeItem('user_id');
  updateAuthStatus();
  window.location.href = '/';
};

onMounted(updateAuthStatus);
watch(() => route.path, updateAuthStatus); // 주소 바뀔 때마다 체크
</script>

<style>
/* 전역 배경색 설정 */
body {
  margin: 0;
  background-color: #a8b69a; /* 은정이가 고른 배경색 */
  font-family: 'Pretendard', sans-serif;
}

.header-nav {
  background-color: #f9f7e8; /* 은정이가 고른 1번 헤더색 */
  height: 60px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.nav-content {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.2rem;
  font-weight: 800;
  color: #556b2f;
  text-decoration: none;
}

.auth-menu {
  display: flex;
  align-items: center;
  gap: 15px;
}

.auth-btn {
  text-decoration: none;
  color: #444;
  font-size: 0.9rem;
  padding: 6px 12px;
  border-radius: 6px;
  transition: 0.2s;
}

.signup {
  background-color: #869a69;
  color: white;
}

.logout {
  background: none;
  border: 1px solid #869a69;
  cursor: pointer;
}

.welcome-msg {
  font-size: 0.85rem;
  color: #666;
}

.user-name {
  font-size: 0.9rem;
  color: #556b2f; /* 우리 포인트 컬러인 짙은 녹색 */
  margin-right: 10px;
}

.user-name strong {
  font-weight: 700;
  text-decoration: underline; /* ID 강조하고 싶으면 추가 */
}
</style>