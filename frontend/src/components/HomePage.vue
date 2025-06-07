<template>
    <div class="home-page">
      <!-- <canvas id="particle-canvas-home"></canvas> Canvas 移除 -->
      <div class="content-wrapper">
        <!-- Hero section removed as requested -->
  
        <!-- New Introduction Section based on the image -->
        <section class="new-introduction-section full-screen-intro">
          <!-- Removed .dialogue-bubbles.left-bubbles and .right-bubbles containers -->
          <!-- Bubbles are now individually positioned with wrappers -->
  
          <div class="bubble-instance-wrapper bubble-wrapper-1">
            <div class="bubble">白羊座</div>
          </div>
          <div class="bubble-instance-wrapper bubble-wrapper-2">
            <div class="bubble">INFP</div>
          </div>
          <div class="bubble-instance-wrapper bubble-wrapper-3">
            <div class="bubble">热爱技术</div>
          </div>
  
          <div class="intro-background-oval"></div> <!-- Decorative oval shape -->
          <div class="intro-container">
            <div class="intro-avatar-column">
              <img src="/yxh.jpg" alt="于晓晗" class="profile-avatar-new">
            </div>
            <div class="intro-text-column">
              <div class="intro-text-card">
                <p class="label-my-name-is">My name is:</p>
                <h2 class="main-name-new">于晓晗</h2>
                <hr class="name-separator-new">
                <p class="label-im-a">I'm a:</p>
                <ul class="roles-new">
                  <li>Influencer (>286K followers)</li>
                  <li>Chromium Developer</li>
                  <li>Web Developer</li>
                  <li>Game Developer</li>
                  <li>Game Critic</li>
                  <li>Digital Nomad</li>
                  <li>Trader</li>
                </ul>
              </div>
            </div>
          </div>
          <div class="floating-icons-area">
              <span class="f-icon chrome-icon" title="Nikon"></span>
              <span class="f-icon eth-icon" title="Ethereum"></span>
              <span class="f-icon edge-icon" title="Edge"></span>
          </div>
  
          <div class="bubble-instance-wrapper bubble-wrapper-4">
            <div class="bubble">尼康佬</div>
          </div>
          <div class="bubble-instance-wrapper bubble-wrapper-5">
            <div class="bubble">啥也不是</div>
          </div>
          <div class="bubble-instance-wrapper bubble-wrapper-6">
            <div class="bubble">健身</div>
          </div>
        </section>
  
        <section class="content-cards-section">
          <div class="main-content-super-card">
            <h2>主要内容</h2>
            <div class="card-container">
              <div class="card card-timeline-placeholder">
                <h3>时间轴</h3>
                <p>关于搭建网站的时间轴。</p>
                <div class="basic-timeline" v-if="!loadingTimeline && !timelineError && latestTimelineEvents.length">
                  <div class="timeline-item" v-for="event in latestTimelineEvents" :key="event.id">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                      <span class="timeline-date">{{ event.date }}</span>
                      <p>{{ event.title }}</p> <!-- 只显示标题，如果需要详情也可以添加 event.details -->
                    </div>
                  </div>
                </div>
                <div v-if="loadingTimeline" class="timeline-loading">
                  <p>加载最新动态中...</p>
                </div>
                <div v-if="timelineError" class="timeline-error">
                  <p>{{ timelineError }}</p>
                </div>
                <div v-if="!loadingTimeline && !timelineError && !latestTimelineEvents.length" class="timeline-no-events">
                  <p>暂无最新动态。</p>
                </div>
                <router-link to="/timeline" class="card-link">了解更多 &rarr;</router-link>
              </div>
              <div class="card card-current-affairs">
                <h3>时政信息</h3>
                <p>定时爬取每天的热点信息。</p>
                <div class="placeholder-content" style="text-align: center; color: #9ca3af; margin-top: 20px;">
                  <p>（内容暂未填充）</p>
                </div>
              </div>
              <div class="card card-calendar">
                <h3>日历</h3>
                <p>是一个努力变j的p人日记</p>
                <div class="mini-calendar-container">
                  <!-- Display loading/error messages for calendar -->
                  <div v-if="loadingAuthStatus && !authError" class="calendar-loading-message">
                    <p>验证用户权限中...</p>
                  </div>
                  <div v-else-if="loadingCalendarEvents && !authError" class="calendar-loading-message">
                    <p>加载日历事件中...</p>
                  </div>
                  <div v-if="authError" class="calendar-error-message">
                    <p>权限验证失败: {{ authError }}</p>
                  </div>
                  <div v-if="calendarEventsError" class="calendar-error-message">
                    <p>事件加载失败: {{ calendarEventsError }}</p>
                  </div>

                  <FullCalendar 
                    v-if="!loadingAuthStatus && !authError && !loadingCalendarEvents"
                    :options="calendarOptions"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

      </div>

      <!-- Modals from calender.vue, placed at the root of home-page -->
      <EventFormModal 
        v-if="showEventModal"
        :selected-date="eventModalDate"
        :event-to-edit="eventToEdit" 
        @close="closeEventModal"
        @save="handleSaveEvent"
      />

      <DayDetailModal
        v-if="showDayDetailModal"
        :selected-date="eventModalDate" 
        :events-for-day="dayDetailEvents"
        :event-type-colors="eventTypeColors"
        :can-edit-events="currentUser.isSuperuser" 
        @close="closeDayDetailModal"
        @request-add-event="openEventFormForSelectedDate"
        @request-delete-event="handleDeleteEventRequest"
        @request-edit-event="openEventFormForEdit"
        @request-toggle-complete="handleToggleEventCompletion"
      />

      <!-- NEW PERSONAL STATS SECTION -->
      <section class="personal-stats-section">
        <div class="stats-super-card">
          <h2>个人数据统计</h2>
          <div class="stats-card-grid-container">
            <div class="stat-card stat-card-tech">
              <h3>技术</h3>
              <p>展示我的技术栈、项目贡献和学习历程。</p>
              <div class="stat-placeholder-content">(技能雷达图或项目列表)</div>
            </div>
            <router-link to="/map" class="stat-card stat-card-map router-link-no-style">
              <h3>Space</h3>
              <p>This is my travel footprint. And currently I'm living in Suzhou, China.</p>
              <FootprintMap />
            </router-link>
            <div class="stat-card stat-card-gaming">
              <h3>游戏</h3>
              <p>盘点我的游戏库、时长和那些难忘的虚拟冒险。</p>
              <div class="stat-placeholder-content">(常玩游戏或成就统计)</div>
            </div>
            <div class="statistics-button-container statistics-button-grid-item">
              <button class="statistics-button">查看完整统计</button>
            </div>
          </div>
        </div>
      </section>
      <!-- END OF NEW PERSONAL STATS SECTION -->
    </div>
  </template>
  
  <script>
  import FullCalendar from '@fullcalendar/vue3';
  import dayGridPlugin from '@fullcalendar/daygrid';
  import interactionPlugin from '@fullcalendar/interaction';
  import timeGridPlugin from '@fullcalendar/timegrid';

  // 移除 FullCalendar 的核心和插件样式导入，让组件和插件自行处理
  // import '@fullcalendar/core/main.css';
  // import '@fullcalendar/daygrid/main.css';
  // import '@fullcalendar/timegrid/main.css';

  import EventFormModal from './EventFormModal.vue'; 
  import DayDetailModal from './DayDetailModal.vue'; 
  import FootprintMap from './FootprintMap.vue';

  export default {
    name: 'HomePage',
    components: {
      FullCalendar, 
      EventFormModal,
      DayDetailModal,
      FootprintMap,
    },
    data() {
      // const today = new Date(); // 移除未使用的局部变量 today
      return {
        currentUser: { isAuthenticated: false, isSuperuser: false },
        loadingAuthStatus: true,
        authError: null,
        
        calendarOptions: { 
          plugins: [ dayGridPlugin, interactionPlugin, timeGridPlugin ],
          initialView: 'dayGridMonth',
          headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: 'today dayGridMonth,timeGridWeek' 
          },
          editable: true, 
          selectable: true, 
          weekends: true,
          events: [], 
          dateClick: this.handleDateClick, 
          eventClick: this.handleEventClick, 
          height: 'auto', 
          aspectRatio: 1.2, 
          eventDisplay: 'block', 
          dayHeaderFormat: { weekday: 'short' }, 
          slotMinTime: '08:00:00', 
          slotMaxTime: '20:00:00', 
          contentHeight: 'auto',
          displayEventTime: false,
        },
        rawCalendarEvents: [], 
        loadingCalendarEvents: true,
        calendarEventsError: null,
        
        eventTypeColors: {
            holiday: 'red',
            memo: 'purple',
            log: 'green',
            other: 'gray',
        },

        showEventModal: false,    
        eventModalDate: null,   
        eventToEdit: null, 
        showDayDetailModal: false, 
        dayDetailEvents: [], 
        
        latestTimelineEvents: [],
        loadingTimeline: true,
        timelineError: null,
      };
    },
    async mounted() {
      await this.fetchAuthStatus();
      await this.fetchLatestTimelineEvents();
      await this.fetchCalendarEvents(); 
    },
    methods: {
      getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
      },
      async fetchAuthStatus() {
        this.loadingAuthStatus = true;
        this.authError = null;
        try {
          const response = await fetch('/api/auth-status/', { credentials: 'include' });
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          const data = await response.json();
          this.currentUser.isAuthenticated = data.is_authenticated;
          this.currentUser.isSuperuser = data.is_superuser; 
        } catch (error) {
          console.error('Error fetching auth status for homepage calendar:', error);
          this.authError = '无法加载用户权限信息。';
          this.currentUser.isAuthenticated = false;
          this.currentUser.isSuperuser = false;
        } finally {
          this.loadingAuthStatus = false;
        }
      },
      handleDateClick(clickInfo) {
        if (this.loadingAuthStatus || this.authError) return;
        this.eventModalDate = clickInfo.date; 
        this.filterEventsForDayDetail(clickInfo.date);
        this.showDayDetailModal = true;
        this.eventToEdit = null; 
      },
      handleEventClick(clickInfo) {
        if (this.loadingAuthStatus || this.authError) return;
        const clickedEventId = clickInfo.event.id; 
        const originalEvent = this.rawCalendarEvents.find(e => e.id.toString() === clickedEventId);
        if (originalEvent) {
          this.eventModalDate = clickInfo.event.start; 
          this.filterEventsForDayDetail(clickInfo.event.start);
          this.showDayDetailModal = true;
          this.eventToEdit = null; 
        } else {
          console.warn('Could not find original event for id:', clickedEventId);
        }
      },
      filterEventsForDayDetail(dateObj) { 
        const selectedDayStart = new Date(dateObj.getFullYear(), dateObj.getMonth(), dateObj.getDate()).getTime();
        const selectedDayEnd = new Date(dateObj.getFullYear(), dateObj.getMonth(), dateObj.getDate(), 23, 59, 59, 999).getTime();
        this.dayDetailEvents = this.rawCalendarEvents.filter(event => {
          const eventDate = new Date(event.start_time);
          if (isNaN(eventDate.getTime())) return false;
          const eventStartTime = eventDate.getTime();
          return eventStartTime >= selectedDayStart && eventStartTime <= selectedDayEnd;
        });
      },
      closeEventModal() { 
        this.showEventModal = false;
        this.eventToEdit = null; 
      },
      async handleSaveEvent(eventData) { 
        if (!this.currentUser.isSuperuser) {
          this.calendarEventsError = "抱歉，只有超级用户才能保存事件。";
          this.closeEventModal();
          return;
        }
        this.calendarEventsError = null; 
        const method = eventData.id ? 'PUT' : 'POST';
        const url = eventData.id ? `/api/calendar-events/${eventData.id}/` : '/api/calendar-events/';
        const csrftoken = this.getCookie('csrftoken');
        try {
          const response = await fetch(url, {
            method: method,
            credentials: 'include',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
            body: JSON.stringify(eventData),
          });
          if (!response.ok) {
            const errorBody = await response.json().catch(() => response.text()); 
            throw new Error(`HTTP ${response.status}: ${JSON.stringify(errorBody)}`);
          }
          this.closeEventModal();
          await this.fetchCalendarEvents(); 
          if (this.showDayDetailModal && this.eventModalDate) {
              this.filterEventsForDayDetail(this.eventModalDate);
          }
        } catch (e) {
          console.error('Error saving event from homepage:', e);
          this.calendarEventsError = `保存事件失败: ${e.message}`;
        }
      },
      closeDayDetailModal() { 
        this.showDayDetailModal = false;
        this.dayDetailEvents = [];
      },
      openEventFormForSelectedDate() { 
        if (!this.currentUser.isSuperuser) {
          alert("抱歉，只有超级用户才能添加事件。");
          return;
        }
        this.showDayDetailModal = false; 
        this.eventToEdit = null; 
        this.showEventModal = true;    
      },
      openEventFormForEdit(event) {  
        if (!this.currentUser.isSuperuser) {
          alert("抱歉，只有超级用户才能编辑事件。");
          return;
        }
        this.showDayDetailModal = false;
        this.eventToEdit = event; 
        this.showEventModal = true; 
      },
      async handleDeleteEventRequest(eventId) { 
        if (!this.currentUser.isSuperuser) {
          alert("抱歉，只有超级用户才能删除事件。");
          return;
        }
        this.calendarEventsError = null;
        const csrftoken = this.getCookie('csrftoken');
        try {
          const response = await fetch(`/api/calendar-events/${eventId}/`, {
            method: 'DELETE', credentials: 'include', headers: { 'X-CSRFToken': csrftoken }
          });
          if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, details: ${errorText}`);
          }
          await this.fetchCalendarEvents(); 
          if (this.showDayDetailModal && this.eventModalDate) {
            this.filterEventsForDayDetail(this.eventModalDate);
          } else if (this.showDayDetailModal) {
              this.closeDayDetailModal();
          }
        } catch (e) {
          console.error('Error deleting event from homepage:', e);
          this.calendarEventsError = `删除事件失败: ${e.message}`;
        }
      },
      async handleToggleEventCompletion(payload) {
        if (!this.currentUser.isSuperuser) {
          alert("抱歉，只有超级用户才能更新事件状态。");
          return;
        }
        this.calendarEventsError = null;
        const csrftoken = this.getCookie('csrftoken');
        try {
          const response = await fetch(`/api/calendar-events/${payload.id}/`, {
            method: 'PATCH',
            credentials: 'include',
            headers: { 
              'Content-Type': 'application/json', 
              'X-CSRFToken': csrftoken 
            },
            body: JSON.stringify({ is_completed: payload.is_completed }),
          });
          if (!response.ok) {
            const errorBody = await response.json().catch(() => response.text()); 
            throw new Error(`HTTP ${response.status}: ${JSON.stringify(errorBody)}`);
          }
          // 更新成功，重新获取所有事件以刷新日历和原始数据列表
          await this.fetchCalendarEvents(); 
          // 如果 DayDetailModal 仍然打开，确保其内容也刷新
          if (this.showDayDetailModal && this.eventModalDate) {
              this.filterEventsForDayDetail(this.eventModalDate);
          }
        } catch (e) {
          console.error('Error toggling event completion status:', e);
          this.calendarEventsError = `更新事件状态失败: ${e.message}`;
          // 可选：如果失败，可能需要将UI状态回滚，但通常重新获取事件可以修正
        }
      },
      async fetchLatestTimelineEvents() { 
        this.loadingTimeline = true;
        this.timelineError = null;
        try {
          const response = await fetch('/api/timeline-events/');
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          this.latestTimelineEvents = await response.json();
        } catch (e) {
          console.error('Error fetching latest timeline events for homepage:', e);
          this.timelineError = '无法加载最新动态。';
          this.latestTimelineEvents = [];
        } finally {
          this.loadingTimeline = false;
        }
      },
      async fetchCalendarEvents() { 
        this.loadingCalendarEvents = true;
        this.calendarEventsError = null;
        try {
          const response = await fetch('/api/calendar-events/', { credentials: 'include' });
          if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, details: ${errorText}`);
          }
          const rawEventsData = await response.json();
          this.rawCalendarEvents = rawEventsData; 

          const formattedEvents = rawEventsData.map(event => {
            if (!event || typeof event.id === 'undefined') return null; 
            const eventDate = new Date(event.start_time);
            if (isNaN(eventDate.getTime())) return null;

            let displayTitle = event.title;
            if (typeof displayTitle === 'string') {
              displayTitle = displayTitle.replace(/^([0-9０-９]+)([.。])\s*/, '');
            }

            return {
              id: event.id.toString(), 
              title: displayTitle,       
              start: eventDate,         
              allDay: !event.start_time.includes('T'), 
              extendedProps: { ...event },
              backgroundColor: this.eventTypeColors[event.event_type] || this.eventTypeColors['other'],
              borderColor: this.eventTypeColors[event.event_type] || this.eventTypeColors['other'],
              classNames: event.is_completed ? ['completed-fc-event'] : []
            };
          }).filter(event => event !== null); 
          
          this.calendarOptions = {
            ...this.calendarOptions, 
            events: formattedEvents
          };

        } catch (e) {
          console.error('Error fetching calendar events for homepage:', e);
          this.calendarEventsError = `无法加载日历事件: ${e.message}`;
          this.rawCalendarEvents = [];
           this.calendarOptions = {
            ...this.calendarOptions,
            events: []
          };
        } finally {
          this.loadingCalendarEvents = false;
        }
      },
    }
  }
  </script>
  
  <style scoped>
  .home-page {
    max-width: 100%;
    margin: 0 auto;
    overflow-x: hidden; 
    position: relative; 
    min-height: 100vh; /* 确保背景应用到整个视口高度 */

    /* 新的背景效果 */
    background-color: #ECEFF1; /* 1. 整体的浅雾灰色底色 (Material Design Blue Grey 50) */
    background-image: radial-gradient(
      circle at center, 
      rgba(255, 255, 255, 0.9) 0%,    /* 中心白色，较高不透明度 */
      rgba(255, 255, 255, 0.8) 15%,   /* 过渡区域 */
      rgba(255, 255, 255, 0.4) 30%,
      rgba(236, 239, 241, 0) 55%     /* 外围逐渐透明到背景色，55% 控制模糊圆的大小 */
    );
    background-size: 180vmin 180vmin; /* 使用 vmin 确保圆形相对于视口较小的一边，使其更像一个圆 */
    background-position: center center;
    background-repeat: no-repeat;

    /* Ensure it can scroll if content overflows */
    overflow-y: auto; 
  }
  
  /* 移除 #particle-canvas-home 样式 */
  /*
  #particle-canvas-home {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 999; 
    background-color: lime !important; 
  }
  */
  
  .content-wrapper {
    width: 90%; /* Increased from 60% to allow more space for three columns */
    margin: 0 auto;
    position: relative; 
    z-index: 1; 
    /* background-color: transparent; 可选：如果希望内容区域背景透明以显示下方渐变 */
  }
  
  /* 移除 Webkit 滚动条隐藏规则 */
  /*
  .content-wrapper::-webkit-scrollbar {
    display: none;
  }
  */
  
  /* Hero section styles removed */
  
  /* Styles for the new introduction section */
  .new-introduction-section {
    position: relative;
    padding: 0px 20px 20px 20px;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    overflow: hidden; 
    min-height: 100vh; 
    box-sizing: border-box;
    width: 100%; 
    /* background-color: transparent; /* 例如，如果希望此section背景透明 */
  }
  
  .full-screen-intro {
      /* This class is now combined with .new-introduction-section rules for simplicity */
  }
  
  /* Ensure .dialogue-bubbles.left-bubbles and .right-bubbles are removed or commented out if they exist */
  .dialogue-bubbles, .left-bubbles, .right-bubbles {
      /* These are no longer used for direct bubble positioning */
      /* display: none; or remove rules */
  }
  
  /* Container for positioning individual bubbles */
  .bubble-instance-wrapper {
      position: absolute;
      /* transform applied here if needed for rotation of the whole stack */
  }
  
  /* Remove old individual bubble positioning - this will be reapplied to .bubble-instance-wrapper */
  /* .bubble-1 { top: 15%; left: 25%; transform: translate(-50%, -50%) rotate(-20deg); } ... etc */
  
  /* New Bubble Positioning - Applied to .bubble-instance-wrapper */
  /* Values are relative to .new-introduction-section */
  /* Ensuring vertical spread */
  .bubble-wrapper-1 { top: 12%; left: 15%; transform: rotate(-15deg); }
  .bubble-wrapper-2 { top: 40%; left: 8%; transform: rotate(5deg);  }
  .bubble-wrapper-3 { top: 68%; left: 12%; transform: rotate(-5deg);  }
  
  .bubble-wrapper-4 { top: 12%; right: 15%; transform: rotate(10deg); }
  .bubble-wrapper-5 { top: 40%; right: 8%; transform: rotate(-8deg); }
  .bubble-wrapper-6 { top: 68%; right: 12%; transform: rotate(15deg); }
  
  .intro-background-oval {
    position: absolute;
    width: 600px; /* 调整椭圆大小 */
    height: 600px; /* 调整椭圆大小 */
    border: 2px dashed #bae6fd;
    border-radius: 50%;
    opacity: 0.6;
    z-index: 0;
    top: 50%;
    left: 50%;
    transform: translate(-50%, calc(-50% - 50px)) rotate(-10deg);
    border-color: var(--border-color-light);
  }
  
  .intro-container {
    display: flex;
    flex-direction: row; 
    align-items: center; 
    justify-content: flex-start;
    position: relative;
    z-index: 1;
    width: 50%;  /* 改为100%，这样就会适应父容器的60%宽度 */
    max-width: 600px; 
    aspect-ratio: 16 / 9; 
    height: auto; 
    background-image: url('/beijing.jpg'); 
    background-size: cover; 
    background-position: center; 
    background-repeat: no-repeat; 
    padding: 0;
    margin-top: -50px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(var(--shadow-color-soft-rgb), 0.15);
    border: 2px solid var(--border-color-medium);
    overflow: hidden;
  }
  
  .intro-avatar-column {
    flex-basis: 50%; 
    display: flex;
    flex-direction: column; 
    justify-content: center; /* Center avatar vertically */
    align-items: center; /* Center avatar horizontally */
    padding: 20px; /* Add some padding inside the avatar column */
    box-sizing: border-box;
  }
  
  .profile-avatar-new {
    width: 130px; /* Increased size */
    height: 130px; /* Increased size */
    max-width: 100%; 
    object-fit: cover;
    border-radius: 50%;
    border: 3px solid var(--primary-600);
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  }
  
  .intro-text-column {
    flex-basis: 50%; 
    display: flex; /* To allow .intro-text-card to take full height */
    flex-direction: column; /* Stack children (the card) */
    /* justify-content: center; */ /* Centering handled by text-card */
    /* width: auto; */ /* Not needed with flex-basis */
  }
  
  .intro-text-card {
    background-image: var(--background-intro-text-card);
    padding: 30px; /* Adjusted padding */
    border-radius: 0; /* Remove border-radius to be flush with parent right angles */
    /* box-shadow: 0 5px 10px rgba(var(--shadow-color-soft-rgb), 0.08); */ /* Optional: remove shadow if flush */
    border: none; /* Optional: remove border if flush */
    border-left: 1px solid var(--border-color-light); /* Optional: add a subtle separator */
    text-align: left; 
    width: 100%; 
    height: 100%; /* Make card take full height of its column */
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center; /* Vertically center text content */
  }
  
  .label-my-name-is{
    display: block; /* 确保显示 */
    visibility: visible; /* 确保可见 */
    font-size: 0.9em;
    color: var(--primary-800);
    margin-bottom: 4px;
    text-align: left; /* Ensure left alignment */
  }
  .label-im-a {
    display: block; /* 确保显示 */
    visibility: visible; /* 确保可见 */
    font-size: 0.9em;
    color: var(--primary-800);
    margin-bottom: 4px;
    text-align: left; /* Ensure left alignment */
  }
  
  .main-name-new {
    font-size: 2.2em;
    color: var(--primary-600);
    margin-top: 50px;
    margin-bottom: 8px;
    font-weight: 600;
    text-align: left; /* Ensure left alignment */
  }
  
  .name-separator-new {
    border: 0;
    height: 1px;
    background-color: var(--border-color-light);
    margin: 10px 0 15px;
  }
  
  .roles-new {
    list-style-type: none;
    padding-left: 0;
    margin-top: 5px;
    color: var(--text-primary);
  }
  
  .roles-new li {
    font-size: 0.95em;
    margin-bottom: 6px;
    line-height: 1.5;
  }
  
  /* Floating Icons Placeholders - Adjusting positions to be closer to the central circle */
  .floating-icons-area {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: 2;
    pointer-events: none;
    transform: translateY(-50px);
  }
  
  .f-icon {
    position: absolute;
    width: 45px; /* 30px * 1.5 */
    height: 45px; /* 30px * 1.5 */
    background-color: var(--icon-placeholder-bg);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px; /* 14px * 1.5, if needed for title text */
    color: var(--icon-placeholder-text);
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    /* Basic icons using pseudo-elements for demo */
  }
  
  .f-icon::before {
   content: attr(title);
   font-weight: bold;
  }
  
  .chrome-icon { /* Nikon */
    left: calc(50% - 240px);
    top: calc(50% - 180px);
    transform: translate(-50%, -50%);
    background-color: var(--icon-chrome-bg);
    color: var(--icon-common-text);
  }
  /* .chrome-icon::before { content: "G";} */
  
  .eth-icon { /* Ethereum */
    left: calc(50% + 240px);
    top: calc(50% - 180px);
    transform: translate(-50%, -50%);
    background-color: var(--icon-eth-bg);
    color: var(--icon-common-text);
    /* font-family: sans-serif; */
  }
  /* .eth-icon::before { content: "Ξ";} */
  
  .edge-icon { /* Edge */
    left: 50%;
    top: calc(50% + 300px);
    transform: translate(-50%, -50%);
    background-color: var(--icon-edge-bg);
    color: var(--icon-common-text);
  }
  /* .edge-icon::before { content: "E";} */
  
  .content-cards-section {
    padding: 40px 0; /* Changed from 40px 20px to remove horizontal padding */
    margin: 40px auto;
    box-sizing: border-box;
  }
  
  .content-cards-section h2 {
    text-align: center;
    margin-bottom: 30px;
    color: var(--text-headings) !important; 
  }
  
  .card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px; 
    justify-content: center;
  }
  
  .card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
    padding: 25px;
    flex-basis: calc((100% - 40px) / 3); /* Changed from width and adjusted formula for 3 columns with 20px gap */
    min-width: 280px; /* Keep for responsiveness */
    box-sizing: border-box; /* Add this line to include padding and border in the element's total width and height */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid #E5E7EB; /* 浅灰色边框 */
  }
  
  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  }
  
  .card h3 {
    color: #1F2937; /* 深灰色标题 */
    margin-top: 0;
    margin-bottom: 15px;
  }
  
  .card p {
    color: #4B5563; /* 中灰色文字 */
    line-height: 1.6;
    margin-bottom: 20px;
  }
  
  .card-link {
    display: inline-block;
    color: #3B82F6; /* 链接颜色，根据配色调整 */
    text-decoration: none;
    font-weight: bold;
  }
  
  .card-link:hover {
    text-decoration: underline;
  }
  
  /* 响应式设计：小屏幕上卡片堆叠 */
  @media (max-width: 992px) {
    .content-wrapper {
      width: 80%;
    }
    .card {
      width: calc(50% - 30px);
    }
  }
  
  @media (max-width: 768px) {
    /* .hero-section h1 removed */
    .content-wrapper {
      width: 95%; 
    }
    .card {
      width: 100%;
      margin-bottom: 20px;
    }
    .card-container {
      flex-direction: column;
      align-items: center;
    }
    .new-introduction-section,
    .content-cards-section {
    }
    .intro-container {
      flex-direction: column; 
      width: 90vw; 
      max-width: 380px; /* Adjusted mobile max-width slightly */
      height: auto; 
      aspect-ratio: unset; 
      padding: 15px;
      transform: translateY(-5vh); /* Less upward movement on mobile */
    }
    .intro-avatar-column {
      align-items: center; 
      margin-bottom: 15px; 
      flex-basis: auto; 
      padding: 10px; /* Reduced padding for mobile */
    }
    .intro-text-column {
      flex-basis: auto; 
      align-items: center; 
    }
    .intro-text-card {
      text-align: center; 
      height: auto; /* Allow height to adjust on mobile */
      padding: 20px;
      border-left: none; /* Remove separator on mobile stacked view */
      border-radius: 10px; /* Add back some radius for mobile card */
    }
    .label-my-name-is,
    .label-im-a,
    .main-name-new {
      text-align: center; /* Center these text elements on mobile */
    }
    .profile-avatar-new {
      width: 100px; /* Avatar size on mobile */
      height: 100px;
    }
    .main-name-new {
      font-size: 1.8em;
    }
    .roles-new li {
      font-size: 0.9em;
    }
    .bubble-instance-wrapper { /* Adjust bubble positions for mobile */
        position: relative; /* Change to relative for simpler stacking */
        top: auto; left: auto; right: auto; transform: none; /* Reset absolute positioning */
        margin: 10px auto; /* Center them and add some space */
        width: fit-content;
    }
    .floating-icons-area { display: none; } /* Hide decorative icons on small screens */
    .intro-background-oval { display: none; } /* Hide oval on small screens */
  }
  
  .bubble {
    background-image: var(--background-bubble);
    color: var(--text-bubble);
    padding: 10px 18px; /* Adjusted padding */
    border-radius: 12px; /* Slightly less rounded to match image */
    position: relative; /* Changed from absolute for ::before positioning context */
    z-index: 1; /* Main bubble content on top */
    box-shadow: 0 4px 8px rgba(var(--shadow-color-soft-rgb), 0.15); /* Shadow on the top layer */
    font-size: 0.95em;
    min-width: 70px;
    text-align: center;
    border: 1px solid var(--border-color-light);
  }
  
  .bubble::before {
    content: '';
    position: absolute;
    left: 4px;
    top: 4px;
    width: 100%;
    height: 100%;
    background-image: var(--background-bubble); /* Same background or slightly darker/desaturated */
    opacity: 0.7;
    border-radius: 12px;
    z-index: -1; /* Behind the main bubble content */
    border: 1px solid var(--border-color-light);
  }

  /* 基础时间轴占位符样式 */
  .basic-timeline {
    margin-top: 20px;
    margin-bottom: 20px;
    border-left: 2px solid #e0e0e0; /* 时间轴的中心线 */
    padding-left: 20px;
  }

  .timeline-item {
    position: relative;
    margin-bottom: 20px;
  }

  .timeline-item:last-child {
    margin-bottom: 0;
  }

  .timeline-dot {
    position: absolute;
    left: -31px; /* 根据边框和内边距调整，使其在中心线上 */
    top: 4px;    /* 根据文本行高调整垂直位置 */
    width: 10px;
    height: 10px;
    background-color: #3B82F6; /* 与链接颜色一致 */
    border-radius: 50%;
    border: 2px solid white; /* 给点添加一个白色边框，使其更突出 */
  }

  .timeline-content .timeline-date {
    display: block;
    font-size: 0.85em;
    color: #6B7280; /* 日期颜色 */
    margin-bottom: 5px;
  }

  .timeline-content p {
    font-size: 0.95em;
    color: #374151; /* 内容颜色 */
    line-height: 1.5;
    margin-bottom: 0; /* 移除默认的p标签下边距 */
  }

  /* 移除之前添加的 custom-timeline-section 的所有CSS */
  /* .custom-timeline-section, .timeline-intro, .timeline-card-container, .timeline-phase, etc. */

  /* 响应式设计 */
  @media (max-width: 992px) {
    .content-wrapper {
      width: 80%;
    }
    .card,
    .card-timeline-placeholder {
      flex-basis: calc(50% - 10px); /* 小屏幕上，每行两个 */
    }
  }
  
  @media (max-width: 768px) {
    .content-wrapper {
      width: 95%;
    }
    .card,
    .card-timeline-placeholder {
      flex-basis: 100%; /* 更小屏幕上，每行一个 */
      margin-bottom: 20px;
    }
    .card-container {
      flex-direction: column;
      align-items: center;
    }
    /* ... (其他移动端样式) ... */
  }

  .card-calendar { /* Specific styles for the calendar card */
    display: flex;
    flex-direction: column;
  }

  .mini-calendar-container {
    flex-grow: 1; /* Allow calendar to take available space in card */
    display: flex;
    flex-direction: column; /* Stack loading message and calendar */
    justify-content: center; /* Center content vertically */
    align-items: center; /* Center content horizontally */
    min-height: 300px; /* Give it some minimum height for loading/error and calendar */
    margin-top: 15px;
    margin-bottom: 10px;
    width: 100%; 
    padding: 5px; /* Add some padding around FullCalendar */
    box-sizing: border-box;
  }

  /* FullCalendar specific styling adjustments */
  :deep(.fc .fc-toolbar-title) {
    font-size: 1.1em; /* Smaller title */
  }
  :deep(.fc .fc-button) {
    font-size: 0.8em; /* Smaller buttons */
    padding: 0.3em 0.5em;
  }
  :deep(.fc .fc-daygrid-day-number) {
      font-size: 0.85em; /* Smaller day numbers */
  }
  :deep(.fc .fc-event) {
      font-size: 0.75em; /* Smaller event text */
  }
  :deep(.fc-daygrid-day) {
    height: auto !important; /* Let content height push day height */
    min-height: 40px; /* Minimal height for a day cell */
  }
  :deep(.fc-daygrid-day-events) {
    min-height: 20px !important; /* Ensure space for at least one event or more link */
  }

  /* Align items in FullCalendar header */
  :deep(.fc-header-toolbar) {
    display: flex;
    align-items: center; /* Vertically align the chunks */
    justify-content: space-between; /* Ensure chunks are spaced out */
  }

  :deep(.fc-toolbar-chunk) {
    display: flex;
    align-items: center; /* Vertically align items within each chunk */
  }

  /* Specific adjustment for the title to ensure it aligns well with buttons */
  :deep(.fc-toolbar-title) {
    margin-left: 0.5em; /* Add some space if it's too close to left buttons */
    margin-right: 0.5em; /* Add some space if it's too close to right buttons */
    line-height: 1.2; /* Adjust line-height if necessary for vertical centering with buttons */
  }

  /* Ensure button groups are also aligned */
  :deep(.fc-button-group) {
    display: flex;
    align-items: center;
  }

  /* 为已完成的 FullCalendar 事件添加删除线样式 */
  :deep(.fc-event.completed-fc-event .fc-event-title),
  :deep(.fc-event.completed-fc-event .fc-event-time) { /* 也可以应用于时间 */
    text-decoration: line-through;
    color: #888 !important; /* 使用 !important 确保覆盖 FullCalendar 默认颜色 */
  }
  :deep(.fc-event.completed-fc-event) {
    opacity: 0.7; /* 让已完成事件稍微不那么突出 */
  }

  /* Loading/Error messages for calendar card (保持之前定义的) */
  .calendar-loading-message,
  .calendar-error-message {
    padding: 10px;
    text-align: center;
    font-size: 0.9em;
    border-radius: 4px;
    margin: 10px 0;
    width: 80%; /* Make messages not too wide */
  }
  .calendar-loading-message {
    background-color: #f0f0f0;
  }
  .calendar-error-message {
    background-color: #f8d7da;
    color: #721c24;
  }

  /* Ensure modals are styled correctly and appear on top */
  /* (Modal styles are usually global or self-contained in their components) */
  /* If they appear behind, z-index might be needed for .home-page or modals */

  /* New styles for the super card */
  .main-content-super-card {
    background-color: white;
    border-radius: 16px; /* Slightly larger radius for a container card */
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); /* A bit more pronounced shadow */
    padding: 30px;
    margin-bottom: 30px;
    box-sizing: border-box;
    max-width: 89%; /* Unify width with the stats section */
    margin-left: auto; /* Center the super card */
    margin-right: auto; /* Center the super card */
  }

  .main-content-super-card h2 { /* Adjust heading inside the super card */
    text-align: center; 
    margin-top: 0; /* Remove top margin if padding from super-card is enough */
    margin-bottom: 25px; /* Space before the card-container */
    color: var(--text-headings) !important;
  }
  /* End of new styles */

  /* Styles for Personal Stats Section */
  .personal-stats-section {
    padding: 20px 0; /* Adjusted padding as it's inside content-wrapper */
    margin-top: 40px;
  }

  .personal-stats-section h2 {
    text-align: center;
    margin-bottom: 30px;
    color: var(--text-headings);
    font-size: 1.8em;
  }

  .stats-card-grid-container {
    display: grid;
    gap: 20px;
    grid-template-columns: repeat(4, 1fr);
    grid-template-areas:
      "tech tech map map"
      "gaming gaming map map"
      "button button button button";
    width: 100%; /* Fill the new stats-super-card */
  }

  .router-link-no-style {
    text-decoration: none;
    color: inherit;
  }

  .stat-card-tech { grid-area: tech; }
  .stat-card-map { grid-area: map; }
  .stat-card-gaming { grid-area: gaming; }
  .statistics-button-grid-item { grid-area: button; }

  .stat-card {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    padding: 20px;
    min-height: 180px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.12);
  }

  .stat-card h3 {
    color: #1F2937;
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 1.25em;
  }

  .stat-card p {
    color: #4B5563;
    line-height: 1.6;
    margin-bottom: 15px;
    font-size: 0.9em;
    flex-grow: 1;
  }

  .stat-placeholder-content {
    background-color: #f3f4f6;
    border: 1px dashed #e5e7eb;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    color: #6b7280;
    font-size: 0.85em;
    min-height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: auto;
  }

  .statistics-button-container {
    margin-top: 0;
    margin-bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .statistics-button {
    background-color: var(--primary-600, #3B82F6);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 30px;
    font-size: 1.1em;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
    box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
  }

  .statistics-button:hover {
    background-color: var(--primary-700, #2563EB);
    transform: translateY(-2px);
  }

  /* Styles for the new stats-super-card, mirroring main-content-super-card */
  .stats-super-card {
    background-color: white;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    padding: 30px;
    margin-bottom: 30px; /* Or match .main-content-super-card's margin */
    box-sizing: border-box;
    max-width: 80%;
    margin-left: auto;
    margin-right: auto;
  }
  </style> 