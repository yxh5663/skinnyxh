const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: config => {
    config.plugin('define').tap(definitions => {
      Object.assign(definitions[0], {
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'true'
      });
      return definitions;
    });
  },
  devServer: {
    proxy: {
      '/api': { // 所有以 /api 开头的请求都会被代理
        target: 'http://localhost:8000', // 你的 Django 后端地址
        changeOrigin: true, // 改变请求头中的 Origin 字段
        // pathRewrite: { '^/api': '' }, // 如果后端API路径不包含/api前缀，则此行取消注释
      },
      '/admin': { // 新增对 /admin 路径的代理
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
}); 