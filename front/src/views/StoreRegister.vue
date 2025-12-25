<template>
  <div class="min-h-screen bg-blue-50 flex flex-col items-center py-10">
    <!-- 헤더 -->
    <header class="mb-10 text-center">
      <h1 class="text-3xl font-extrabold text-blue-600 tracking-tight mb-2">동네곳곳 원샷 등록</h1>
      <p class="text-md text-blue-500">사진 한 장으로 상품을 등록하세요</p>
    </header>

    <!-- 업로드 영역 -->
    <div>
      <label
        for="file-upload"
        class="flex flex-col items-center justify-center w-96 h-64 border-4 border-dashed border-blue-200 bg-white rounded-3xl shadow-xl cursor-pointer transition hover:border-blue-400"
      >
        <svg class="w-16 h-16 text-blue-400 mb-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5V19a2 2 0 002 2h14a2 2 0 002-2v-2.5M7 10l5-5m0 0l5 5m-5-5v12" /></svg>
        <span class="text-lg font-semibold text-blue-700">상품 사진 업로드</span>
        <input
          id="file-upload"
          type="file"
          accept="image/*"
          @change="onFileChange"
          class="hidden"
        />
      </label>
    </div>

    <!-- 로딩 -->
    <div v-if="loading" class="mt-10 flex flex-col items-center">
      <svg class="animate-spin h-10 w-10 text-blue-600 mb-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
      </svg>
      <div class="text-blue-600 font-semibold text-lg">AI 에이전트 분석 중...</div>
    </div>

    <!-- 결과 모달 -->
    <div v-if="showModal" class="fixed inset-0 flex z-50 items-center justify-center bg-black bg-opacity-30">
      <div class="bg-white rounded-3xl shadow-xl p-8 w-96 relative">
        <h2 class="text-2xl font-bold text-blue-600 mb-6 text-center">AI 인식 결과</h2>
        <div class="mb-4">
          <label class="block text-sm font-semibold text-blue-700 mb-2">상품명</label>
          <input 
            v-model="modalItem"
            type="text"
            class="w-full rounded-xl border border-blue-200 px-4 py-2 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none"
          />
        </div>
        <div class="mb-6">
          <label class="block text-sm font-semibold text-blue-700 mb-2">가격 (원)</label>
          <input 
            v-model.number="modalPrice"
            type="number"
            min="0"
            class="w-full rounded-xl border border-blue-200 px-4 py-2 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none"
          />
        </div>
        <button 
          class="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white shadow-lg font-bold text-lg transition"
          @click="onSubmitFinal"
        >최종 등록</button>
        <button aria-label="close" @click="showModal=false" class="absolute top-4 right-4 text-blue-300 hover:text-blue-600 text-xl">&times;</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const loading = ref(false)
const showModal = ref(false)
const modalItem = ref('')
const modalPrice = ref('')
const uploadedImage = ref(null)

async function onFileChange(e) {
  const file = e.target.files[0]
  if (!file) return;
  uploadedImage.value = file;
  loading.value = true;
  try {
    const formData = new FormData();
    formData.append('image', file)
    // 추가적으로 상품명·가격 예시 입력까지 받고 싶다면 formData에 title, content 등을 append 가능
    const response = await axios.post('/api/stores/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    const { item, price } = response.data;
    modalItem.value = item;
    modalPrice.value = price;
    showModal.value = true;
  } catch (error) {
    alert('AI 분석 또는 업로드에 실패했습니다.');
  } finally {
    loading.value = false;
  }
}

function onSubmitFinal() {
  // 실제 최종 등록 처리 로직(예: PUT, PATCH 등)은 필요에 따라 여기에 작성
  alert(`상품명: ${modalItem.value}\n가격: ${modalPrice.value}원\n(실제 저장로직은 추가 구현!)`)
  showModal.value = false;
}
</script>

<style scoped>
</style>

