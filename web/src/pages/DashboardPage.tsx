import React from 'react';
import SidebarMenu from '../components/SidebarMenu';

const DashboardPage: React.FC = () => {

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '200px 1fr', gridTemplateRows: '100px 1fr', height: '100vh', gap: '16px', padding: '16px' }}>
      <div style={{ gridArea: '1 / 1 / 2 / 2', border: '1px solid #ccc', padding: '16px' }}>LOGO</div>
      <div style={{ gridArea: '1 / 2 / 2 / 3', border: '1px solid #ccc', padding: '16px' }}>模块名称</div>
      <div style={{ gridArea: '2 / 1 / 3 / 2', border: '1px solid #ccc', padding: '16px' }}><SidebarMenu/></div>
      <div style={{ gridArea: '2 / 2 / 3 / 3', border: '1px solid #ccc', padding: '16px' }}>数据展示和业务操作</div>
    </div>
  );
};

export default DashboardPage;