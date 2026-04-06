<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-blue-700 text-white p-4 shadow-md">
      <div class="container mx-auto flex justify-between items-center">
      </div>
    </header>
    
    <main>
      <router-view />
    </main>
    
    <footer class="bg-gray-800 text-white p-4 mt-8">
      <div class="container mx-auto text-center">
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
body {
  background-color: #a8b69a; 
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  margin: 0;
  color: #333;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

:root {
  --primary-color: #869a69;
  --text-dark: #333;
  --text-light: #f5f5f5;
  --bg-light: #ffffff;
  --border-color: #e5e7eb;
}
</style>
