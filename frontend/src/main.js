import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // 引入路由配置
import './assets/styles.css' // 引入全局样式

const app = createApp(App)

app.use(router) // 使用路由

app.mount('#app') 