<template>
  <transition name="modal-fade">
    <div class="modal-overlay" >
      <div class="modal-window">
        <header class="modal-header">
          <slot name="header">
            알림
          </slot>
        </header>

        <main class="modal-body">
          <slot>
            모달 내용입니다.
          </slot>
        </main>
<<<<<<< Updated upstream

        <footer class="modal-footer">
          <button @click="$emit('close')" class="modal-close-button">
            확인
          </button>
        </footer>
=======
>>>>>>> Stashed changes
      </div>
    </div>
  </transition>
</template>

<script setup>
defineEmits(['close']);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);


  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px); 

  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-window {
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  width: 90%;
  max-width: 500px;
  overflow: hidden;
  font-family: 'Pretendard', sans-serif;
}

.modal-header {
  background-color: var(--primary-color, #869a69);
  color: white;
  padding: 1rem 1.5rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.modal-body {
  padding: 2rem 1.5rem;
  font-size: 1.1rem;
  line-height: 1.6;
}

.modal-footer {
  padding: 1rem 1.5rem;
  text-align: right;
  border-top: 1px solid #eee;
}

.modal-close-button {
  padding: 0.7rem 1.5rem;
  border: none;
  border-radius: 8px;
  background-color: var(--primary-color, #869a69);
  color: white;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.modal-close-button:hover {
  background-color: #708255;
}

.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
</style>
