<template>
    <div class="home-page">
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
              <img src="https://i.pravatar.cc/150?u=yuxiaohan_avatar" alt="于晓晗" class="profile-avatar-new">
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
          <h2>主要内容</h2>
          <div class="card-container">
            <div class="card">
              <h3>经历</h3>
              <p>这里将展示我的工作和学习经历。</p>
              <router-link to="/experience" class="card-link">了解更多 &rarr;</router-link>
            </div>
            <div class="card">
              <h3>项目</h3>
              <p>这里将展示我参与或独立完成的项目。</p>
              <router-link to="/projects" class="card-link">了解更多 &rarr;</router-link>
            </div>
            <div class="card">
              <h3>其他</h3>
              <p>这里可以放置一些其他的补充信息，例如博客、爱好等。</p>
              <router-link to="/message-wall" class="card-link">查看留言墙 &rarr;</router-link>
            </div>
          </div>
        </section>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePage'
  }
  </script>
  
  <style scoped>
  .home-page {
    max-width: 100%;
    margin: 0 auto;
    overflow-x: hidden;
  }
  
  .content-wrapper {
    width: 60%;
    margin: 0 auto;
    position: relative;
  }
  
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
    content: url('/yxh.jpg'); /* Changed image source */
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
    padding: 40px 20px; /* Added horizontal padding */
    max-width: 1200px; /* Constrain width of this section */
    margin: 0 auto; /* Center this section */
  }
  
  .content-cards-section h2 {
    text-align: center;
    margin-bottom: 30px;
    color: var(--text-headings) !important; /* Use variable, keep important if necessary */
  }
  
  .card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px; /* 卡片之间的间距 */
    justify-content: center;
  }
  
  .card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
    padding: 25px;
    width: calc(33.333% - 40px); /* 响应式调整，一行最多3个卡片 */
    min-width: 280px; /* 最小宽度 */
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
    .new-introduction-section {
      padding: 20px 10px; /* Reduce padding on small screens */
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
    /* margin-bottom: 10px; */ /* No longer needed as wrappers handle spacing */
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
  </style> 