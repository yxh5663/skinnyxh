<template>
  <div class="modal-overlay" @click.self="closeMe">
    <div class="modal-content day-detail-modal">
      <h3>{{ formattedSelectedDate }}</h3>

      <div v-if="eventsForDay && eventsForDay.length > 0" class="event-list">
        <h4>当天事件:</h4>
        <ul>
          <li v-for="event in eventsForDay" :key="event.id" class="event-item">
            <div class="event-info">
              <div class="event-header">
                <!-- Completion Checkbox/Indicator -->
                <input 
                  type="checkbox" 
                  :checked="event.is_completed" 
                  @change="toggleComplete(event)" 
                  :disabled="!canEditEvents"
                  class="completion-checkbox"
                  title="标记为已完成/未完成"
                  v-if="canEditEvents"
                />
                <span 
                  v-if="!canEditEvents && event.is_completed" 
                  class="completion-indicator completion-indicator-done"
                  title="已完成"
                >✓</span>
                <span 
                  v-if="!canEditEvents && !event.is_completed" 
                  class="completion-indicator completion-indicator-pending"
                  title="未完成"
                >☐</span>

                <span class="event-time">{{ formatEventTime(event) }}</span>
                <span class="event-title" :class="{ 'completed-event': event.is_completed }">{{ event.title }}</span> 
                <span class="event-type-badge" :style="{ backgroundColor: eventTypeColors[event.event_type] || eventTypeColors['other'] }">
                  {{ event.event_type }}
                </span>
              </div>
              <p v-if="event.description" class="event-description" :class="{ 'completed-event': event.is_completed }">{{ event.description }}</p>
            </div>
            <div class="event-actions" v-if="canEditEvents">
              <button @click="requestEdit(event)" class="btn-edit-event">编辑</button>
              <button @click="requestDelete(event.id)" class="btn-delete-event">删除</button>
            </div>
          </li>
        </ul>
      </div>
      <div v-else class="no-events-message">
        <p>当天没有事件。</p>
      </div>

      <div class="modal-actions">
        <button v-if="canEditEvents" @click="requestAdd" class="btn-add-for-day">为此日期添加事件</button>
        <div v-else class="action-placeholder"></div>
        <button @click="closeMe" class="btn-close-detail">关闭</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DayDetailModal',
  props: {
    selectedDate: { // Date object
      type: Date,
      required: true
    },
    eventsForDay: {
      type: Array,
      default: () => []
    },
    eventTypeColors: { // Pass this from parent for consistency
        type: Object,
        default: () => ({
            holiday: 'red',
            memo: 'purple',
            log: 'green',
            other: 'gray',
        })
    },
    canEditEvents: { // New prop to control edit/delete/add visibility
        type: Boolean,
        default: false
    }
  },
  computed: {
    formattedSelectedDate() {
      if (!this.selectedDate) return '';
      return this.selectedDate.toLocaleDateString('zh-CN', { 
        year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' 
      });
    }
  },
  mounted() {
    // console.log('[DayDetailModal mounted] canEditEvents prop:', this.canEditEvents);
    // console.log('[DayDetailModal mounted] selectedDate:', this.selectedDate);
  },
  updated() {
    // console.log('[DayDetailModal updated] canEditEvents prop:', this.canEditEvents);
  },
  methods: {
    closeMe() {
      this.$emit('close');
    },
    requestAdd() {
      if (!this.canEditEvents) return;
      this.$emit('request-add-event');
    },
    requestEdit(event) {
      if (!this.canEditEvents) return;
      this.$emit('request-edit-event', event);
    },
    requestDelete(eventId) {
      if (!this.canEditEvents) return;
      if (confirm('确定要删除这个事件吗？')) {
        this.$emit('request-delete-event', eventId);
      }
    },
    toggleComplete(event) {
      if (!this.canEditEvents) return;
      const updatedEventPayload = {
        id: event.id,
        is_completed: !event.is_completed // 发送切换后的状态
      };
      this.$emit('request-toggle-complete', updatedEventPayload);
    },
    formatEventTime(event) {
      if (event.is_all_day) {
        return '全天';
      }
      const startTime = new Date(event.start_time).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', hour12: false });
      let timeRange = startTime;
      if (event.end_time) {
        const endTime = new Date(event.end_time).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', hour12: false });
        // Only show end time if it's different from start time (useful for short events not spanning midnight)
        if (endTime !== startTime) {
            timeRange += ` - ${endTime}`;
        }
      }
      return timeRange;
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050; /* Higher than event form modal if they can overlap, though unlikely with current flow */
}

.day-detail-modal {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  width: 90%;
  max-width: 550px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
}

.day-detail-modal h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: var(--primary-700, #1D4ED8);
  text-align: center;
  font-size: 1.4em;
}

.event-list {
  margin-bottom: 20px;
  flex-grow: 1;
  overflow-y: auto; /* Allows scrolling for many events */
}

.event-list h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  font-size: 1.1em;
  border-bottom: 1px solid #eee;
  padding-bottom: 5px;
}

