<template>
  <div class="page-container">
    <header class="app-header">
      <h1>나의 기록들</h1>
      <router-link to="/" class="write-button">새 일기 작성하기</router-link>
    </header>

    <main class="content-wrapper">
      <div v-if="diaries.length > 0" class="diary-list">
        <article v-for="diary in diaries" :key="diary.id" class="diary-card">
          <header class="card-header">
            <h3>{{ diary.title }}</h3>
            <span class="card-date">{{ formatDate(diary.date) }}</span>
          </header>
          <p class="card-content">{{ diary.content }}</p>
        </article>
      </div>
      <div v-else class="empty-list-message">
        <p>아직 기록된 일기가 없어요.</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 현재 브라우저의 주소(hostname)를 사용해서 API 서버의 기본 주소를 동적으로 만듬.
const API_BASE_URL = `http://${window.location.hostname}:8000`;

// 이제 각 API의 최종 주소는 이 기본 주소를 바탕으로 만들어짐.
const API_URL = `${API_BASE_URL}/api/diaries/`;

const diaries = ref([]);

function formatDate(dateString) {
  const date = new Date(dateString);
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`;
}

async function fetchDiaries() {
  try {
    const response = await axios.get(API_URL);
    diaries.value = response.data;
  } catch (error) {
    console.error("일기를 불러오는 데 실패했습니다:", error);
  }
}

onMounted(() => {
  fetchDiaries();
});
</script>

<style scoped>
.page-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 1rem;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 0 1rem;
}

.app-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffffff
  /* color: var(--primary-color, #869a69); */
}

.write-button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  background-color: var(--primary-color, #869a69);
  color: var(--text-light, #fff);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
}

.write-button:hover {
  background-color: #708255;
  transform: translateY(-2px);
}

.diary-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.diary-card {
  background-color: var(--bg-light, #fff);
  border: 1px solid var(--border-color, #e0e0e0);
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.04);
  transition: all 0.2s;
}

.diary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.8rem;
}

.card-header h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
}

.card-date {
  font-size: 0.85rem;
  color: #777;
}

.card-content {
  font-size: 1rem;
  line-height: 1.6;
  color: #555;
  white-space: pre-wrap;
  max-height: 150px;
  overflow-y: auto;
}

.empty-list-message {
  text-align: center;
  padding: 4rem;
  background-color: var(--bg-light, #fff);
  border-radius: 12px;
  color: #888;
  font-size: 1.2rem;
}
</style>
