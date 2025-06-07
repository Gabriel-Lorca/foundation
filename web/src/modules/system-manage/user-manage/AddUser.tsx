import { Button, Form, Input, Select, message } from 'antd';
import apiAxios from '@../../../src/config/axios';
import { useEffect, useState } from 'react';
import styles from './AddUser.module.css';



interface User {
  id: number;
  name: string;
  phone_num: string;
  role_name: string;
  username: string;
  password_hash: string;
}

const AddUser = () => {
  const [roles, setRoles] = useState<string[]>([]);

  // 获取角色数据逻辑（与获取用户列表同级）
  const fetchRoles = async () => {
    try {
      const response = await apiAxios.get('/roles/all');
      setRoles(response.data); // 假设接口返回格式为 string[]
    } catch (error) {
      console.error('获取角色列表失败:', error);
    }
  };

  useEffect(() => {
    fetchRoles();
  }, []);

  // 新增用户逻辑
  const handleAddUser = async (value: User) => {
    try {
      console.log('新增用户数据:', value);
      await apiAxios.post('/users/add_user', value);
      message.success('新增成功');
    } catch (error) {
      message.error('新增失败');
      console.error('新增用户失败:', error);
    }
  };

  return (
    <div style={{ width: '50%', margin: '0 auto' }}>

      <Form
        name="addUserForm"
        layout="vertical"
        onFinish={handleAddUser}
        initialValues={{ role_name: '' }}
        className={styles['add-user-form']}
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
          name="username"
          label="账号"
          rules={[{ required: true, message: '请输入账号' }]}
        >
          <Input placeholder="请输入账号" />
        </Form.Item>

        <Form.Item
          name="password_hash"
          label="密码"
          rules={[{ required: true, message: '请输入密码' }]}
        >
          <Input.Password placeholder="请输入密码" />
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

        <Form.Item>
          <Button type="primary" htmlType="submit">
            添加用户
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default AddUser;

