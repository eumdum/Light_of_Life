<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div class="min-h-screen bg-[#869a69] flex flex-col items-center pt-12 sm:pt-20 px-4">
    <div class="w-full max-w-2xl lg:max-w-3xl xl:max-w-4xl flex flex-col items-center">
      <h2 class="text-white text-2xl sm:text-3xl font-bold mb-8 text-center">
        오늘은 무슨 일이 있었나요?
      </h2>

      <textarea
        class="w-full p-4 bg-white border border-gray-300 rounded-lg shadow-lg focus:outline-none focus:ring-4 focus:ring-[#B8CBA5] focus:border-transparent resize-y text-gray-800 placeholder-gray-500"
        rows="12"
        placeholder="여기에 하루를 기록해보세요..."
      ></textarea>
      <button
        class="mt-8 px-10 py-3 bg-[#607A4C] hover:bg-[#506A3C] text-white text-lg font-semibold rounded-lg shadow-xl focus:outline-none focus:ring-4 focus:ring-[#A5C9A5] focus:ring-opacity-75 transition-all duration-200 ease-in-out transform hover:scale-105"
      >
        저장
      </button>
      </div>
  </div>
</template>

<style scoped>
/* 이 컴포넌트에만 적용되는 추가 스타일이 필요하다면 여기에 작성합니다. */
</style>
<!--
<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
-->