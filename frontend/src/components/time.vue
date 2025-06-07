<template>
  <div class="timeline-page-container">
    <canvas id="particle-canvas-timeline"></canvas>
    <div class="actual-content-wrapper">
      <!-- Single visual block for all timeline related content -->
      <div class="timeline-single-box content-block">

        <!-- Header area for Title and Intro -->
        <div class="timeline-box-header">
          <h1 class="page-title">网站时间轴</h1>
          <p class="page-intro">关于搭建网站的时间轴</p>
        </div>

        <!-- Conditional Messages -->
        <div v-if="isLoading" class="loading-message status-message">
          <p>正在加载时间轴数据...</p>
          <div class="spinner"></div>
        </div>
        <div v-if="!isLoading && error" class="error-message status-message">
          <p>加载失败：{{ error }}</p>
          <button @click="fetchTimelineEvents" class="retry-button">重试</button>
        </div>
        <div v-if="!isLoading && !error && timelineEvents.length === 0" class="empty-message status-message">
          <p>目前还没有时间轴事件。</p>
        </div>

        <!-- Wrapper for actual timeline items and the blue line -->
        <div v-if="!isLoading && !error && timelineEvents.length > 0" class="timeline-items-wrapper">
          <div v-for="(event, index) in timelineEvents" :key="event.id || index" class="timeline-item">
            <div class="timeline-marker"></div>
            <div class="timeline-content">
              <div class="event-date">{{ formatDate(event.date) }}</div>
              <h3 class="event-title">{{ event.title }}</h3>
              <p class="event-details">{{ event.details }}</p>
              <div v-if="event.created_at" class="event-meta">
                记录于: {{ formatDateTime(event.created_at) }}
              </div>
            </div>
          </div>
        </div>
      </div> <!-- End of timeline-single-box -->
    </div> <!-- End of actual-content-wrapper -->
  </div>
</template>

