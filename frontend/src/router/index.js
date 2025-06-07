import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import MessageWall from '../components/MessageWall.vue';
import ExperiencePage from '../components/experience.vue';
import TimelinePage from '../components/time.vue';
import CalendarPage from '../components/calender.vue';
import MapPage from '../components/MapPage.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/map',
    name: 'Map',
    component: MapPage
  },
  {
    path: '/message-wall',
    name: 'MessageWall',
    component: MessageWall,
    meta: { navTransparentOnMessageWall: true }
  },
  {
    path: '/experience',
    name: 'Experience',
    component: ExperiencePage
  },
  {
    path: '/timeline',
    name: 'Timeline',
    component: TimelinePage
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: CalendarPage
  }
  // 如果你有其他页面，可以在这里添加更多路由
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL || '/'), // process.env.BASE_URL 通常在Vue CLI项目中配置
  routes
});

export default router;

