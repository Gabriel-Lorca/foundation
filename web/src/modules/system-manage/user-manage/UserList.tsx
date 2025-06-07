import { Modal, Form, Input, Select, message } from 'antd';
import React, { useEffect, useState } from 'react';
import apiAxios from '@../../../src/config/axios';
import styles from './UserList.module.css';



interface User {
  id: number;
  name: string;
  phone_num: string;
  role_name: string;
  is_deleted: boolean;
  s_deletable: boolean;
}

interface User_Update {
  name: string;
  phone_num: string;
  role_name: string;
}

const UserList: React.FC = () => {
  

  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  // 新增状态：控制模态框显示、记录当前编辑用户
  const [isEditModalVisible, setIsEditModalVisible] = useState(false);
  const [currentEditUser, setCurrentEditUser] = useState<User | null>(null);
  // 新增角色数据状态
  const [roles, setRoles] = useState<string[]>([]);
  // const [fo, setSelectedRoles] = useState<string[]>([]); // 新增角色状态
  const [form] = Form.useForm(); // 获取表单实例

  // 获取用户列表逻辑
  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await apiAxios.get('/users/all');
      setUsers(response.data);
    } catch (err) {
      setError('获取用户列表失败');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // 获取角色数据逻辑（与获取用户列表同级）
  const fetchRoles = async () => {
    try {
      const response = await apiAxios.get('/roles/all');
      setRoles(response.data); // 假设接口返回格式为 string[]
    } catch (error) {
      console.error('获取角色列表失败:', error);
    }
  };

  // 删除用户逻辑
  const handleDelete = async (id: number) => {
    try {
      await apiAxios.post(`/users/del/${id}`);
      message.success('删除成功');
      // 重新获取用户列表数据
      fetchUsers(); 
    } catch (error) {
      message.error('删除失败');
      console.error('删除用户失败:', error);
    }
  };

  //编辑用户逻辑
  const handleEditSubmit = async (value: User_Update) => {
    try {
      await apiAxios.post(`/users/update/${currentEditUser!.id}`, value);
      message.success('编辑成功');
      
    } catch (error) {
      message.error('编辑失败');
      console.error('编辑用户失败:', error);
    }
    setIsEditModalVisible(false)
    fetchUsers();
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  useEffect(() => {
    
    if (isEditModalVisible && currentEditUser) {
      // 当模态框打开且有当前编辑用户时，初始化表单值
      form.setFieldsValue(currentEditUser);
    }
  }, [isEditModalVisible,currentEditUser,form]);

  const handleEdit = (user: User) => {
    fetchRoles(); // 确保在打开编辑模态框前获取角色数据
    setCurrentEditUser(user); // 记录当前编辑的用户
    setIsEditModalVisible(true); // 显示模态框
  };

  if (loading) return <div>加载中...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className={styles['user-list']}>
      
      <table className={styles['user-list-table']}>
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>手机号</th>
            <th>角色</th>
            <th>状态</th>
            <th>编辑用户</th>
            <th>删除用户</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.name}</td>
              <td>{user.phone_num}</td>
              <td>{user.role_name}</td>
              <td>
              {user.is_deleted ? (
                  <span className="user-list-status user-list-status-deleted" style={{ color: 'red' }}>禁用</span>
                ) : (
                  <span className="user-list-status user-list-status-active">启用</span>
                )}
              </td>
              <td><button className="edit-btn" onClick={() => handleEdit(user)} disabled={!user.s_deletable || user.is_deleted}>
                {!user.s_deletable || user.is_deleted ? (
                  <span className='user-list-status user-list-status-disabled'>禁止编辑</span>
                ):(<span className='user-list-status user-list-status-disabled'>修改</span>)}
                  </button></td>
             
              <td className="user-list-cell">
                <button className="delete-btn" onClick={() => handleDelete(user.id)} disabled={!user.s_deletable}>
                  {!user.s_deletable ? (
                    <span className="user-list-status user-list-status-disabled">禁止删除</span>
                  ) : (user.is_deleted ? (
                    <span className="user-list-status user-list-status-deleted">恢复</span>
                  ) : (
                    <span className="user-list-status user-list-status-active">删除</span>
                  ))}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <Modal
        title="编辑用户信息"
        // 假设使用新的属性来替代 visible，这里假设新属性名为 isModalOpen
        open={isEditModalVisible}
        okText="提交"
        cancelText="取消"
        // 由于 onOk 期望的是鼠标事件处理函数，而 handleEditSubmit 需要表单值，
        // 这里手动触发表单提交以获取表单值并调用 handleEditSubmit
        onOk={() => {
          const form = document.querySelector('form');
          if (form) {
            form.requestSubmit();
          }
        }}
        onCancel={() => setIsEditModalVisible(false)}
      >
        <Form
          form={form}
        // 由于 currentEditUser 可能为 null，这里需要做非空判断，避免类型错误
          initialValues={currentEditUser ? currentEditUser : undefined}
          onFinish={handleEditSubmit}
        >
          <Form.Item
            name="name"
            label="用户名"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input placeholder="请输入用户名" />
          </Form.Item>
          <Form.Item
            name="phone_num"
            label="手机号"
            rules={[{ required: true, message: '请输入手机号' }, { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确' }]}
          >
            <Input placeholder="请输入手机号" />
          </Form.Item>

          <Form.Item
            name="role_name"
            label="角色"
            rules={[{ required: true, message: '请选择角色' }]}
          >

            <Select placeholder="请选择角色">
              {roles.map(role => (
                <Select.Option key={role} value={role}>{role}</Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default UserList;