<script>
export default {
  name: 'TimelinePage',
  data() {
    return {
      timelineEvents: [],
      isLoading: true,
      error: null,
    };
  },
  mounted() {
    console.log('TimelinePage: mounted() hook called');
    this.fetchTimelineEvents();
    this.initTimelineParticleCanvas();
  },
  beforeUnmount() {
    if (typeof this.cleanupResizeListener === 'function') {
      this.cleanupResizeListener();
    }
    if (typeof this.cancelAnimation === 'function') {
      this.cancelAnimation();
    }
  },
  methods: {
    async fetchTimelineEvents() {
      console.log('TimelinePage: fetchTimelineEvents() method called');
      this.isLoading = true;
      this.error = null;
      try {
        console.log('TimelinePage: BEFORE fetch call to /api/timeline-events/');
        const response = await fetch('/api/timeline-events/');
        console.log('TimelinePage: AFTER fetch call. Response object:', response);
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({ message: response.statusText }));
          throw new Error(`HTTP error ${response.status}: ${errorData.message || response.statusText}`);
        }
        const data = await response.json();
        this.timelineEvents = data;
      } catch (e) {
        console.error('获取时间轴数据失败:', e);
        this.error = e.message || '无法连接到服务器或解析数据失败。';
      } finally {
        this.isLoading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    formatDateTime(dateTimeString) {
      if (!dateTimeString) return '';
      const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateTimeString).toLocaleString(undefined, options);
    },
    initTimelineParticleCanvas() {
      const canvas = document.getElementById('particle-canvas-timeline');
      if (!canvas) {
        console.error("Canvas element 'particle-canvas-timeline' not found!");
        return;
      }
      const ctx = canvas.getContext('2d');
      if (!ctx) {
        console.error("Could not get 2D context from canvas!");
        return;
      }
      let particlesArray;

      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;

      const resizeHandler = () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        // eslint-disable-next-line no-use-before-define
        if (typeof init === 'function') {
          init();
        }
      };
      window.addEventListener('resize', resizeHandler);
      this.cleanupResizeListener = () => {
        window.removeEventListener('resize', resizeHandler);
      };

      class Particle {
        constructor(x, y, directionX, directionY, size, color) {
          this.x = x;
          this.y = y;
          this.directionX = directionX;
          this.directionY = directionY;
          this.size = size;
          this.color = color;
        }
        draw() {
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
          ctx.fillStyle = this.color;
          ctx.fill();
        }
        update() {
          if (this.x + this.size > canvas.width || this.x - this.size < 0) {
            this.directionX = -this.directionX;
          }
          if (this.y + this.size > canvas.height || this.y - this.size < 0) {
            this.directionY = -this.directionY;
          }
          this.x += this.directionX;
          this.y += this.directionY;
          this.draw();
        }
      }

      function init() {
        particlesArray = [];
        const numberOfParticles = (canvas.height * canvas.width) / 9000;
        for (let i = 0; i < numberOfParticles; i++) {
          const size = (Math.random() * 2) + 1;
          const x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
          const y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
          const directionX = (Math.random() * .3) - .15;
          const directionY = (Math.random() * .3) - .15;
          const color = 'rgba(180, 180, 180, 0.4)';
          particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
        }
      }

      let animationFrameId = null;
      function animate() {
        animationFrameId = requestAnimationFrame(animate);
        ctx.clearRect(0, 0, innerWidth, innerHeight);
        if (particlesArray && particlesArray.length) {
          for (let i = 0; i < particlesArray.length; i++) {
            particlesArray[i].update();
          }
          // eslint-disable-next-line no-use-before-define
          connect();
        }
      }
      this.cancelAnimation = () => {
        if (animationFrameId) {
          cancelAnimationFrame(animationFrameId);
        }
      };

      function connect() {
        let opacityValue = 1;
        for (let a = 0; a < particlesArray.length; a++) {
          for (let b = a; b < particlesArray.length; b++) {
            const distance = ((particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x))
                           + ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));
            if (distance < (canvas.width / 10) * (canvas.height / 10)) {
              opacityValue = 1 - (distance / 15000);
              ctx.strokeStyle = 'rgba(180, 180, 180,' + opacityValue * 0.3 + ')';
              ctx.lineWidth = 0.5;
              ctx.beginPath();
              ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
              ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
              ctx.stroke();
            }
          }
        }
      }
      init();
      animate();
    }
  },
};
</script>

<style scoped>
.timeline-page-container {
  width: 100vw;
  height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
}

#particle-canvas-timeline {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  background-color: #f0f0f0;
}

.actual-content-wrapper {
  position: relative;
  z-index: 2;
  padding-top: 80px; 
  padding-bottom: 20px;
  max-width: 900px;
  margin: 0 auto;
  color: var(--text-primary);
}

