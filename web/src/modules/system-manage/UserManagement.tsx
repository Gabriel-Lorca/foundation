import React, { useState } from 'react';
import UserList from './user-manage/UserList';
import AddUser from './user-manage/AddUser';

const UserManagement = () => {
  const [activeTab, setActiveTab] = useState('userList');

  return (
    <div className="user-management">
      <div className="tabs">
        <button 
          className={activeTab === 'userList' ? 'active' : ''}
          onClick={() => setActiveTab('userList')}
        >
          用户列表
        </button>
        <button
          className={activeTab === 'AddUser' ? 'active' : ''}
          onClick={() => setActiveTab('AddUser')}
        >
          新增用户
        </button>
        
      <hr className="tab-divider" />
      </div>
      
      <div className="tab-content">
        {activeTab === 'userList' && <UserList />}
        {activeTab === 'AddUser' && <AddUser />}
      </div>
    </div>
  );
};

export default UserManagement;