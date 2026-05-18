<template>
  <div class="page-container">
    <header class="app-header">
      <h1>오늘의 일기</h1>
      <p>하루의 끝, 당신의 이야기를 남겨보세요.</p>
    </header>

    <main class="content-wrapper">
      <form @submit.prevent="submitDiary" class="diary-form">
        <input v-model="newDiary.title" type="text" placeholder="제목" class="form-input" required />
        <textarea v-model="newDiary.content" placeholder="어떤 하루를 보냈나요?" class="form-textarea" rows="8"
          required></textarea>
        <div class="button-group">
          <button type="submit" class="submit-button" :disabled="isSubmitting">
            일기 저장하기
          </button>
          <router-link to="/list" class="list-button">목록 보기</router-link>
        </div>
      </form>
    </main>

    <Modal v-if="isModalVisible" @close="closeModalAndRedirect">
      <template #header>
        <span v-if="modalState === 'loading'">분석 중...</span>
        <span v-else>📝 당신의 하루를 분석했어요</span>
      </template>

      <div v-if="modalState === 'loading'" class="loading-content">
        <div class="spinner"></div>
        <p>당신의 하루를 분석하고 있어요{{ loadingDots }}</p>
      </div>

      <div v-else class="analysis-content">
<<<<<<< Updated upstream
        <p>오늘의 감정은 <strong>'{{ analysisResult.emotion }}'</strong>(이)네요.</p>
        <div class="music-recommendation">
          <h4>이런 음악은 어때요?</h4>
          <p class="recommendation-text">
            아래 링크를 눌러 오늘의 감정에 맞는 음악을 들어보세요!
          </p>
          <a :href="analysisResult.youtubeLink" target="_blank" rel="noopener noreferrer" class="youtube-link-button">
            🎵 유튜브에서 음악 듣기
          </a>
        </div>
=======
        <div v-if="recommendation && recommendation.recommendation_song">
          <p>지금 마음은 <strong>'{{ recommendation.emotion }}'</strong> 인 것 같네요!</p>
          <p>오늘의 추천 곡: <strong>{{ recommendation.recommendation_song }}</strong></p>

          <div class="music-recommendation">
            <h4>추천 이유 및 감정 분석</h4>

            <div class="scroll-box">
              <p class="recommendation-text">{{ recommendation.recommendation_reason }}</p>
            </div>

            <a :href="recommendation.youtube_url" target="_blank" rel="noopener noreferrer" class="youtube-link-button">
              🎵 유튜브에서 노래 듣기 🎵
            </a>
          </div>
        </div>

        <div v-else>
          <p>일기가 안전하게 저장되었습니다!</p>
        </div>

        <button @click="closeModalAndRedirect" class="modal-close-button">확인</button>
>>>>>>> Stashed changes
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Modal from '@/components/Modal.vue';

