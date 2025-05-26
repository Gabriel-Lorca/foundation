import React from 'react';
import SidebarMenu from '../components/SidebarMenu';

/**
 * 仪表盘页面组件
 * 采用网格布局，分为四个区域：
 * 1. 顶部左侧：LOGO区域
 * 2. 顶部右侧：模块名称
 * 3. 左侧：侧边栏菜单
 * 4. 右侧：数据展示和业务操作区域
 */
const DashboardPage: React.FC = () => {
  const [currentModule, setCurrentModule] = React.useState('');
  

  const moduleComponentMap: Record<string, React.LazyExoticComponent<React.ComponentType>> = {
    '系统管理-用户管理': React.lazy(() => import('../modules/UserManagement')),
    '系统管理-角色管理': React.lazy(() => import('../modules/RoleManagement')),
    '系统管理-模块管理': React.lazy(() => import('../modules/ModeManagement')),
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '200px 1fr', gridTemplateRows: '100px 1fr', height: '100vh', gap: '16px', padding: '16px' }}>
      {/* 顶部左侧LOGO区域 */}
      <div style={{ gridArea: '1 / 1 / 2 / 2', border: '1px solid #ccc', padding: '16px' }}>LOGO</div>
      {/* 顶部右侧模块名称区域 */}
      <div style={{ gridArea: '1 / 2 / 2 / 3', border: '1px solid #ccc', display: 'flex', justifyContent: 'center', alignItems: 'center' }}><h1 style={{ margin: 0 }}>{currentModule || '模块名称'}</h1></div>
      {/* 左侧侧边栏菜单区域 */}
      <div style={{ gridArea: '2 / 1 / 3 / 2', border: '1px solid #ccc', padding: '16px' }}><SidebarMenu onMenuClick={(modulePath) => setCurrentModule(modulePath)}/></div>
      {/* 右侧数据展示和业务操作区域 */}
      <div style={{ gridArea: '2 / 2 / 3 / 3', border: '1px solid #ccc', padding: '16px' }}>
        <React.Suspense fallback={<div>加载中...</div>}>
          {currentModule && moduleComponentMap[currentModule] && React.createElement(moduleComponentMap[currentModule])}
        </React.Suspense>
      </div>
    </div>
  );

};

export default DashboardPage;