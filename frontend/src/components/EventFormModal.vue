<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <h3>{{ editingEvent ? '编辑事件' : '添加新事件' }}</h3>
      <form @submit.prevent="submitEvent">
        <div class="form-group">
          <label for="event-title">标题:</label>
          <input type="text" id="event-title" v-model="form.title" required>
        </div>

        <div class="form-group">
          <label for="event-description">描述:</label>
          <textarea id="event-description" v-model="form.description"></textarea>
        </div>

        <div class="form-group">
          <label for="event-type">类型:</label>
          <select id="event-type" v-model="form.event_type">
            <option value="memo">备忘</option>
            <option value="log">日志</option>
            <option value="holiday">节日</option>
            <option value="other">其他</option>
          </select>
        </div>
        
        <div class="form-group form-group-inline">
          <label for="event-is-all-day">全天事件:</label>
          <input type="checkbox" id="event-is-all-day" v-model="form.is_all_day">
        </div>

        <div class="form-group form-group-inline">
          <label for="event-is-completed">已完成:</label>
          <input type="checkbox" id="event-is-completed" v-model="form.is_completed">
        </div>

        <div v-if="!form.is_all_day">
          <div class="form-group">
            <label for="event-start-time">开始时间:</label>
            <input type="time" id="event-start-time" v-model="form.startTimeStr">
          </div>
          <div class="form-group">
            <label for="event-end-time">结束时间:</label>
            <input type="time" id="event-end-time" v-model="form.endTimeStr">
          </div>
        </div>
        
        <p v-if="selectedDate" class="selected-date-info">
          日期: {{ new Date(selectedDate).toLocaleDateString() }}
        </p>
        
        <!-- TODO: Add date range selection for global add button -->

        <div class="form-actions">
          <button type="submit" class="btn-save">保存</button>
          <button type="button" @click="closeModal" class="btn-cancel">取消</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EventFormModal',
  props: {
    selectedDate: { // YYYY-MM-DD string or Date object for pre-filling
      type: [String, Date],
      default: null
    },
    eventToEdit: { // Pass an event object to pre-fill form for editing
      type: Object,
      default: null
    }
  },
  data() {
    return {
      form: {
        title: '',
        description: '',
        event_type: 'memo',
        is_all_day: true,
        is_completed: false,
        startTimeStr: '09:00', // Default start time if not all-day
        endTimeStr: '17:00',   // Default end time if not all-day
        // For multi-day events (later)
        // startDate: null, 
        // endDate: null,   
      },
      editingEvent: null, // Store the original event if in edit mode
    };
  },
  watch: {
    eventToEdit: {
      handler(newEvent) {
        if (newEvent) {
          this.editingEvent = newEvent;
          this.form.title = newEvent.title || '';
          this.form.description = newEvent.description || '';
          this.form.event_type = newEvent.event_type || 'memo';
          this.form.is_all_day = newEvent.is_all_day || false;
          this.form.is_completed = newEvent.is_completed || false;
          
          if (newEvent.start_time) {
            const startDate = new Date(newEvent.start_time);
            this.form.startTimeStr = `${String(startDate.getHours()).padStart(2, '0')}:${String(startDate.getMinutes()).padStart(2, '0')}`;
          } else {
             this.form.startTimeStr = '09:00';
          }

          if (newEvent.end_time) {
            const endDate = new Date(newEvent.end_time);
            this.form.endTimeStr = `${String(endDate.getHours()).padStart(2, '0')}:${String(endDate.getMinutes()).padStart(2, '0')}`;
          } else {
            // If no end_time, but start_time exists, maybe set a default duration or leave as is
            this.form.endTimeStr = this.form.startTimeStr // Or some logic for default duration
          }
        } else {
          this.resetForm();
          this.editingEvent = null;
        }
      },
      immediate: true // Run watcher when component is created
    }
  },
  methods: {
    resetForm() {
        this.form.title = '';
        this.form.description = '';
        this.form.event_type = 'memo';
        this.form.is_all_day = true;
        this.form.is_completed = false;
        this.form.startTimeStr = '09:00';
        this.form.endTimeStr = '17:00';
    },
    closeModal() {
      this.resetForm();
      this.$emit('close');
    },
    submitEvent() {
      const eventData = { ...this.form };
      let eventDate = this.selectedDate ? new Date(this.selectedDate) : new Date(); // Fallback to today if no date selected

      if (this.editingEvent && this.editingEvent.start_time) {
          // If editing, preserve the original date part from start_time if only time is changed
          eventDate = new Date(this.editingEvent.start_time);
      }
      
      // Construct start_time and end_time
      if (eventData.is_all_day) {
        eventData.start_time = new Date(eventDate.getFullYear(), eventDate.getMonth(), eventDate.getDate(), 0, 0, 0).toISOString();
        // For all-day, end_time could be null or end of day. API should handle this.
        // Let's set it to end of the selected day for clarity, or null if API prefers
        eventData.end_time = new Date(eventDate.getFullYear(), eventDate.getMonth(), eventDate.getDate(), 23, 59, 59, 999).toISOString();
      } else {
        const [startHours, startMinutes] = eventData.startTimeStr.split(':').map(Number);
        eventData.start_time = new Date(eventDate.getFullYear(), eventDate.getMonth(), eventDate.getDate(), startHours, startMinutes, 0).toISOString();

        if (eventData.endTimeStr) {
          const [endHours, endMinutes] = eventData.endTimeStr.split(':').map(Number);
          const endDateForEndTime = new Date(eventDate.getFullYear(), eventDate.getMonth(), eventDate.getDate(), endHours, endMinutes, 0);
          // Handle if end time is on the next day (e.g. 10 PM to 2 AM) - for future enhancement
          eventData.end_time = endDateForEndTime.toISOString();
        } else {
          eventData.end_time = null; // Or set to start_time if it's an event with no duration
        }
      }
      
      delete eventData.startTimeStr;
      delete eventData.endTimeStr;

      if (this.editingEvent && this.editingEvent.id) {
        eventData.id = this.editingEvent.id; // Add id if editing
      }

      this.$emit('save', eventData);
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
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.form-group input[type="text"],
.form-group textarea,
.form-group select,
.form-group input[type="time"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 1em;
}

.form-group textarea {
  min-height: 80px;
  resize: vertical;
}

.form-group-inline {
  display: flex;
  align-items: center;
}
.form-group-inline label {
  margin-bottom: 0;
  margin-right: 10px;
}
.form-group-inline input[type="checkbox"] {
  width: auto;
  height: 1.2em; /* Adjust for better visual alignment */
  width: 1.2em;
}

.selected-date-info {
  margin-top: 15px;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f0f8ff;
  border: 1px solid #d1e9ff;
  border-radius: 4px;
  font-size: 0.9em;
  color: #31708f;
}


.form-actions {
  margin-top: 25px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-save, .btn-cancel {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
  font-weight: bold;
}

.btn-save {
  background-color: var(--primary-600, #3B82F6);
  color: white;
}
.btn-save:hover {
  background-color: var(--primary-700, #2563EB);
}

.btn-cancel {
  background-color: #f0f0f0;
  color: #333;
}
.btn-cancel:hover {
  background-color: #e0e0e0;
}
</style> 