<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <h1>나의 감정 일기</h1>
    <DiaryForm /> {/* DiaryForm 컴포넌트를 여기에 추가 */} {/* 여기에 기존에
    만들었던 일기 목록 표시 컴포넌트도 추가할 수 있습니다. */}
  </div>
</template>

<script setup>
// @ is an alias to /src
import DiaryForm from "@/components/DiaryForm.vue"; // DiaryForm 컴포넌트 가져오기

// 만약 HomeView에서 다른 로직 (예: 일기 목록 불러오기)이 있다면 여기에 작성
</script>

<style scoped>
.home {
  text-align: center;
}
.home h1 {
  margin-bottom: 30px;
}
</style>
