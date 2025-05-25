<template>
  <div class="home-container">
    <div class="diary-form">
      <h1>감정 일기 작성</h1>
      <label for="content"></label>
      <!--위에 라벨부분 지워야하나?-->
      <textarea
        id="content"
        v-model="content"
        rows="10"
        class="diary-textarea"
        placeholder="오늘은 무슨일이 있었나요?"
      ></textarea>
      <br />
      <button class="submit-button" @click="submitDiary">저장</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const content = ref("");
const submitDiary = async () => {
  try {
    await axios.post("http://127.0.0.1:8000/api/diaries/", {
      content: content.value,
    });
    content.value = "";
  } catch (error) {
    console.error("저장 실패:", error);
  }
};
</script>

<style scoped>
.home-container {
  background-color: #869a69;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: start;
  padding-top: 100px;
  font-family: "Segoe UI", sans-serif;
}

.diary-form {
  background-color: white;
  padding: 40px;
  border-radius: 12px;
  width: 60%;
  max-width: 800px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.diary-textarea {
  width: 100%;
  height: 200px;
  font-size: 1rem;
  padding: 10px;
  resize: vertical;
  border-radius: 8px;
  border: 1px solid #ccc;
  margin-top: 10px;
}

.submit-button {
  margin-top: 20px;
  padding: 10px 24px;
  background-color: #4e6e4f;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}
</style>
