import { useState } from 'react';
import UserList from './user-manage/UserList';
import AddUser from './user-manage/AddUser';
import { Radio,Divider } from 'antd';

const UserManagement = () => {
  const [activeTab, setActiveTab] = useState('userList');

  return (
    <div className="user-management">
      <div className="tabs">
        <Radio.Group>
          <Radio.Button className={activeTab === 'userList' ? 'active' : ''}
          onClick={() => setActiveTab('userList')} value="userList">用户列表</Radio.Button>
          <Radio.Button className={activeTab === 'AddUser' ? 'active' : ''}
          onClick={() => setActiveTab('AddUser')} value="AddUser">新增用户</Radio.Button>
        </Radio.Group>
        <Divider dashed />
      </div>
      
      <div className="tab-content">
        {activeTab === 'userList' && <UserList />}
        {activeTab === 'AddUser' && <AddUser />}
      </div>
    </div>
  );
};

export default UserManagement;