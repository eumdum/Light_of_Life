<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-blue-700 text-white p-4 shadow-md">
      <div class="container mx-auto flex justify-between items-center">
      </div>
    </header>
    
    <main>
      <router-view />
    </main>
    
    <footer class="bg-gray-800 text-white p-4 mt-8">
      <div class="container mx-auto text-center">
      </div>
    </footer>
  </div>
</template>

<<<<<<< Updated upstream
<script>
export default {
  name: 'App'
}
=======
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
watch(() => route.path, updateAuthStatus); 
>>>>>>> Stashed changes
</script>

<style>
body {
  background-color: #a8b69a; 
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  margin: 0;
<<<<<<< Updated upstream
  color: #333;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
=======
  background-color: #a8b69a; 
  font-family: 'Pretendard', sans-serif;
}

.header-nav {
  background-color: #f9f7e8; 
  height: 60px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
>>>>>>> Stashed changes
}

:root {
  --primary-color: #869a69;
  --text-dark: #333;
  --text-light: #f5f5f5;
  --bg-light: #ffffff;
  --border-color: #e5e7eb;
}
<<<<<<< Updated upstream
</style>
=======

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
  color: #556b2f; 
  margin-right: 10px;
}

.user-name strong {
  font-weight: 700;
  text-decoration: underline; 
}
</style>
>>>>>>> Stashed changes
