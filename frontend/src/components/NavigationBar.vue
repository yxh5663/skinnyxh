<template>
  <button @click.stop="toggleNav" class="nav-toggle-button-topbar">☰</button>
  <div v-if="isNavOpen" @click="closeNav" class="nav-overlay"></div>
  <nav :class="{ 'nav-open': isNavOpen }" class="side-navbar-panel" ref="sideNavPanel">
    <ul>
      <li @click="closeNav"><router-link to="/" class="nav-link">首页</router-link></li>
      <li @click="closeNav"><router-link to="/experience" class="nav-link">经历</router-link></li>
      <li @click="closeNav"><router-link to="/projects" class="nav-link">项目</router-link></li>
      <li @click="closeNav"><router-link to="/message-wall" class="nav-link">其他</router-link></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'NavigationBar',
  emits: ['toggle-theme'],
  data() {
    return {
      isNavOpen: false
    };
  },
  methods: {
    toggleNav() {
      this.isNavOpen = !this.isNavOpen;
    },
    closeNav() {
      this.isNavOpen = false;
    },
    handleClickOutside(event) {
      if (this.isNavOpen && this.$refs.sideNavPanel && !this.$refs.sideNavPanel.contains(event.target)) {
        // Check if the click was on the toggle button itself to prevent immediate re-close
        const toggleButton = document.querySelector('.nav-toggle-button-topbar'); 
        if (toggleButton && toggleButton.contains(event.target)) {
            return; 
        }
        this.closeNav();
      }
    }
  },
  watch: {
    isNavOpen(isOpen) {
      if (isOpen) {
        document.addEventListener('click', this.handleClickOutside, true); // Use capture phase
      } else {
        document.removeEventListener('click', this.handleClickOutside, true);
      }
    }
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside, true);
  }
};
</script>

<style scoped>
.nav-toggle-button-topbar {
  background: none;
  border: none;
  color: inherit;
  padding: 8px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 1.5em;
  transition: color 0.3s;
  line-height: 1;
  z-index: 1003;
}

.nav-toggle-button-topbar:hover {
  color: var(--accent-color);
}

.nav-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  z-index: 1001;
}

.side-navbar-panel {
  position: fixed;
  top: 0;
  right: -280px;
  width: 280px;
  height: 100%;
  background-color: var(--sidenav-background);
  transition: right 0.3s ease;
  padding-top: 60px;
  z-index: 1002;
  box-shadow: -3px 0 10px rgba(0,0,0,0.1);
}

.side-navbar-panel.nav-open {
  right: 0;
}

.side-navbar-panel ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  transform: translateY(-80px);
}

.side-navbar-panel ul li {
    display: flex;
    align-items: center;
    justify-content: center; 
}

.side-navbar-panel ul li a {
  display: block;
  padding: 20px 25px;
  color: var(--sidenav-text);
  text-decoration: none;
  transition: background-color 0.3s, color 0.3s;
  font-size: 1.1em;
  font-weight: normal;
  text-align: center;
  width: 100%;
  box-sizing: border-box;
}

.side-navbar-panel ul li a:hover {
  background-color: var(--sidenav-hover-background);
  color: var(--sidenav-hover-text);
}

.nav-link {
  font-size: 1.5em; 
  font-weight: bold; 
}

</style> 