.event-list ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.event-item {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.event-item:last-child {
  border-bottom: none;
}

.event-info {
  flex-grow: 1;
  margin-right: 10px; /* Space before action buttons */
}

.event-header {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
}

.completion-checkbox {
  margin-right: 8px;
  width: 16px;
  height: 16px;
  flex-shrink: 0; /* 防止复选框被压缩 */
  cursor: pointer;
}
.completion-checkbox:disabled {
  cursor: not-allowed;
}

.completion-indicator {
  margin-right: 8px;
  font-size: 1.1em; /* 调整大小以匹配复选框的视觉效果 */
  width: 16px; /* 给予宽度以对齐 */
  display: inline-block;
  text-align: center;
  flex-shrink: 0;
}
.completion-indicator-done {
  color: green;
}
/* .completion-indicator-pending can use default text color or be styled */

.event-time {
  font-weight: bold;
  color: #555;
  display: block;
  font-size: 0.9em;
  margin-bottom: 4px;
}

.event-title {
  font-size: 1.1em;
  color: #333;
  font-weight: 500;
  margin-bottom: 3px; /* 调整，因为现在在 flex 容器中 */
  margin-right: 8px; /* 与类型徽章的间距 */
}

.event-title.completed-event {
  text-decoration: line-through;
  color: #888; /* 更柔和的颜色表示已完成 */
}

.event-type-badge {
  display: inline-block;
  padding: 2px 8px;
  font-size: 0.75em;
  border-radius: 10px;
  color: white;
  margin-left: 8px;
  vertical-align: middle;
}

.event-description {
  font-size: 0.9em;
  color: #666;
  margin-top: 5px;
  white-space: pre-wrap; /* Preserve line breaks in description */
}

.event-description.completed-event {
  text-decoration: line-through;
  color: #888; /* 更柔和的颜色表示已完成 */
}

.event-actions {
  display: flex;
  flex-direction: column; /* Stack edit and delete buttons */
  gap: 8px; /* Space between edit and delete buttons */
  align-items: flex-end; /* Align buttons to the right */
}

.btn-edit-event, .btn-delete-event {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85em;
  font-weight: 500;
  min-width: 60px; /* Ensure buttons have some minimum width */
  text-align: center;
}

.btn-edit-event {
  background-color: var(--info-500, #3B82F6);
  color: white;
}
.btn-edit-event:hover {
  background-color: var(--info-600, #2563EB);
}

.btn-delete-event {
  background-color: var(--danger-500, #EF4444);
  color: white;
}
.btn-delete-event:hover {
  background-color: var(--danger-600, #DC2626);
}

.no-events-message {
  text-align: center;
  color: #777;
  padding: 20px;
  font-style: italic;
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: space-between; /* Align buttons to opposite ends */
  gap: 10px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.btn-add-for-day, .btn-close-detail {
  padding: 10px 18px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.95em;
  font-weight: 500;
}

.btn-add-for-day {
  background-color: var(--primary-600, #3B82F6);
  color: white;
}
.btn-add-for-day:hover {
  background-color: var(--primary-700, #2563EB);
}

.action-placeholder {
    min-width: 150px; /* Adjust based on your add button's typical width */
}

.btn-close-detail {
  background-color: #6c757d; /* A neutral gray */
  color: white;
}
.btn-close-detail:hover {
  background-color: #5a6268;
}
</style> 