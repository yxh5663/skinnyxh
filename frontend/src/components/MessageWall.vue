<template>
  <div class="message-wall-page">
    <div class="background-image-container">
      <!-- 背景图片通过 CSS 设置 -->
    </div>

    <div class="message-canvas">
      <div 
        v-for="(message, index) in messages" 
        :key="message.id" 
        class="message-bubble-wrapper" 
        :style="getMessageStyle(message)"
        :ref="el => { if (el) bubbleRefs[index] = el }"
      >
        <div class="message-bubble">
          <p class="message-text">{{ message.text }}</p>
          <span class="message-timestamp">{{ formatTimestamp(message.timestamp) }}</span>
        </div>
      </div>
    </div>

    <div class="message-input-container">
      <textarea v-model="newMessage" placeholder="留下点什么吧..."></textarea>
      <button @click="postMessage">发送</button>
    </div>
  </div>
</template>

<script>
// 假设你有一个AppHeader组件，如果不是，请告诉我正确的组件或移除它
// import AppHeader from './AppHeader.vue'; 

export default {
  name: 'MessageWall',
  // components: { AppHeader },
  data() {
    return {
      newMessage: '',
      messages: [],
      animationFrameId: null,
      canvasDimensions: { width: 0, height: 0 },
      bubbleRefs: [] // 用于存储对气泡 DOM 元素的引用
    };
  },
  mounted() {
    console.log('MessageWall component MOUNTED');
    // fetchMessages 会在其成功回调中调用 initializeMessageMotion 和 startAnimation
    this.fetchMessages();
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    this.stopAnimation();
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleResize() {
        const canvas = this.$el.querySelector('.message-canvas');
        if (canvas) {
            this.canvasDimensions.width = canvas.clientWidth;
            this.canvasDimensions.height = canvas.clientHeight;
        }
        // 可选择重新初始化位置或仅更新边界
    },
    async fetchMessages() {
      console.log('Fetching messages from backend...');
      try {
        const response = await fetch('http://localhost:8000/api/messages/');
        if (!response.ok) throw new Error('Failed to fetch messages');
        const fetchedMessages = await response.json();
        console.log('Fetched messages:', JSON.parse(JSON.stringify(fetchedMessages)));
        this.messages = fetchedMessages.map(msg => ({ ...msg, motionProps: null })); // 重置 motionProps
        
        this.$nextTick(async () => { // 等待 DOM 渲染完成
            const canvas = this.$el.querySelector('.message-canvas');
            if (canvas) {
                this.canvasDimensions.width = canvas.clientWidth;
                this.canvasDimensions.height = canvas.clientHeight;
            }
            await this.initializeMessageMotion(); // 改为异步以等待 refs 更新
            this.startAnimation(); 
        });
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    },
    async postMessage() {
      if (!this.newMessage.trim()) {
        alert('内容不能为空哦！');
        return;
      }
      const messageData = { text: this.newMessage };
      try {
        const response = await fetch('http://localhost:8000/api/messages/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(messageData)
        });
        if (!response.ok) {
          let errorData = { message: 'Failed to post message' };
          try { errorData = await response.json(); } catch (e) { /* 忽略 */ }
          throw new Error(errorData.detail || errorData.message || 'Failed to post message');
        }
        const savedMessage = await response.json();
        const newMessage = { ...savedMessage, motionProps: null };
        this.messages.push(newMessage);

        this.$nextTick(async () => { // 等待新气泡的 DOM 元素创建
            await this.initializeMessageMotion([newMessage]); // 只为新消息初始化运动和尺寸
            // 如果动画已停止，可以考虑重启，或者 animateBubbles 会自然处理新元素
        });
        this.newMessage = ''; 
      } catch (error) {
        console.error('Error posting message:', error);
        alert(`发送失败: ${error.message}`);
      }
    },
    formatTimestamp(timestamp) {
      if (!timestamp) return '';
      const date = new Date(timestamp);
      return date.toLocaleString('zh-CN', { hour: '2-digit', minute: '2-digit' }); // 简化时间戳显示
    },
    async initializeMessageMotion(messagesToUpdate) {
      // 等待 bubbleRefs 被 Vue 更新
      await this.$nextTick(); 

      const messages = messagesToUpdate || this.messages;
      const canvasWidth = this.canvasDimensions.width;
      const canvasHeight = this.canvasDimensions.height;

      messages.forEach((msg, indexInProcessedArray) => {
        // 如果是 전체 messages 数组，则 indexInProcessedArray 就是它在 this.messages 中的索引
        // 如果是 messagesToUpdate (单元素数组), 我们需要找到它在 this.messages 中的原始索引来匹配 ref
        const originalIndex = messagesToUpdate ? this.messages.findIndex(m => m.id === msg.id) : indexInProcessedArray;
        const bubbleElement = this.bubbleRefs[originalIndex];

        let bubbleWidth = 200; // Default/fallback
        let bubbleHeight = 80; // Default/fallback

        if (bubbleElement) {
          bubbleWidth = bubbleElement.offsetWidth;
          bubbleHeight = bubbleElement.offsetHeight;
          console.log(`Bubble ${msg.id} dimensions: W=${bubbleWidth}, H=${bubbleHeight}`);
        } else {
          console.warn(`Bubble element for message ID ${msg.id} not found in refs.`);
        }

        if (!msg.motionProps) { // 只有在 motionProps 不存在时才初始化
          msg.motionProps = {
            x: Math.random() * Math.max(0, canvasWidth - bubbleWidth),
            y: Math.random() * Math.max(0, canvasHeight - bubbleHeight),
            vx: (Math.random() - 0.5) * 0.4, 
            vy: (Math.random() - 0.5) * 0.4, 
            width: bubbleWidth,
            height: bubbleHeight,
            element: bubbleElement // 可以缓存 element 引用，但注意 Vue 的虚拟 DOM 更新
          };
        } else { // 如果 motionProps 已存在 (例如窗口 resize 后重新计算)，只更新尺寸和边界相关的
          msg.motionProps.width = bubbleWidth;
          msg.motionProps.height = bubbleHeight;
          // 可以选择是否重新随机化位置，或根据新尺寸调整现有位置以防出界
          msg.motionProps.x = Math.min(msg.motionProps.x, Math.max(0, canvasWidth - bubbleWidth));
          msg.motionProps.y = Math.min(msg.motionProps.y, Math.max(0, canvasHeight - bubbleHeight));
        }
      });
      if (!messagesToUpdate) {
        this.messages = [...this.messages]; 
      }
    },
    getMessageStyle(message) {
      if (!message.motionProps) {
        return { position: 'absolute', opacity: 0 }; // 初始隐藏，等待 JS 定位
      }
      return {
        position: 'absolute',
        transform: `translate(${message.motionProps.x}px, ${message.motionProps.y}px)`,
        opacity: 1 // JS 定位后可见
      };
    },
    startAnimation() {
      if (!this.animationFrameId) {
        this.animateBubbles();
      }
    },
    stopAnimation() {
      if (this.animationFrameId) {
        cancelAnimationFrame(this.animationFrameId);
        this.animationFrameId = null;
      }
    },
    animateBubbles() {
      this.messages.forEach((msg, i) => { // 获取当前气泡的索引 i
        if (!msg.motionProps) return;

        let { x, y, vx, vy, width, height } = msg.motionProps;

        x += vx;
        y += vy;

        // 边界检测
        if (x < 0 || x + width > this.canvasDimensions.width) {
          vx = -vx;
          x = Math.max(0, Math.min(x, this.canvasDimensions.width - width));
        }
        if (y < 0 || y + height > this.canvasDimensions.height) {
          vy = -vy;
          y = Math.max(0, Math.min(y, this.canvasDimensions.height - height));
        }
        
        // 碰撞检测 (AABB)
        for (let j = i + 1; j < this.messages.length; j++) {
          const otherMsg = this.messages[j];
          if (!otherMsg.motionProps) continue;

          const other = otherMsg.motionProps;

          // AABB collision detection
          if (x < other.x + other.width &&
              x + width > other.x &&
              y < other.y + other.height &&
              y + height > other.y) {
            
            // Collision detected
            // Simple response: reverse velocity for both
            vx = -vx;
            vy = -vy;
            other.vx = -other.vx;
            other.vy = -other.vy;

            // Resolve overlap: Move bubbles apart along the axis of least penetration (simplified)
            // This is a very basic overlap resolution and can be jittery.
            // More sophisticated resolution would involve calculating penetration depth for X and Y
            // and moving them along the axis with the minimum penetration.
            
            let overlapX = 0;
            if (vx > 0) { // Current bubble moving right, collided with left side of other
                overlapX = (x + width) - other.x;
            } else if (vx < 0) { // Current bubble moving left, collided with right side of other
                overlapX = (other.x + other.width) - x;
            }

            let overlapY = 0;
            if (vy > 0) { // Current bubble moving down, collided with top side of other
                overlapY = (y + height) - other.y;
            } else if (vy < 0) { // Current bubble moving up, collided with bottom side of other
                overlapY = (other.y + other.height) - y;
            }

            // Simple push apart - can be improved
            if (Math.abs(overlapX) < Math.abs(overlapY) && overlapX !== 0) { // Push horizontally
                const push = overlapX / 2;
                x -= push;
                other.x += push;
            } else if (overlapY !== 0) { // Push vertically
                const push = overlapY / 2;
                y -= push;
                other.y += push;
            }
          }
        }

        msg.motionProps.x = x;
        msg.motionProps.y = y;
        msg.motionProps.vx = vx;
        msg.motionProps.vy = vy;
      });
      this.animationFrameId = requestAnimationFrame(this.animateBubbles);
    }
  }
};
</script>

