import React from 'react';
  const baseConfig = {  
    apiBaseUrl: 'http://localhost:8000', // 服务器地址+端口
    timeout: 5000, // 请求超时时间（毫秒）
    enableDebug: true // 调试模式开关
  };
  const menu_data = 
    {
      '系统管理-用户管理': React.lazy(() => import('../modules/system-manage/UserManagement')),
      '系统管理-角色管理': React.lazy(() => import('../modules/system-manage/RoleManagement')),
    };
  const config = { ...baseConfig, menu_data };
  export default config;