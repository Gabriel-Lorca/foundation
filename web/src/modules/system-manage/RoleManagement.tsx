import { useState } from 'react';
import RoleList from './role-manage/RoleList';
import AddRole from './role-manage/AddRole';

const RoleManagement = () => {
  const [activeTab, setActiveTab] = useState('roleList');

  return (
    <div>
      <div className="tabs">
        <button 
          className={activeTab === 'roleList' ? 'active' : ''}
          onClick={() => setActiveTab('roleList')}
        >
          角色列表
        </button>
        <button
          className={activeTab === 'AddRole' ? 'active' : ''}
          onClick={() => setActiveTab('AddRole')}
        >
          新增角色
        </button>
        
      <hr className="tab-divider" />
      </div>
      
      <div className="tab-content">
        {activeTab === 'roleList' && <RoleList />}
        {activeTab === 'AddRole' && <AddRole />}
      </div>
    </div>
  );
};

export default RoleManagement;