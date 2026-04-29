<template>
    <div class="calendar-container">
        <div class="calendar-card">
            <div class="calendar-header">
                <div class="header-side"></div> <h2>🌿 {{ calendarTitle }}마음 달력</h2>
                
                <div class="header-side">
                    <router-link v-if="isLoggedIn" to="/list" class="list-view-btn">
                        📋 목록 보기
                    </router-link>
                </div>
            </div>

            <VCalendar
            expanded
            borderless
            :attributes="attributes"
            @dayclick="onDayClick"
            class="custom-calendar"
            />
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

            <!-- <h3 class="detail-song">🎵 {{ selectedDiary.recommendation_song }}</h3>
            <p class="detail-reason">{{ selectedDiary.recommendation_reason }}</p> -->

            <div class="song-recommendation">
                <div class="song-header">
                    <h3 class="detail-song">🎵 {{ selectedDiary.recommendation_song }}</h3>
                    <a :href="selectedDiary.youtube_url" target="_blank" class="youtube-icon-btn">
                        <span class="play-icon">▶</span> 들어보기
                    </a>
                </div>
                <p class="detail-reason">{{ selectedDiary.recommendation_reason }}</p>
            </div>

            <!-- <div class="detail-footer">
                <a :href="selectedDiary.youtube_url" target="_blank" class="youtube-link">유튜브로 듣기</a> -->
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
// import Modal from '@/components/Modal.vue';

const diaries = ref([]);
const attributes = ref([]);
const selectedDiary = ref(null);

const calendarTitle = computed(() => {
  const savedId = localStorage.getItem('user_id');
  const token = localStorage.getItem('access_token');
  
  // 토큰과 아이디가 둘 다 있을 때만 "은정님의 " 처럼 표시, 아니면 빈칸
  return (token && savedId) ? `${savedId}님의 ` : '';
});

const isLoggedIn = computed(() => !!localStorage.getItem('access_token'));
  
const fetchDiaries = async () => {
    const token = localStorage.getItem('access_token');
  
    // [추가] 토큰이 없으면 데이터를 비우고 종료!
    if (!token) {
        diaries.value = [];
        attributes.value = [];
        selectedDiary.value = null;
        return;
    }

    try {
        // const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:8000/api/diaries/', {
            headers: { Authorization: `Bearer ${token}` }
        });
        diaries.value = response.data;

        // 현재 로그인한 유저 정보 (localStorage 등에 저장해둔 유저 ID가 있다면 활용)
        // const currentUserId = localStorage.getItem('user_id'); 

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
  console.log("클릭한 날짜 ID:", day.id); // 1. 클릭이 되는지 확인
  console.log("현재 가지고 있는 전체 일기들:", diaries.value); // 2. 전체 데이터 확인

  const found = diaries.value.find(d => d.date === day.id);
  
  if (found) {
    console.log("✅ 찾은 데이터:", found); // 3. 매칭된 데이터 확인
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
background-color: #f9f7e8; /* 우리 헤더 색상 */
padding: 30px;
border-radius: 20px;
box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

h2 {
text-align: center;
color: #556b2f;
margin-bottom: 20px;
}

/* v-calendar 내부 스타일 커스텀 */
.custom-calendar {
background-color: transparent !important;
}

.diary-detail-card {
  margin-top: 20px;
  padding: 20px;
  background-color: #f9f7e8;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
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
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
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
  white-space: pre-wrap; /* 줄바꿈 허용 */
}

.divider {
  border: 0;
  border-top: 1px dashed #869a69;
  margin: 15px 0;
}

/* 제목과 버튼을 가로로 정렬 */
.song-header {
  display: flex;
  align-items: center;
  gap: 12px; /* 제목과 버튼 사이 간격 */
  margin: 15px 0 10px 0;
  flex-wrap: wrap; /* 제목이 너무 길면 버튼이 아래로 자연스럽게 내려가게 */
}

.detail-song {
  color: #556b2f;
  margin: 0; /* 헤더 안에서 정렬을 위해 마진 제거 */
  font-size: 1.1rem;
  font-weight: 700;
}

/* 유튜브 버튼을 작고 귀엽게 */
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

/* 기존 하단 푸터는 이제 필요 없으니 삭제하거나 정리해줘 */
.detail-footer {
  display: none;
}

.floating-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  background-color: #869a69; /* 우리 포인트 컬러 */
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

/* 양옆 공간을 똑같이 나눠 가져서 타이틀이 가운데 오게 함 */
.header-side {
  flex: 1;
  display: flex;
  justify-content: flex-end; /* 오른쪽 요소는 오른쪽 정렬 */
}

h2 {
  flex: 2; /* 타이틀이 중앙을 더 많이 차지하게 */
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