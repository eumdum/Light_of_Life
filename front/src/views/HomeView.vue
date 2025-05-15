<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js App" />
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";
import axios from "axios";

export default {
  name: "HomeView",
  components: {
    HelloWorld,
  },
};

axios.get("http://127.0.0.1:8000/api/diaries/").then((response) => {
  console.log(response.data);
});
</script>
