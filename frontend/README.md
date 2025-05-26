# 个人网站前端 (Vue.js)

这是一个使用 Vue.js 构建的个人网站前端项目。

## 项目设置

确保您已安装 Node.js 和 npm/yarn。

1.  **安装依赖**

    ```bash
    npm install
    # 或者
    # yarn install
    ```

2.  **本地开发 (热重载)**

    ```bash
    npm run serve
    # 或者
    # yarn serve
    ```
    应用将在 `http://localhost:8080` (或类似端口) 上运行。

3.  **生产构建**

    ```bash
    npm run build
    # 或者
    # yarn build
    ```
    构建后的文件将位于 `dist` 目录中。

## 项目结构

-   `public/`: 静态资源和 `index.html` 模板。
-   `src/`: Vue.js 应用源代码。
    -   `assets/`: 样式文件、图片等资源。
    -   `components/`: Vue 组件。
    -   `App.vue`: 根 Vue 组件。
    -   `main.js`: Vue 应用入口。

## 设计说明

-   **配色方案**: 基于 `https://uicolors.app/generate/4590b5`。
-   **导航**: 右上角固定按钮，点击后从右侧滑出。
-   **内容**: 包含个人介绍和卡片式内容展示。 