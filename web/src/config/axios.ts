import axios from 'axios';
import config from './index'; // 假设config已导出apiBaseUrl

// 创建自定义Axios实例
const apiAxios = axios.create({ 
  baseURL: config.apiBaseUrl, // 自动添加公共地址头
  timeout: 5000 // 可选：设置超时时间
});

// // 可选：添加请求/响应拦截器（如处理Token）
// apiAxios.interceptors.request.use((config) => {
//   // 例如：添加Authorization头
//   const token = localStorage.getItem('token');
//   if (token) config.headers.Authorization = `Bearer ${token}`;
//   return config;
// });

export default apiAxios;