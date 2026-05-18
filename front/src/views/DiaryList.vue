<template>
  <div class="page-container">
    <header class="app-header">
      <div class="header-side"></div>

      <h2>🌿 {{ calendarTitle }}일기 목록</h2>

      <div class="header-side">
        <router-link to="/" class="calendar-view-btn">
          📅 달력 보기
        </router-link>
      </div>
    </header>

    <main class="content-wrapper">
      <div v-if="diaries.length > 0" class="diary-list">
        <article v-for="diary in diaries" :key="diary.id" class="diary-card" @click="openDetailModal(diary)">
          <div class="card-header">
            <div class="header-top">
              <h3>{{ diary.title }}</h3>
              <button class="card-delete-btn" @click.stop="openDeleteModal(diary)">❌</button>
            </div>
            <div class="header-bottom">
              <span class="card-date">{{ formatDate(diary.date) }}</span>
              <span v-if="diary.emotion" class="emotion-tag">{{ diary.emotion }}</span>
            </div>
          </div>
          <p class="card-content">{{ diary.content }}</p>
        </article>
      </div>

      <div v-else class="empty-list-message">
        <p>아직 기록된 일기가 없어요.</p>
      </div>
    </main>

    <div v-if="showDetailModal" class="modal-overlay" @click="closeDetailModal">
      <div class="modal-content detail-modal" @click.stop>
        <header class="modal-header">
          <h2>{{ selectedDiary?.title }}</h2>
          <span class="detail-date">{{ formatDate(selectedDiary?.date) }}</span>
        </header>

        <div class="modal-body">
          <section class="diary-text-section">
            <p class="diary-text">{{ selectedDiary?.content }}</p>
          </section>

          <section v-if="selectedDiary?.emotion" class="ai-analysis-section">
            <div class="ai-header">
              <span class="ai-badge">AI 감정 분석</span>
              <span class="ai-emotion">오늘의 감정: <strong>{{ selectedDiary.emotion }}</strong></span>
            </div>
            <div class="ai-recommendation">
              <p class="song-title">🎵 추천 곡: {{ selectedDiary.recommendation_song }}</p>
              <div class="scroll-box">
                <p class="reason-text">{{ selectedDiary.recommendation_reason }}</p>
              </div>
              <a :href="selectedDiary.youtube_url" target="_blank" class="youtube-btn">
                유튜브에서 감상하기
              </a>
            </div>
          </section>
        </div>

        <footer class="modal-footer">
          <button class="close-btn" @click="closeDetailModal">확인</button>
        </footer>
      </div>
    </div>

    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDetailModal">
      <div class="modal-content delete-confirm-modal" @click.stop>
        <h3>일기를 삭제할까요?</h3>
        <p>삭제한 기록은 되살릴 수 없습니다.</p>
        <div class="modal-actions">
          <button class="cancel-btn" @click="closeDetailModal">취소</button>
          <button class="confirm-delete-btn" @click="deleteDiary">삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const diaries = ref([]);
const selectedDiary = ref(null);
const showDetailModal = ref(false);
const showDeleteModal = ref(false);

const calendarTitle = computed(() => {
  const savedId = localStorage.getItem('user_id');
  const token = localStorage.getItem('access_token');
  return (token && savedId) ? `${savedId}님의 ` : '';
});

const fetchDiaries = async () => {
  try {
    const token = localStorage.getItem('access_token'); 
    const res = await axios.get(`${API_BASE_URL}diaries/`, {
      headers: {
        Authorization: `Bearer ${token}` 
      }
    });
    diaries.value = res.data;
  } catch (error) {
    console.error("데이터 로드 실패", error);
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return `${date.getFullYear()}. ${date.getMonth() + 1}. ${date.getDate()}.`;
};

const openDetailModal = (diary) => {
  selectedDiary.value = diary;
  showDetailModal.value = true;
};

const openDeleteModal = (diary) => {
  selectedDiary.value = diary;
  showDeleteModal.value = true;
};

const closeDetailModal = () => {
  showDetailModal.value = false;
  showDeleteModal.value = false;
  selectedDiary.value = null;
};

const deleteDiary = async () => {
  const token = localStorage.getItem('access_token');

  try {
    await axios.delete(`${API_BASE_URL}diaries/${selectedDiary.value.id}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    await fetchDiaries(); 
    closeDetailModal();
    alert("일기가 삭제되었습니다.");
  } catch (error) {
    console.error("삭제 실패:", error.response?.data || error);
    alert("삭제 중 오류가 발생했습니다.");
  }
};

onMounted(fetchDiaries);
</script>

<style scoped>
.page-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.app-header h1 {
  color: #fff;
  font-size: 2.2rem;
}

.write-button {
  background: #869a69;
  color: white;
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
}

.diary-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.diary-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  display: flex;
  flex-direction: column;
  height: 220px;
}

.diary-card:hover {
  transform: translateY(-5px);
}

.card-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 0.8rem;
  margin-bottom: 1rem;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-top h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.card-delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.8rem;
}

.header-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.card-date {
  color: #888;
  font-size: 0.85rem;
}

.emotion-tag {
  background: #f0f4e8;
  color: #869a69;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: bold;
}

.card-content {
  color: #555;
  line-height: 1.5;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  margin: 0;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 550px;
  padding: 2rem;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

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
  margin-bottom: 0.8rem;
}

.scroll-box {
  max-height: 150px;
  overflow-y: auto;
  background: white;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #eee;
  margin-bottom: 1rem;
}

.reason-text {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.6;
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
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.cancel-btn {
  background: #eee;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
}

.confirm-delete-btn {
  background: #d9534f;
  color: white;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
}

.scroll-box::-webkit-scrollbar {
  width: 5px;
}

.scroll-box::-webkit-scrollbar-thumb {
  background: #869a69;
  border-radius: 10px;
}

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