/* This is the single main box for title, intro, and timeline items */
.timeline-single-box.content-block {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.timeline-box-header {
  text-align: center;
  margin-bottom: 30px; /* Increased space before timeline items */
}

.page-title {
  color: var(--accent-color);
  font-size: 2.2em;
  margin-top: 0;
  margin-bottom: 10px;
}

.page-intro {
  font-size: 1.1em;
  color: var(--text-secondary);
  margin-top: 0;
  margin-bottom: 0;
}

/* Styling for status messages (loading, error, empty) so they look good inside the single box */
.status-message {
  text-align: center;
  padding: 20px 0;
}
.loading-message p, .empty-message p {
   margin-bottom: 15px;
}


/* Wrapper for the actual timeline items and its ::before line */
.timeline-items-wrapper {
  position: relative;
  padding-left: 40px;
}

.timeline-items-wrapper::before {
  content: '';
  position: absolute;
  left: 10px;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: var(--primary-200);
  border-radius: 2px;
}

/* .content-block common styling (only timeline-single-box uses it now) */
/* .page-header-block is removed */

/* Styles for .timeline, .loading-message, .error-message, .empty-message */
/* These elements might not need all their previous individual styling if they are simplified */
/* .timeline class is now on .timeline-single-box if events exist, or just used for structure */


.retry-button {
  padding: 10px 20px;
  margin-top: 15px;
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background-color: color-mix(in srgb, var(--accent-color) 80%, black);
}

.spinner {
  margin: 0 auto; /* Centered if p above is also centered */
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: var(--accent-color);
  animation: spin 1s ease infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.timeline-item {
  position: relative;
  margin-bottom: 25px; /* Space between bubbles */
}

.timeline-item:last-child {
  margin-bottom: 0;
}

.timeline-marker {
  position: absolute;
  left: -34.5px; 
  top: 18px; /* Adjust vertical alignment with the bubble's content */
  width: 12px;
  height: 12px;
  background-color: var(--accent-color);
  border: 3px solid #f0f0f0; /* Border color to match particle canvas background */
  border-radius: 50%;
  z-index: 2; /* Ensure marker is above the line but can be under a lifted bubble if overlap */
}

.timeline-content {
  background-color: white;
  border-radius: 10px; /* Rounded corners for the bubble */
  box-shadow: 0 3px 6px rgba(0,0,0,0.08); /* Initial softer shadow */
  padding: 20px 25px; /* Padding inside the bubble */
  margin-left: 10px; /* Create some space from the marker/line area */
  position: relative; /* For z-index stacking if needed */
  z-index: 1; /* Base z-index */
  transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
  /* Resetting some potentially inherited styles */
  border: none; 
}

.timeline-content:hover {
  transform: translateY(-6px); /* Lift effect */
  box-shadow: 0 8px 16px rgba(0,0,0,0.12); /* Enhanced shadow on hover */
  z-index: 3; /* Ensure hovered item is on top */
}

.event-date {
  font-size: 0.85em; /* Slightly smaller */
  color: var(--text-secondary);
  margin-bottom: 8px;
  font-weight: 600; /* Bolder */
}

.event-title {
  font-size: 1.3em; /* Adjusted size */
  margin-top: 0;
  margin-bottom: 10px;
  color: var(--text-primary-strong);
}

.event-details {
  font-size: 0.95em; /* Adjusted size */
  line-height: 1.6;
  color: var(--text-primary);
  margin-bottom: 12px;
  white-space: pre-wrap;
}

.event-meta {
  font-size: 0.8em;
  color: var(--text-tertiary);
  text-align: right;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .actual-content-wrapper {
    padding-top: 70px;
    max-width: 100%;
    /* margin: 0 10px; */ /* Let content-block handle its own margins/padding on small screens if needed */
    /* padding-left: 15px; */
    /* padding-right: 15px; */
  }
  .timeline-single-box.content-block {
    margin: 0 10px; /* Add horizontal margin for the main box on small screens */
    padding: 15px;
  }
  .page-title {
    font-size: 1.8em;
  }
  .timeline-items-wrapper {
    padding-left: 30px; /* Less padding for line on smaller screens */
  }
  .timeline-items-wrapper::before {
    left: 5px; /* Adjust line position */
  }
  .timeline-marker {
     /* Recalculate for new padding and line pos: 5px (line_left) + 1.5px (half_line) - 5px (half_marker_10px) = 1.5px from wrapper left */
     /* 1.5px - 30px (wrapper_padding_left) = -28.5px */
    left: -28.5px; /* Adjust marker position */
    top: 15px; /* Adjust for smaller text */
    width: 10px;
    height: 10px;
    border-width: 2px; /* Thinner border for smaller marker */
  }
  .timeline-content {
    /* margin-left: 5px; */ /* Not needed */
    padding: 15px 20px;
    margin-left: 5px; /* Less margin on small screens */
  }
  .event-title {
    font-size: 1.2em;
  }
  .event-details {
    font-size: 0.9em;
  }
}
</style> 