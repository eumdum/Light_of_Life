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
        <p>{{ loadingMessages[currentMessageIndex] }}{{ loadingDots }}</p>
      </div>

      <div v-else class="analysis-content">
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
      </div>
    </Modal>
  </div>
</template>


<script>
import axios from 'axios';
import Modal from '@/components/Modal.vue';

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
        "인공지능이 마음을 분석 중이에요",
        "당신에게 어울리는 노래를 찾는 중이에요",
        "추천 이유를 정성껏 작성 중입니다",
        "거의 다 됐어요! 잠시만요~"
      ],
      currentMessageIndex: 0,
      messageInterval: null,
    };
  },

  methods: {
    async submitDiary() {
      if (!this.newDiary.title || !this.newDiary.content) {
        alert("제목과 내용을 모두 입력해주세요.");
        return;
      }

      this.isSubmitting = true;
      this.recommendation = null;
      this.showLoadingModal();

      const token = localStorage.getItem('access_token');

      try {
        const response = await axios.post(
          `${API_BASE_URL}diaries/`,
          {
            title: this.newDiary.title,
            content: this.newDiary.content,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        if (response.data) {
          if (response.data.recommendation_song) {
            this.recommendation = response.data;
          } else if (response.data.recommendation) {
            this.recommendation = response.data.recommendation;
          }
          console.log("모달에 표시될 데이터:", this.recommendation);
        }

        this.modalState = 'success';
      } catch (error) {
        console.error('일기 저장 실패:', error.response?.data || error);

        if (error.response?.status === 401) {
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

      this.messageInterval = setInterval(() => {
        if (this.currentMessageIndex < this.loadingMessages.length - 1) {
          this.currentMessageIndex++;
        } else {
          clearInterval(this.messageInterval);
        }
      }, 4000);
    },

    startLoadingDots() {
      if (this.loadingInterval) clearInterval(this.loadingInterval);
      this.loadingInterval = setInterval(() => {
        this.loadingDots = this.loadingDots.length >= 3 ? '' : this.loadingDots + '.';
      }, 500);
    },

    stopLoadingDots() {
      clearInterval(this.loadingInterval);
      clearInterval(this.messageInterval);
    },

    closeModalAndRedirect() {
      this.isModalVisible = false;
      this.recommendation = null;
      this.$router.push('/list');
    },
  },
};
</script>


<style scoped>
.page-container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 1rem;
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
</style>