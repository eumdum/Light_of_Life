<template>
  <div class="auth-container">
    <h2>로그인</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="아이디" required />
      <input v-model="password" type="password" placeholder="비밀번호" required />
      <button type="submit">로그인</button>
    </form>
    <div class="auth-footer">
      <router-link to="/signup" class="link-text">
        아직 회원이 아니신가요? <strong>회원가입 하러가기</strong>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const username = ref('');
const password = ref('');
const router = useRouter();

const login = async () => {
  try {
    const res = await axios.post(`${API_BASE_URL}token/`, {
      username: username.value,
      password: password.value
    });
    localStorage.setItem('access_token', res.data.access);
    localStorage.setItem('user_id', username.value);
    axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`;
    router.push('/');
  } catch (e) {
    console.error(e);
    alert('로그인 실패!');
  }
};
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 80px auto;
  padding: 40px;
  background-color: #f9f7e8;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  color: #556b2f;
  margin-bottom: 30px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

button {
  padding: 12px;
  background-color: #869a69;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background-color: #6d7e56;
}

.link-text {
  margin-top: 20px;
  display: inline-block;
  color: #666;
  text-decoration: none;
  font-size: 0.9rem;
}

.link-text:hover {
  text-decoration: underline;
}


.auth-footer {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
}

.link-text {
  text-decoration: none;
  color: #6d7e56;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.link-text:hover {
  color: #556b2f;
  font-weight: 700;
}

.btn-secondary {
  display: inline-block;
  margin-top: 15px;
  padding: 10px 20px;
  background-color: transparent;
  border: 1px solid #869a69;
  color: #869a69;
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.9rem;
  transition: 0.3s;
}

.btn-secondary:hover {
  background-color: #869a69;
  color: white;
}
</style>