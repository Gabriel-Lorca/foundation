import { Button, Form, Input, message, TreeSelect } from 'antd';
import apiAxios from '@../../../src/config/axios';
import { useEffect, useState } from 'react';
import styles from './AddRole.module.css';

interface Role {
  id: number;
  name: string;
  description: string;
  permission: string[];
  }

interface second_module{
  // 二级模块列表结构
  id: number;
  name: string;
  primary_module_id: number;
}  
interface First_module{
  // 一级模块列表结构
  id: number;
  name: string;
  children: second_module[];
}


const AddRole = () => {
  const [firstModule, setFirstModule] = useState<First_module[]>([]);
  // 选中权限的ID数组
  const [selectedPermissions, setSelectedPermissions] = useState<string[]>([]);

  const { SHOW_PARENT } = TreeSelect;

  // 获取可赋予权限逻辑（与获取用户列表同级）
  const fetchDescription = async () => {
    try {
      const response = await apiAxios.get('/roles/get_all_permission_data');
      setFirstModule(response.data); // 假设接口返回格式为 string[]
    } catch (error) {
      console.error('获取角色列表失败:', error);
    }
  };

  const onChange = (newValue: string[]) => {
    setSelectedPermissions(newValue);
  };

  const treeData = firstModule.map((item) => ({
    title: item.name,
    value: `${item.id}`,
    key: `${item.id}`, // 确保key是字符串类型
    children: item.children.map((child) => ({
      title: child.name,
      value: `${item.id}-${child.id}`, // 确保value是字符串类型
      key: `${item.id}-${child.id}`, // 确保key是字符串类型
    })),
  }));

  const tProps = {
    treeData,
    selectedPermissions,
    onChange,
    treeCheckable: true,
    showCheckedStrategy: SHOW_PARENT,
    placeholder: '请选择角色权限',
    style: {
      width: '100%',
    },
  };

  useEffect(() => {
    fetchDescription();
  }, []);

// 新增用户逻辑
  const handleAddUser = async (value: Role) => {
    try {
      await apiAxios.post(`/roles/add_role`, value);
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
          label="角色名"
          rules={[{ required: true, message: '请输入角色名' }]}
        >
          <Input placeholder="请输入用户名" />
        </Form.Item>

        <Form.Item
          name="description"
          label="角色描述"
          rules={[{ required: true, message: '请输入角色描述' }]}
        >
          <Input placeholder="请输入账号" />
        </Form.Item>

        <Form.Item
         name="permission" 
         label="设置角色权限"
         rules={[{ required: true, message: '请选择角色权限' }]}
         >
          <TreeSelect
            {...tProps} 
          />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit">
            新增角色
          </Button>
        </Form.Item>
      </Form>
    </div>
    );
};

export default AddRole;







