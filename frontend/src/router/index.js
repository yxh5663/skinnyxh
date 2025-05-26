import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import MessageWall from '../components/MessageWall.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/message-wall',
    name: 'MessageWall',
    component: MessageWall,
    meta: { navTransparentOnMessageWall: true }
  }
  // 如果你有其他页面，可以在这里添加更多路由
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL || '/'), // process.env.BASE_URL 通常在Vue CLI项目中配置
  routes
});

export default router;

