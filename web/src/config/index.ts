const baseConfig = {  
    apiBaseUrl: 'http://localhost:8000', // 服务器地址+端口
    timeout: 5000, // 请求超时时间（毫秒）
    enableDebug: true // 调试模式开关
  };
  const config = { ...baseConfig };
  export default config;