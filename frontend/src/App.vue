<template>
  <div id="app-container" :class="currentTheme">
    <header class="top-navbar" :class="[{ 'scrolled': isScrolled }, { 'message-wall-nav-style': $route.meta.navTransparentOnMessageWall }]">
      <div class="logo">Skinnyxh</div>
      <div class="welcome-message">欢迎来到yxh的个人网站</div>
      <nav class="top-nav-actions">
        <button @click="toggleTheme" class="theme-toggle-button">
          <span v-if="currentTheme === 'theme-blue'">☀️</span>
          <span v-else>🌙</span>
        </button>
        <!-- NavigationBar component will now primarily be the toggle button for the side nav -->
        <NavigationBar @toggle-theme="toggleTheme" />
      </nav>
    </header>
    <router-view />
  </div>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue'

export default {
  name: 'App',
  components: {
    NavigationBar
  },
  data() {
    return {
      isScrolled: false,
      currentTheme: 'theme-blue' // Default theme
    };
  },
  methods: {
    handleScroll() {
      this.isScrolled = window.scrollY > 50;
    },
    toggleTheme() {
      if (this.currentTheme === 'theme-blue') {
        this.currentTheme = 'theme-orange';
      } else {
        this.currentTheme = 'theme-blue';
      }
      document.documentElement.className = this.currentTheme; // Apply theme to root for global vars
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
    document.documentElement.className = this.currentTheme; // Set initial theme on root
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  }
}
</script>

<style>
#app-container {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-primary);
  background-color: var(--background-main);
  transition: background-color 0.3s, color 0.3s;
}

.top-navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 30px; /* Increased padding for content */
  background-color: var(--navbar-background-initial);
  color: var(--navbar-text);
  z-index: 1001; /* Higher than side nav toggle, but side nav itself needs higher */
  transition: background-color 0.3s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  box-sizing: border-box;
}

.top-navbar.scrolled {
  background-color: var(--navbar-background-scrolled);
}

.top-navbar.message-wall-nav-style {
  background-color: rgba(0, 0, 0, 0.1) !important; /* 90% 透明的深色背景，可根据主题调整 */
  /* 如果希望基于现有主题色的变量进行透明化，会复杂一些，需要知道变量的具体颜色值 */
  /* 例如，如果 --navbar-background-initial 是纯色，可以这样： */
  /* background-color: color-mix(in srgb, var(--navbar-background-initial) 10%, transparent); */
  /* 但 color-mix 兼容性可能需要注意，直接用 rgba 更稳妥 */
  box-shadow: none !important; /* 移除阴影，使其更融入背景 */
}

.logo {
  font-weight: bold;
  font-size: 1.5em;
  color: var(--accent-color); /* Use accent color for logo */
}

.welcome-message {
  font-size: 1.1em; /* Increased font size */
  color: var(--text-secondary);
  /* Allow shrinking if space is an issue on smaller screens */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0 15px; /* Add some margin to prevent sticking to logo or buttons */
}

.top-nav-actions {
  display: flex;
  align-items: center;
  background-color: var(--primary-50) !important; /* 直接使用主题中最浅的蓝色作为背景 */
  border-radius: 6px; 
  overflow: hidden; 
  box-shadow: none; /* 移除之前的 box-shadow，以防它引入非期望颜色 */
  /* border: 1px solid var(--primary-100); */ /* 可选：如果需要一个非常浅的轮廓 */
}

.theme-toggle-button,
.nav-toggle-button-topbar {
  background-color: transparent !important; /* 按钮透明，透出父容器的 --primary-50 背景 */
  border: none !important; 
  color: var(--navbar-text) !important; /* 文字/图标颜色保持不变 */
  padding: 8px 12px; 
  border-radius: 0; 
  cursor: pointer;
  font-size: 1.5em;
  transition: color 0.3s, background-color 0.3s;
  line-height: 1; 
}

.theme-toggle-button { 
   border-right: 1px solid var(--primary-100); /* 分割线用比背景稍深一度的浅蓝 (primary-100) */ 
}

.nav-toggle-button-topbar {
    /* 确保右边按钮没有左边框，以免重复 */
    border-left: none !important; 
}

.theme-toggle-button:hover,
.nav-toggle-button-topbar:hover {
  color: var(--accent-color) !important;
  background-color: rgba(0,0,0,0.05) !important; /* Hover时背景用轻微叠加色 */
}

/* Adjust main content to account for fixed navbar */
.home-page { /* Assuming HomePage is the direct child after header */
  padding-top: 70px; /* Height of the navbar + some space */
}
</style> 