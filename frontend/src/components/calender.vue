<template>
  <div class="calendar-page">
    <div v-if="loadingAuthStatus && !authError && !eventsError" class="loading-message">验证用户权限中...</div>
    <div v-else-if="loadingEvents && !authError && !eventsError && !showEventModal && !showDayDetailModal" class="loading-message">加载事件中...</div>
    <div v-if="authError" class="error-message">无法验证用户权限: {{ authError }}</div>
    <div v-if="eventsError && !showEventModal && !showDayDetailModal" class="error-message">{{ eventsError }}</div>
    
    <div v-if="!loadingEvents && !eventsError && !loadingAuthStatus && !authError">
      <div class="calendar-controls">
        <button @click="setView('month')" :class="{ 'active-view': currentView === 'month' }">月视图</button>
        <button @click="setView('week')" :class="{ 'active-view': currentView === 'week' }">周视图</button>
        <!-- 年视图按钮可以后续添加 -->
      </div>
      <div class="calendar-wrapper">
        <v-calendar
          class="custom-calendar"
          :is-expanded="true"
          :attributes="attributes"
          :view="currentView" 
          @dayclick="handleDayClick"
          @update:from-page="handlePageUpdate" 
        >
          <template #day-content="{ day, attributes }">
            <div class="calendar-day-cell-custom">
              <span class="day-label-custom">{{ day.day }}</span>
              <div class="event-titles-container-custom">
                <div v-for="attr in getEventsForDay(day, attributes)" :key="attr.key">
                  <p v-if="attr.customData && attr.customData.title"
                    class="event-title-in-cell-custom"
                    :style="{ backgroundColor: eventTypeColors[attr.customData.event_type] || eventTypeColors['other'] }"
                  >
                    {{ attr.customData.title }}
                  </p>
                </div>
              </div>
            </div>
          </template>
        </v-calendar>
      </div>
    </div>
    
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
    />

    <!-- Global add button can be added later -->
    <!-- <button @click="openGlobalAddEventModal" class="global-add-event-btn">添加事件</button> -->

  </div>
</template>

<script>
import { Calendar as VCalendar } from 'v-calendar';
import 'v-calendar/dist/style.css';
import EventFormModal from './EventFormModal.vue';
import DayDetailModal from './DayDetailModal.vue'; // Import DayDetailModal

