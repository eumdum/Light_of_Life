<template>
  <div class="page-container">
    <header class="app-header">
      <h1>나의 기록들</h1>
      <router-link to="/" class="write-button">새 일기 작성하기</router-link>
    </header>

    <main class="content-wrapper">
      <div v-if="diaries.length > 0" class="diary-list">
        <article v-for="diary in diaries" :key="diary.id" class="diary-card">
          <button
            class="delete-button"
            @click="openDeleteModal(diary)"
            aria-label="일기 삭제"
          >
            ❌
          </button>

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

    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-content" @click.stop>
        <h3>일기를 삭제할까요?</h3>
        <p>
          <strong>{{ selectedDiary?.title }}</strong>
          일기를 삭제하면 다시 복구할 수 없어요.
        </p>

        <div class="modal-actions">
          <button class="cancel-button" @click="closeDeleteModal">취소</button>
          <button
            class="confirm-delete-button"
            @click="deleteDiary"
            :disabled="isDeleting"
          >
            {{ isDeleting ? '삭제 중...' : '삭제' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

<<<<<<< Updated upstream
// 현재 브라우저의 주소(hostname)를 사용해서 API 서버의 기본 주소를 동적으로 만듬.
const API_BASE_URL = `http://${window.location.hostname}:8000`;
const API_URL = `${API_BASE_URL}/api/diaries/`;
=======
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
>>>>>>> Stashed changes

const diaries = ref([]);
const showDeleteModal = ref(false);
const selectedDiary = ref(null);
const isDeleting = ref(false);

function formatDate(dateString) {
  const date = new Date(dateString);
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`;
}

<<<<<<< Updated upstream
async function fetchDiaries() {
  try {
    const response = await axios.get(API_URL);
    diaries.value = response.data;
=======
const fetchDiaries = async () => {
  try {
    const token = localStorage.getItem('access_token'); 
    const res = await axios.get('http://localhost:8000/api/diaries/', {
      headers: {
        Authorization: `Bearer ${token}` 
      }
    });
    diaries.value = res.data;
>>>>>>> Stashed changes
  } catch (error) {
    console.error("일기를 불러오는 데 실패했습니다:", error);
  }
}

function openDeleteModal(diary) {
  selectedDiary.value = diary;
<<<<<<< Updated upstream
=======
  showDetailModal.value = true;
};

const openDeleteModal = (diary) => {
  selectedDiary.value = diary;
  showDeleteModal.value = true; 
>>>>>>> Stashed changes
  showDeleteModal.value = true;
}

function closeDeleteModal() {
  showDeleteModal.value = false;
  selectedDiary.value = null;
}

<<<<<<< Updated upstream
async function deleteDiary() {
  if (!selectedDiary.value) return;

  try {
    isDeleting.value = true;

    await axios.delete(`${API_URL}${selectedDiary.value.id}/`);

    diaries.value = diaries.value.filter(
      (diary) => diary.id !== selectedDiary.value.id
    );

    closeDeleteModal();
  } catch (error) {
    console.error('일기 삭제에 실패했습니다:', error);
    alert('일기 삭제에 실패했습니다.');
  } finally {
    isDeleting.value = false;
=======
const deleteDiary = async () => {
  const token = localStorage.getItem('access_token');

  try {
    await axios.delete(`${API_URL}${selectedDiary.value.id}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    await fetchDiaries();
    closeDetailModal();
    alert("일기가 삭제되었습니다.");
  } catch (error) {
    console.error("삭제 실패:", error.res?.data || error);
    alert("삭제 중 오류가 발생했습니다.");
>>>>>>> Stashed changes
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
  position: relative;
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

.delete-button {
  position: absolute;
  top: 12px;
  right: 12px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 0.95rem;
  line-height: 1;
  padding: 0.2rem;
  transition: transform 0.2s ease;
}

.delete-button:hover {
  transform: scale(1.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.8rem;
  padding-right: 1.8rem;
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

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  width: 90%;
  max-width: 420px;
  background: #fff;
  border-radius: 16px;
  padding: 1.8rem;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
  text-align: center;
}

<<<<<<< Updated upstream
.modal-content h3 {
=======
.modal-header {
  border-bottom: 2px solid #f0f4e8;
  padding-bottom: 1rem;
  margin-bottom: 1.5rem;
}

.modal-header h2 {
  margin: 0;
  color: #333;
}

.detail-date {
  color: #999;
  font-size: 0.9rem;
}

.diary-text-section {
  margin-bottom: 2rem;
}

.diary-text {
  line-height: 1.8;
  color: #444;
  white-space: pre-wrap;
}

.ai-analysis-section {
  background: #f7f8f6;
  border-radius: 12px;
  padding: 1.5rem;
  border-left: 5px solid #869a69;
}

.ai-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.ai-badge {
  background: #869a69;
  color: white;
  width: fit-content;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: bold;
}

.ai-emotion {
  color: #333;
  font-size: 1rem;
}

.ai-recommendation .song-title {
  font-weight: bold;
  color: #444;
>>>>>>> Stashed changes
  margin-bottom: 0.8rem;
  font-size: 1.3rem;
  color: #222;
}

.modal-content p {
  color: #555;
  line-height: 1.6;
<<<<<<< Updated upstream
  margin-bottom: 1.5rem;
=======
  margin: 0;
}

.youtube-btn {
  display: block;
  background: #FF0000;
  color: white;
  text-align: center;
  padding: 0.8rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
}

.modal-footer {
  margin-top: 2rem;
  text-align: center;
}

.close-btn {
  background: #869a69;
  color: white;
  border: none;
  padding: 0.8rem 2.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

.delete-confirm-modal {
  max-width: 350px;
  text-align: center;
>>>>>>> Stashed changes
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 0.8rem;
}

.cancel-button,
.confirm-delete-button {
  min-width: 100px;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 10px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-button {
  background: #e9ecef;
  color: #333;
}

.cancel-button:hover {
  background: #dde2e6;
}

.confirm-delete-button {
  background: #d9534f;
  color: white;
}

<<<<<<< Updated upstream
.confirm-delete-button:hover {
  background: #c9302c;
=======
.scroll-box::-webkit-scrollbar {
  width: 5px;
>>>>>>> Stashed changes
}

.confirm-delete-button:disabled {
  background: #e3a3a1;
  cursor: not-allowed;
}
<<<<<<< Updated upstream
</style>
=======

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px 0;
}

.header-side {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

h2 {
  flex: 2;
  text-align: center;
  margin: 0;
  color: #556b2f;
}

.calendar-view-btn {
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
  color: #869a69;
  background-color: white;
  padding: 8px 16px;
  border: 1px solid #869a69;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.calendar-view-btn:hover {
  background-color: #869a69;
  color: white;
}
</style>
>>>>>>> Stashed changes
