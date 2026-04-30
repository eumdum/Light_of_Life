<template>
  <div class="calendar-container">
    <div class="calendar-card">
      <div class="calendar-header">
        <div class="header-side"></div>
        <h2>🌿 {{ calendarTitle }}마음 달력</h2>

        <div class="header-side">
          <router-link v-if="isLoggedIn" to="/list" class="list-view-btn">
            📋 목록 보기
          </router-link>
        </div>
      </div>

      <VCalendar expanded borderless :attributes="attributes" @dayclick="onDayClick" class="custom-calendar" />
    </div>

    <div v-if="selectedDiary" class="diary-detail-card">
      <div class="detail-header">
        <span class="detail-date">{{ selectedDiary.date }}</span>
        <span class="detail-emotion">#{{ selectedDiary.emotion }}</span>
      </div>

      <div class="diary-content-section">
        <h3 class="detail-title">{{ selectedDiary.title }}</h3>
        <p class="detail-content">{{ selectedDiary.content }}</p>
      </div>

      <hr class="divider" />

      <div class="song-recommendation">
        <div class="song-header">
          <h3 class="detail-song">🎵 {{ selectedDiary.recommendation_song }}</h3>
          <a :href="selectedDiary.youtube_url" target="_blank" class="youtube-icon-btn">
            <span class="play-icon">▶</span> 들어보기
          </a>
        </div>
        <p class="detail-reason">{{ selectedDiary.recommendation_reason }}</p>
      </div>

    </div>

    <div v-else class="no-selection">
      <p>이날은 아직 마음 기록이 없어요.</p>
      <button @click="$router.push('/write')" class="write-link-btn">
        오늘의 마음 기록하기 ✏️
      </button>
    </div>

    <router-link v-if="isLoggedIn" to="/write" class="floating-btn">
      <span class="plus-icon">+</span>
    </router-link>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const diaries = ref([]);
const attributes = ref([]);
const selectedDiary = ref(null);

const calendarTitle = computed(() => {
  const savedId = localStorage.getItem('user_id');
  const token = localStorage.getItem('access_token');

  return (token && savedId) ? `${savedId}님의 ` : '';
});

const isLoggedIn = computed(() => !!localStorage.getItem('access_token'));

const fetchDiaries = async () => {
  const token = localStorage.getItem('access_token');

  if (!token) {
    diaries.value = [];
    attributes.value = [];
    selectedDiary.value = null;
    return;
  }

  try {
    const response = await axios.get(`${API_BASE_URL}diaries/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    diaries.value = response.data;
    attributes.value = diaries.value.map(diary => ({
      highlight: {
        color: 'green',
        fillMode: 'light',
      },
      dates: new Date(diary.date),
      customData: diary
    }));
  } catch (error) {
    console.error("데이터 로드 실패", error);
    diaries.value = [];
    attributes.value = [];
  }
};

const onDayClick = (day) => {
  console.log("클릭한 날짜 ID:", day.id);
  console.log("현재 가지고 있는 전체 일기들:", diaries.value);

  const found = diaries.value.find(d => d.date === day.id);

  if (found) {
    console.log("✅ 찾은 데이터:", found);
    selectedDiary.value = found;
  } else {
    console.log("❌ 이 날짜엔 일기가 없네?");
    selectedDiary.value = null;
  }
};

onMounted(fetchDiaries);
</script>

<style scoped>
.calendar-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 0 20px;
}

.calendar-card {
  background-color: #f9f7e8;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #556b2f;
  margin-bottom: 20px;
}

.custom-calendar {
  background-color: transparent !important;
}

.diary-detail-card {
  margin-top: 20px;
  padding: 20px;
  background-color: #f9f7e8;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  animation: slideUp 0.3s ease-out;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 0.9rem;
  color: #666;
}

.detail-song {
  color: #556b2f;
  margin: 10px 0;
}

.detail-reason {
  font-size: 0.95rem;
  line-height: 1.5;
  color: #444;
  margin-bottom: 15px;
}

.youtube-link {
  display: inline-block;
  padding: 8px 15px;
  background-color: #ff0000;
  color: white;
  text-decoration: none;
  border-radius: 20px;
  font-size: 0.85rem;
}

.no-selection {
  margin-top: 30px;
  text-align: center;
  color: #6d7e56;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.diary-content-section {
  margin: 15px 0;
  padding: 10px;
  background-color: f9f7e8;
  border-radius: 10px;
}

.detail-title {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 8px;
}

.detail-content {
  font-size: 0.95rem;
  color: #555;
  line-height: 1.6;
  white-space: pre-wrap;
}

.divider {
  border: 0;
  border-top: 1px dashed #869a69;
  margin: 15px 0;
}

.song-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 15px 0 10px 0;
  flex-wrap: wrap;
}

.detail-song {
  color: #556b2f;
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
}

.youtube-icon-btn {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  background-color: #ff0000;
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
  transition: transform 0.2s, background-color 0.2s;
}

.youtube-icon-btn:hover {
  background-color: #cc0000;
  transform: scale(1.05);
}

.play-icon {
  margin-right: 4px;
  font-size: 0.6rem;
}

.floating-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  background-color: #869a69;
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  text-decoration: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s, background-color 0.2s;
  z-index: 1000;
}

.floating-btn:hover {
  background-color: #6d7e56;
  transform: scale(1.1);
}

.plus-icon {
  font-size: 30px;
  font-weight: bold;
}

.write-link-btn {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #f9f7e8;
  border: 1px dashed #869a69;
  color: #556b2f;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

.write-link-btn:hover {
  background-color: #e8efdf;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-side {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

h2 {
  flex: 2;
  text-align: center;
  color: #556b2f;
  margin: 0;
  font-size: 1.4rem;
}

.list-view-btn {
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
  color: #869a69;
  background-color: white;
  padding: 6px 12px;
  border: 1px solid #869a69;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.list-view-btn:hover {
  background-color: #869a69;
  color: white;
}
</style>