<style scoped>
.message-wall-page {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center; /* 水平居中输入框等 */
  justify-content: flex-end; /* 将输入框推到底部 */
  background-color: #f0f0f0; /* 页面背景色，防止背景图加载失败时一片空白 */
}

.background-image-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/sky.jpg'); /* 您的背景图 */
  background-size: cover;
  background-position: center;
  z-index: 0;
}

.message-canvas {
  position: absolute; /* 或者 relative，取决于整体布局需求 */
  top: 0;
  left: 0;
  width: 100%;
  height: calc(100% - 100px); /* 假设输入框区域高度约为100px，给输入框留出空间 */
  overflow: hidden; /* 防止气泡移出画布时产生滚动条 */
  z-index: 1;
}

.message-bubble-wrapper {
  /* position: absolute; is now set by getMessageStyle */
  will-change: transform;
  opacity: 0; /* Initially hidden, shown by getMessageStyle after JS positioning */
}

.message-bubble {
  background-color: rgba(255, 255, 255, 0.9);
  color: #333;
  padding: 12px 18px;
  border-radius: 25px;
  max-width: 250px; /* 气泡最大宽度 */
  min-width: 50px;  /* 气泡最小宽度 */
  box-shadow: 0 5px 15px rgba(0,0,0,0.15);
  word-wrap: break-word;
  transition: transform 0.3s ease;
  font-size: 0.9rem;
}

