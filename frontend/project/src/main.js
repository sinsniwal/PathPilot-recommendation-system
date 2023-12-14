import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'

const app = createApp(App)

app.use(router)

router.isReady().then(() => {
    app.mount('#app')
})