export default {
  name: 'CalendarPage',
  components: {
    VCalendar,
    EventFormModal,
    DayDetailModal, // Register DayDetailModal
  },
  data() {
    const today = new Date();
    return {
      currentView: 'month', // 'month' or 'week'
      selectedDate: null, 
      todayAttribute: { 
        key: 'today',
        highlight: true, // Simplified highlight
        dates: today,
      },
      attributes: [], 
      calendarEvents: [], 
      loadingEvents: true,
      eventsError: null,
      eventTypeColors: { 
        holiday: 'red',
        memo: 'purple',
        log: 'green',
        other: 'gray',
      },
      showEventModal: false,    
      eventModalDate: null,   // Shared date for both modals (Date object)
      eventToEdit: null, // Used to pass an event to EventFormModal for editing

      showDayDetailModal: false, // Controls DayDetailModal visibility
      dayDetailEvents: [], // Events for the selected day shown in DayDetailModal
      currentUser: {
        isAuthenticated: false,
        isSuperuser: false,
      },
      loadingAuthStatus: true,
      authError: null,
    };
  },
  async mounted() {
    console.log('[CalenderPage] Mounted');
    await this.fetchAuthStatus();
    await this.fetchCalendarEvents();
  },
  methods: {
    setView(view) {
      this.currentView = view;
    },
    handlePageUpdate(page) {
      // Optional: Handle page changes if needed, for example to fetch events for the new range
      console.log('Calendar page updated:', page);
    },
    getEventsForDay(day, allAttributes) {
      // Filter attributes that are actual events and belong to the current day.
      // This is a simplified example; v-calendar might pass attributes differently for day cells vs. events.
      // You might need to adjust this based on how 'attributes' are structured for events.
      return allAttributes.filter(attr => {
        if (!attr.customData || !attr.customData.isEvent) return false; // Assuming events have 'isEvent: true' in customData
        
        // Check if the event's date matches the current day object
        // The 'day.date' is a Date object for the cell.
        // Event attributes usually have a 'dates' property.
        if (attr.dates) {
          if (Array.isArray(attr.dates)) {
            return attr.dates.some(d => 
              d.getFullYear() === day.date.getFullYear() &&
              d.getMonth() === day.date.getMonth() &&
              d.getDate() === day.date.getDate()
            );
          } else { // Assuming single date object
             return attr.dates.getFullYear() === day.date.getFullYear() &&
                    attr.dates.getMonth() === day.date.getMonth() &&
                    attr.dates.getDate() === day.date.getDate();
          }
        }
        return false;
      });
    },
    getCookie(name) { // RE-ADD getCookie method directly in the component
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
      console.log('[CalenderPage fetchAuthStatus] Fetching auth status...');
      try {
        const response = await fetch('/api/auth-status/', {
          credentials: 'include',
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('[CalenderPage fetchAuthStatus] Auth status response data (raw):', data); // Log raw data
        console.log('[CalenderPage fetchAuthStatus] API responded with is_authenticated:', data.is_authenticated);
        console.log('[CalenderPage fetchAuthStatus] API responded with is_superuser:', data.is_superuser); // Specific log for is_superuser from API
        
        this.currentUser.isAuthenticated = data.is_authenticated;
        this.currentUser.isSuperuser = data.is_superuser; 
        
        console.log('[CalenderPage fetchAuthStatus] this.currentUser.isAuthenticated after assignment:', this.currentUser.isAuthenticated);
        console.log('[CalenderPage fetchAuthStatus] this.currentUser.isSuperuser after assignment:', this.currentUser.isSuperuser); // Specific log for component state
        console.log('[CalenderPage fetchAuthStatus] Full currentUser state updated:', JSON.parse(JSON.stringify(this.currentUser)));
      } catch (error) {
        console.error('Error fetching auth status:', error);
        this.authError = '无法加载用户权限信息。';
        this.currentUser.isAuthenticated = false;
        this.currentUser.isSuperuser = false;
      } finally {
        this.loadingAuthStatus = false;
      }
    },
    handleDayClick(day) {
      console.log('[CalendarPage] handleDayClick called. loadingAuthStatus:', this.loadingAuthStatus, 'authError:', this.authError);
      if (this.loadingAuthStatus || this.authError) {
        console.warn('[CalendarPage] handleDayClick aborted due to auth status.');
        return;
      }
      
      this.selectedDate = day; 
      this.eventModalDate = day.date; 
      this.filterEventsForDayDetail(day.date);
      this.showDayDetailModal = true;
      this.eventToEdit = null; 
    },
    filterEventsForDayDetail(dateObj) {
      const selectedDayStart = new Date(dateObj.getFullYear(), dateObj.getMonth(), dateObj.getDate()).getTime();
      const selectedDayEnd = new Date(dateObj.getFullYear(), dateObj.getMonth(), dateObj.getDate(), 23, 59, 59, 999).getTime();
      this.dayDetailEvents = this.calendarEvents.filter(event => {
        const eventStartTime = new Date(event.start_time).getTime();
        return eventStartTime >= selectedDayStart && eventStartTime <= selectedDayEnd;
      });
    },
    closeEventModal() {
      this.showEventModal = false;
      this.eventToEdit = null; 
    },
    async handleSaveEvent(eventData) {
      if (!this.currentUser.isSuperuser) {
        this.eventsError = "抱歉，只有超级用户才能保存事件。";
        this.closeEventModal(); // Close modal as action is disallowed
        return;
      }
      this.eventsError = null; 
      const method = eventData.id ? 'PUT' : 'POST';
      const url = eventData.id ? `/api/calendar-events/${eventData.id}/` : '/api/calendar-events/';
      const csrftoken = this.getCookie('csrftoken');

      try {
        const response = await fetch(url, {
          method: method,
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
          },
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
        console.error('Error saving event:', e);
        this.eventsError = `保存事件失败: ${e.message}`;
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
        // Error message will be shown by DayDetailModal or handled by its button visibility
        // For now, just ensure we don't proceed.
        alert("抱歉，只有超级用户才能删除事件。");
        return;
      }
      this.eventsError = null;
      const csrftoken = this.getCookie('csrftoken');
      try {
        const response = await fetch(`/api/calendar-events/${eventId}/`, {
          method: 'DELETE',
          credentials: 'include',
          headers: {
            'X-CSRFToken': csrftoken,
          }
        });
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`HTTP error! status: ${response.status}, details: ${errorText}`);
        }
        await this.fetchCalendarEvents(); 
        // If DayDetailModal is still open and for the same date, update its list
        // This ensures that if deletion is quick, the list refreshes.
        if (this.showDayDetailModal && this.eventModalDate) {
          this.filterEventsForDayDetail(this.eventModalDate);
        } else if (this.showDayDetailModal) {
            // If it was some other date (should not happen with current flow but as safeguard)
            this.closeDayDetailModal();
        }
      } catch (e) {
        console.error('Error deleting event:', e);
        this.eventsError = `删除事件失败: ${e.message}`;
      }
    },
    async fetchCalendarEvents() {
      this.loadingEvents = true;
      this.eventsError = null;
      console.log('[CalenderPage fetchCalendarEvents] Fetching calendar events...');
      try {
        const response = await fetch('/api/calendar-events/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('[CalenderPage fetchCalendarEvents] Raw events data from API:', data);

        this.calendarEvents = data.map(event => {
          if (!event || typeof event.id === 'undefined') {
            console.warn('[CalenderPage] Event data is invalid or missing id, skipping:', event);
            return null;
          }
          const eventDate = new Date(event.start_time);
          if (isNaN(eventDate.getTime())) {
            console.warn(`[CalenderPage] Invalid start_time for event id ${event.id}: "${event.start_time}". Skipping this event.`);
            return null; // Mark for removal
          }
          return {
            key: event.id.toString(), 
            customData: {
              ...event, // Spread all event properties
              title: event.title, 
              description: event.description,
              event_type: event.event_type,
              isEvent: true // Add a flag to identify these as events for the #day-content slot
            },
            dates: eventDate, // Use the validated Date object
            dot: { 
              color: this.eventTypeColors[event.event_type] || this.eventTypeColors['other'],
            },
          };
        }).filter(event => event !== null); // Filter out any null (skipped) events
        
        // Combine event attributes with the 'today' attribute
        this.attributes = [this.todayAttribute, ...this.calendarEvents];
        console.log('[CalenderPage fetchCalendarEvents] Processed attributes for calendar:', JSON.parse(JSON.stringify(this.attributes)));

      } catch (error) {
        console.error('Error fetching calendar events:', error);
        this.eventsError = '无法加载日历事件。';
      } finally {
        this.loadingEvents = false;
      }
    },
  },
  computed: {
    canUserEditEvents() {
      const canEdit = this.currentUser.isSuperuser;
      console.log('[CalenderPage computed canUserEditEvents]:', canEdit);
      return canEdit;
    }
  }
};
</script>

<style scoped>
.calendar-page {
  min-height: calc(100vh - 70px); /* Adjust 70px if navbar height is different */
  width: 100%;
  padding: 20px; 
  box-sizing: border-box;
  background-color: #f0f0f0; /* Light gray page background */
  display: flex;
  flex-direction: column;
  align-items: center; 
  /* justify-content: center; /* Centering wrapper if it's smaller than page */
}

.loading-message, .error-message {
  text-align: center;
  padding: 15px;
  font-size: 1.1em;
  margin-top: 20px; /* Give some space from top controls or calendar */
  margin-bottom: 20px;
  border-radius: 6px;
  width: 60%; 
  max-width: 500px; /* Max width for messages */
  margin-left: auto;
  margin-right: auto;
  /* Removed absolute positioning to flow with content better */
  z-index: 100; 
}

.loading-message {
  color: #333;
  background-color: #e9e9e9;
}

.error-message {
  color: #D8000C;
  background-color: #FFD2D2;
  border: 1px solid #D8000C;
}

.calendar-controls {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  justify-content: center; /* Center buttons */
}

.calendar-controls button {
  padding: 8px 15px;
  border: 1px solid #ccc;
  background-color: #f8f8f8;
  cursor: pointer;
  border-radius: 4px;
  font-size: 0.9em;
}

.calendar-controls button.active-view {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.calendar-wrapper {
  width: 90vw;    /* Make calendar significantly wider */
  height: 78vh;   /* Make calendar significantly taller */
  max-width: 1350px; /* Optional max width */
  /* background-color: lightgreen; */ /* Debug: Original green area color */
  /* border: 2px dashed darkgreen; */    /* Debug: Original green area border */
  border-radius: 8px; 
  padding: 10px; 
  box-sizing: border-box;
  display: flex; 
  flex-direction: column;
  background-color: #ffffff; /* Give the wrapper a background, e.g., white */
  box-shadow: 0 4px 12px rgba(0,0,0,0.1); /* Add some shadow for depth */
}

.custom-calendar { /* Class on <v-calendar> tag itself */
  width: 100%;
  flex-grow: 1; 
  display: flex; 
  flex-direction: column;
  border: none; /* Remove default border if wrapper has one */
}

/* Styles for event titles within calendar cells (new #day-content slot) */
.calendar-day-cell-custom {
  width: 100%;
  height: 100%; 
  display: flex;
  flex-direction: column;
  overflow: hidden; 
  position: relative; /* For positioning day number if needed */
}

.day-label-custom {
  font-size: 0.8em;
  text-align: left;
  padding: 3px 5px;
  align-self: flex-start; 
}

.event-titles-container-custom {
  flex-grow: 1;
  overflow-y: auto; 
  font-size: 0.78em;
  line-height: 1.3;
  padding: 0 3px 3px 3px; /* Add some padding */
}

.event-title-in-cell-custom {
  padding: 2px 4px;
  margin: 2px 0;
  border-radius: 3px;
  color: white; 
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: default; 
  font-weight: 500;
}

/* v-calendar deep styling adjustments */
:deep(.custom-calendar .vc-header) {
  padding: 8px 0; 
}
:deep(.custom-calendar .vc-title) {
  font-size: 1.2em; 
  font-weight: 600;
}

:deep(.custom-calendar .vc-weekday) {
  font-size: 0.85em; 
  padding-bottom: 5px;
  font-weight: 500;
  text-transform: uppercase;
}

:deep(.custom-calendar .vc-day) {
  min-height: 110px; /* Ensure day cells have a minimum height */
  /* height: auto; */ /* Auto height could also work depending on content */
  padding: 0 !important; /* Override default padding if using custom cell structure fully */
}

:deep(.custom-calendar .vc-day.is-today .vc-day-content) {
  /* Example: Make today's date number more prominent if not using full highlight */
  /* background-color: #e6f7ff; */
}

:deep(.custom-calendar .vc-day-content) {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style> 