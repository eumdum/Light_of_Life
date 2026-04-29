import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './index.css'
import VCalendar from 'v-calendar'
import 'v-calendar/style.css'

createApp(App)
  .use(store)
  .use(router)
  .mount('#app')

const app = createApp(App)

app.use(router)
app.use(VCalendar, {})

app.mount('#app')

