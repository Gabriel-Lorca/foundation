import { useState } from 'react';
import RoleList from './role-manage/RoleList';
import AddRole from './role-manage/AddRole';
import { Radio,Divider } from 'antd';

const RoleManagement = () => {
  const [activeTab, setActiveTab] = useState('roleList');

  return (
    <div>
      <div className="tabs">
        <Radio.Group>
          <Radio.Button className={activeTab === 'roleList' ? 'active' : ''}
          onClick={() => setActiveTab('roleList')} value="roleList">角色列表</Radio.Button>
          <Radio.Button className={activeTab === 'AddRole' ? 'active' : ''}
          onClick={() => setActiveTab('AddRole')} value="AddRole">新增角色</Radio.Button>
        </Radio.Group>
        <Divider dashed />
      </div>
      
      <div className="tab-content">
        {activeTab === 'roleList' && <RoleList />}
        {activeTab === 'AddRole' && <AddRole />}
      </div>
    </div>
  );
};

export default RoleManagement;