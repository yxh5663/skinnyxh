<template>
  <div class="dynamic-page-container">
    <canvas id="particle-canvas"></canvas>
    <div class="main-content">
      <!-- Pinterest-like masonry grid -->
      <div class="masonry-grid">
        <div class="masonry-item" v-for="item in items" :key="item.id" :style="{height: item.height}">
          <h3>{{ item.title }}</h3>
          <p>{{ item.content }}</p>
          <p><em>卡片高度: {{ item.height }}</em></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExperiencePage',
  data() {
    return {
      items: [] // 卡片数据
    };
  },
  mounted() {
    this.initParticleCanvas();
    this.generateMasonryItems(); // 生成示例卡片数据
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
    generateMasonryItems() {
      const sampleItems = [];
      const numItems = 15; // 生成15个卡片
      for (let i = 0; i < numItems; i++) {
        sampleItems.push({
          id: i,
          title: `卡片 ${i + 1}`,
          content: '这里是一些示例内容，用于填充卡片。卡片的内容长度可以不同，从而产生不同的高度。Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
          height: `${Math.floor(Math.random() * 200) + 150}px` // 随机高度 150px 到 350px
        });
      }
      this.items = sampleItems;
    },
    initParticleCanvas() {
      const canvas = document.getElementById('particle-canvas');
      if (!canvas) {
        console.error("Canvas element not found!");
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
          const size = (Math.random() * 2) + 1; // 粒子更小一点
          const x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
          const y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
          const directionX = (Math.random() * .3) - .15; // 移动慢一点
          const directionY = (Math.random() * .3) - .15;
          const color = 'rgba(180, 180, 180, 0.4)'; // 粒子颜色浅一点
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
            if (distance < (canvas.width / 10) * (canvas.height / 10)) { // 调整连接距离
              opacityValue = 1 - (distance / 15000); // 调整透明度计算
              ctx.strokeStyle = 'rgba(180, 180, 180,' + opacityValue * 0.3 + ')'; // 线条更浅
              ctx.lineWidth = 0.5; // 线条更细
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
  }
};
</script>

<style scoped>
.dynamic-page-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow-y: auto; /* 允许主容器在内容过多时滚动 */
  overflow-x: hidden;
}

#particle-canvas {
  position: fixed; /* 让canvas固定，不随滚动条滚动 */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  background-color: #f0f0f0;
}

.main-content {
  position: relative;
  z-index: 2;
  width: 70%; /* 修改宽度 */
  max-width: 1200px; /* 修改最大宽度 */
  min-height: 80vh; 
  padding-top: 10vh; /* 使用padding-top来确保背景可见 */
  padding-bottom: 5vh;
  margin-left: auto;
  margin-right: auto;
  /* background-color: white; /* 暂时移除背景色，让masonry-grid的背景色生效 */
  /* box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); */ /* 暂时移除阴影 */
  /* border-radius: 8px; */ /* 暂时移除圆角 */
  /* padding: 20px; */ /* 暂时移除内边距，由masonry-grid控制 */
}

.masonry-grid {
  column-count: 3; /* 三列布局 */
  column-gap: 1em; /* 列间距 */
  background-color: white; /* 白色背景块 */
  padding: 20px; /* 内部留白 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.masonry-item {
  background-color: #f9f9f9; /* 卡片背景色 */
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 1em; /* 卡片底部外边距 */
  break-inside: avoid-column; /* 防止卡片内容在列中断裂 */
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  overflow: hidden; /* 确保内容不会溢出卡片 */
}

.masonry-item h3 {
  margin-top: 0;
  font-size: 1.2em;
}
</style> 