import apiAxios from '@../../../src/config/axios';
import { useNavigate } from 'react-router-dom';
import styles from './LoginPage.module.css';
import { Button, Form, Input } from 'antd';
import React, { useState } from 'react';




const LoginPage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onFinish = async (values: any) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('username', values.username);
      formData.append('password', values.password);
      const response = await apiAxios.post('/token', formData);
      localStorage.setItem('loginResponse', JSON.stringify(response.data));
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
        <div className={styles.loginBox}>
            <Form
              name="login"
              onFinish={onFinish}
              layout="vertical"
            >
              <Form.Item
                label="用户名"
                name="username"
                rules={[{ required: true, message: '请输入用户名' }]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="密码"
                name="password"
                rules={[{ required: true, message: '请输入密码' }]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  登录
                </Button>
              </Form.Item>
            </Form>
        </div>
    </div>
);
};

export default LoginPage;