// ✅ Tailwind CSS가 이미 설치되었다고 가정하고 작성

// 📁 src/components/DiaryForm.vue
<template>
  <div class="min-h-screen bg-[#869A69] flex justify-center items-start pt-20">
    <div class="bg-white p-10 rounded-2xl shadow-lg w-full max-w-2xl">
      <h1 class="text-2xl font-bold text-center mb-6">감정 일기 작성</h1>
      <label for="content" class="block mb-2 font-semibold">일기쓰기</label>
      <textarea
        id="content"
        v-model="content"
        rows="10"
        class="w-full border rounded-md p-4 text-base resize-y"
        placeholder="오늘 있었던 일을 자유롭게 적어보세요."
      ></textarea>
      <button
        class="mt-6 w-full bg-green-700 hover:bg-green-800 text-white py-2 px-4 rounded-md text-lg"
        @click="submitDiary"
      >
        저장
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const content = ref('')

const submitDiary = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/api/diaries/', {
      content: content.value,
    })
    alert('일기가 저장되었습니다!')
    content.value = ''
  } catch (error) {
    console.error('저장 실패:', error)
    alert('저장에 실패했습니다.')
  }
}
</script>


// 📁 src/components/DiaryList.vue
<template>
  <div class="min-h-screen bg-gray-100 py-10 px-4">
    <div class="max-w-3xl mx-auto bg-white p-8 rounded-lg shadow">
      <h2 class="text-2xl font-bold mb-6">감정 일기 목록</h2>
      <ul>
        <li
          v-for="(diary, index) in diaries"
          :key="index"
          class="border-b py-4"
        >
          <p class="text-gray-800 font-medium">{{ diary.content }}</p>
          <p class="text-sm text-gray-500">감정: {{ diary.emotion }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const diaries = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/diaries/')
    diaries.value = res.data
  } catch (e) {
    console.error('불러오기 실패:', e)
  }
})
</script>


// 📁 src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import DiaryForm from '@/components/DiaryForm.vue'
import DiaryList from '@/components/DiaryList.vue'

const routes = [
  {
    path: '/',
    name: 'WriteDiary',
    component: DiaryForm,
  },
  {
    path: '/diaries',
    name: 'DiaryList',
    component: DiaryList,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

<!--
<template>
  <div class="diary-form">
    <h3>오늘의 일기</h3>
    <textarea
      v-model="diaryContent"
      placeholder="오늘 하루 어떤 일이 있었나요?"
    ></textarea>
    <button @click="submitDiary">일기 저장</button>

    <div v-if="isLoading" class="loading-indicator">
      <p>일기를 분석하고 있어요...</p>
    </div>

    <div v-if="diaryResponse" class="diary-result">
      <h4>작성된 일기</h4>
      <p><strong>내용:</strong> {{ diaryResponse.content }}</p>
      <p><strong>감정:</strong> {{ diaryResponse.emotion }}</p>
    </div>

    <div v-if="error" class="error-message">
      <p>오류가 발생했습니다: {{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const diaryContent = ref("");
const diaryResponse = ref(null); // API 응답을 저장할 ref
const isLoading = ref(false);
const error = ref(null);

const submitDiary = async () => {
  if (!diaryContent.value.trim()) {
    alert("일기 내용을 입력해주세요.");
    return;
  }

  isLoading.value = true;
  diaryResponse.value = null;
  error.value = null;

  try {
    // Django API 엔드포인트 (포트 번호는 Django 서버와 일치해야 함)
    const response = await axios.post("http://127.0.0.1:8000/api/diaries/", {
      content: diaryContent.value,
      // 'emotion' 필드는 백엔드에서 분석 후 채워지므로 보내지 않음
    });
    diaryResponse.value = response.data; // 성공 시 응답 데이터 저장
    diaryContent.value = ""; // 입력창 초기화
  } catch (err) {
    console.error("일기 저장 오류:", err);
    error.value = err.response
      ? err.response.data
      : "서버에 연결할 수 없습니다.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.diary-form {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.diary-form h3 {
  text-align: center;
  margin-bottom: 20px;
}

.diary-form textarea {
  width: 100%;
  min-height: 150px;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box; /* 너비 계산에 패딩과 테두리 포함 */
  resize: vertical; /* 세로 크기만 조절 가능 */
}

.diary-form button {
  display: block;
  width: 100%;
  padding: 10px 15px;
  background-color: #5cb85c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.diary-form button:hover {
  background-color: #4cae4c;
}

.loading-indicator {
  margin-top: 20px;
  text-align: center;
  color: #555;
}

.diary-result {
  margin-top: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 4px;
}

.diary-result h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
}

.diary-result p {
  margin-bottom: 5px;
}

.error-message {
  margin-top: 20px;
  padding: 10px;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
}
</style>
-->