<<<<<<< Updated upstream
const router = useRouter();
=======
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default {
  components: { Modal },
  data() {
    return {
      newDiary: {
        title: '',
        content: '',
      },
      isSubmitting: false,
      isModalVisible: false,
      modalState: 'loading',
      loadingDots: '',
      loadingInterval: null,
      recommendation: null,
      loadingMessages: [
        "당신의 오늘을 읽고 있어요",
        "AI가 마음을 분석 중이에요",
        "당신에게 어울리는 노래를 찾는 중이에요",
        "추천 이유를 정성껏 작성 중입니다",
        "거의 다 됐어요! 잠시만요~"
      ],
      currentMessageIndex: 0,
      messageInterval: null,
    };
  },
>>>>>>> Stashed changes

const API_BASE_URL = `http://${window.location.hostname}:8000`;

<<<<<<< Updated upstream
const API_URL = `${API_BASE_URL}/api/diaries/`;

const newDiary = ref({ title: '', content: '' });
const isSubmitting = ref(false);

const isModalVisible = ref(false);
const modalState = ref('hidden');
const analysisResult = ref({
  emotion: '',
  youtubeLink: ''
});

const loadingDots = ref('.');
let dotInterval = null;

watch(isModalVisible, (newValue) => {
  if (newValue && modalState.value === 'loading') {
    dotInterval = setInterval(() => {
      loadingDots.value = loadingDots.value.length < 3 ? loadingDots.value + '.' : '.';
    }, 500);
  } else {
    if (dotInterval) {
      clearInterval(dotInterval);
      dotInterval = null;
    }
  }
});
=======
      this.isSubmitting = true;
      this.recommendation = null;
      this.showLoadingModal();

      const token = localStorage.getItem('access_token');

      try {
        const res = await axios.post(`${API_BASE_URL}diaries/`, {
          title: this.newDiary.title,
          content: this.newDiary.content,
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        if (res.data) {
          if (res.data.recommendation_song) {
            this.recommendation = res.data;
          } else if (res.data.recommendation) {
            this.recommendation = res.data.recommendation;
          }
          console.log("모달에 표시될 데이터:", this.recommendation);
        }

        this.modalState = 'success';
      } catch (error) {
        console.error('일기 저장 실패:', error.res?.data || error);

        if (error.res?.status === 401) {
          alert('로그인이 만료되었습니다. 다시 로그인해주세요.');
          this.$router.push('/login');
        } else {
          alert('저장 중 오류가 발생했습니다.');
        }
        this.isModalVisible = false;
      } finally {
        this.stopLoadingDots();
        this.isSubmitting = false;
      }
    },

    showLoadingModal() {
      this.isModalVisible = true;
      this.modalState = 'loading';
      this.currentMessageIndex = 0;
      this.loadingDots = '';
      this.startLoadingDots();
>>>>>>> Stashed changes


const musicQueryDatabase = {
  "행복": [
    "신나는 노래", "기분 좋아지는 음악 플레이리스트", "행복할 때 듣는 KPOP", 
    "밝은 팝송", "듣기만 해도 설레는 노래", "축하 파티 음악", "성공 축하 노래"
  ],
  "슬픔": [
    "위로가 되는 노래", "슬픈 발라드 추천", "혼자 듣기 좋은 잔잔한 음악", 
    "비 오는 날 듣는 노래", "이별 노래 모음", "감성적인 영화 OST", "새벽에 듣기 좋은 노래"
  ],
  "분노": [
    "스트레스 해소 음악", "신나는 락 음악", "운동할 때 듣는 EDM", 
    "화날 때 듣는 힙합", "세상에 소리치고 싶을 때 듣는 노래", "파워풀한 메탈", "분노의 질주 OST"
  ],
  "평온": [
    "차분한 연주곡", "명상 음악", "새벽 감성 플레이리스트", "유명 클래식 모음",
    "집중할 때 듣는 음악", "Lo-fi hip hop", "자연의 소리", "잠 잘오는 클래식"
  ],
  "중립": [
    "요즘 인기있는 노래", "드라이브 플레이리스트", "카페에서 듣기 좋은 노래", 
    "팝송 베스트", "인디 음악 추천", "잔잔한 팝송 모음"
  ]
};

function generateYoutubeLink(emotion) {
  const queries = musicQueryDatabase[emotion] || musicQueryDatabase['중립'];
  const randomQuery = queries[Math.floor(Math.random() * queries.length)];
  const youtubeSearchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(randomQuery)}`;
  return youtubeSearchUrl;
}

<<<<<<< Updated upstream
async function submitDiary() {
  if (!newDiary.value.title || !newDiary.value.content) {
    alert("제목과 내용을 모두 입력해주세요.");
    return;
  }
  isSubmitting.value = true;

  modalState.value = 'loading';
  isModalVisible.value = true;

  try {
    const response = await axios.post(API_URL, newDiary.value);
    const savedDiary = response.data;

    analysisResult.value.emotion = savedDiary.emotion || '중립';
    analysisResult.value.youtubeLink = generateYoutubeLink(analysisResult.value.emotion);
    
    modalState.value = 'result';

  } catch (error) {
    console.error("일기 저장에 실패했습니다:", error);
    isModalVisible.value = false;
    modalState.value = 'hidden';
    alert("저장에 실패했습니다. 다시 시도해주세요.");
  } finally {
    isSubmitting.value = false;
  }
}

function closeModalAndRedirect() {
  isModalVisible.value = false;
  modalState.value = 'hidden';
  router.push('/list');
}
</script>


<style scoped>
.page-container { 
  max-width: 700px; 
  margin: 2rem auto; 
  padding: 1rem; 
=======
<style scoped>
.page-container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 1rem;
>>>>>>> Stashed changes
}

.app-header {
  text-align: center;
  margin-bottom: 2rem;
  color: #ffffff;
}

.app-header h1 {
  font-size: 2.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.app-header p {
  font-size: 1.1rem;
  color: #ffffff;
}

.content-wrapper {
  background-color: var(--bg-light, #fff);
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid var(--border-color, #e0e0e0);
  border-radius: 10px;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  box-sizing: border-box;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--primary-color, #869a69);
  box-shadow: 0 0 0 3px rgba(134, 154, 105, 0.3);
}

.button-group {
  display: flex;
  gap: 1rem;
}

.submit-button,
.list-button {
  flex-grow: 1;
  padding: 1rem;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  text-decoration: none;
}

.submit-button {
  border: none;
  background-color: var(--primary-color, #869a69);
  color: var(--text-light, #fff);
}

.submit-button:hover {
  background-color: #708255;
  transform: translateY(-2px);
}

.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.list-button {
  background-color: #f0f0f0;
  color: #555;
  border: 1px solid #ddd;
}

.list-button:hover {
  background-color: #e5e5e5;
  border-color: #ccc;
  transform: translateY(-2px);
}

.loading-content,
.analysis-content {
  padding: 1rem;
  text-align: center;
}

.loading-content p {
  font-size: 1.2rem;
  font-weight: 500;
  color: #555;
}

.analysis-content p {
  margin-bottom: 1.5rem;
  color: #444;
}

.analysis-content strong {
  color: var(--primary-color, #869a69);
  font-size: 1.1em;
}

<<<<<<< Updated upstream
.music-recommendation { 
  background-color: #f7f8f6; 
  padding: 1.5rem; 
  border-radius: 8px; 
  border-left: 4px solid var(--primary-color, #869a69); 
  text-align: center; 
}

.music-recommendation h4 { 
  margin: 0 0 0.5rem 0; 
  font-size: 1rem; 
  color: #555; 
}

.recommendation-text { 
  font-size: 1rem; 
  color: #666; 
  margin-bottom: 1rem !important; 
}

.youtube-link-button { 
  display: inline-block; 
  padding: 0.8rem 2rem; 
  border-radius: 8px; 
  background-color: #FF0000; 
  color: white; 
  font-size: 1.1rem; 
  font-weight: 600; 
  text-decoration: none; 
  transition: all 0.2s; 
}

.youtube-link-button:hover { 
  background-color: #cc0000; 
  transform: scale(1.05); 
=======
.music-recommendation {
  background-color: #f7f8f6;
  padding: 1.5rem;
  border-radius: 12px;
  border-left: 5px solid var(--primary-color, #869a69);
  text-align: center;
  margin-bottom: 1.5rem;
  overflow: visible;
}

.music-recommendation h4 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  color: #555;
  font-weight: bold;
}

.scroll-box {
  max-height: 150px;
  overflow-y: auto;
  margin-bottom: 1.2rem;
  padding: 0 10px;
  text-align: left;
}

.scroll-box::-webkit-scrollbar {
  width: 6px;
}

.scroll-box::-webkit-scrollbar-thumb {
  background: #869a69;
  border-radius: 10px;
}

.scroll-box::-webkit-scrollbar-track {
  background: #eeeeee;
}

.recommendation-text {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.7;
  margin: 0 !important;
  word-break: keep-all;
}

.youtube-link-button {
  display: block;
  padding: 0.8rem;
  border-radius: 8px;
  background-color: #FF0000;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.youtube-link-button:hover {
  background-color: #cc0000;
  transform: scale(1.02);
>>>>>>> Stashed changes
}

.spinner {
  margin: 0 auto 1.5rem auto;
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid var(--primary-color, #869a69);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
<<<<<<< Updated upstream
=======

.modal-close-button {
  margin-top: 10px;
  padding: 12px 30px;
  background-color: #869a69;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

.modal-close-button:hover {
  background-color: #708255;
}
>>>>>>> Stashed changes
</style>