.message-bubble:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.message-text {
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.message-timestamp {
  font-size: 0.7rem;
  color: #888;
  display: block;
  text-align: right;
}

.message-input-container {
  /* position: relative;  改为 fixed 或 absolute 相对于 page */
  position: fixed; /* 固定在视口底部 */
  bottom: 20px; /* 距离底部20px */
  left: 50%;
  transform: translateX(-50%); /* 水平居中 */
  width: 90%;
  max-width: 600px; /* 最大宽度 */
  padding: 15px;
  background-color: rgba(0, 0, 0, 0.6);
  border-radius: 25px; /* 更圆润 */
  display: flex;
  align-items: center; /* 新增：使内部元素垂直居中 */
  gap: 10px;
  z-index: 100; /* 确保在最上层 */
  box-sizing: border-box;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
}

.message-input-container textarea {
  flex-grow: 1;
  min-height: 48px;
  max-height: 120px;
  padding: 12px 15px;
  border-radius: 20px;
  border: none;
  background-color: rgba(255, 255, 255, 0.95);
  color: #333;
  font-size: 0.95rem;
  resize: none;
}

.message-input-container button {
  padding: 0 25px;
  height: 48px;
  border-radius: 20px;
  background-color: #007bff; /* Bootstrap primary blue */
  color: white;
  border: none;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: bold;
  transition: background-color 0.2s ease;
}

.message-input-container button:hover {
  background-color: #0056b3;
}
</style> 