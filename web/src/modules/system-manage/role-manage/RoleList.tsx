import { Modal, Form, Input, message,TreeSelect } from 'antd';
import React, { useEffect, useState as roleState } from 'react';
import apiAxios from '@../../../src/config/axios';
import styles from './RoleList.module.css';



interface Role {
  id: number;
  name: string;
  description: string;
  is_deleted: boolean;
  is_deletable: boolean;
}

interface User_Update {
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

const RoleList: React.FC = () => {
  
  const [firstModule, setFirstModule] = roleState<First_module[]>([]);
  const [roles, setRoles] = roleState<Role[]>([]);
  const [loading, setLoading] = roleState(false);
  const [error, setError] = roleState('');
  // 新增状态：控制模态框显示、记录当前编辑用户
  const [isEditModalVisible, setIsEditModalVisible] = roleState(false);
  const [currentEditRole, setCurrentEditRole] = roleState<Role | null>(null);
  const [selectedPermissions, setSelectedPermissions] = roleState<string[]>([]);
  const { SHOW_PARENT } = TreeSelect;
  const [form] = Form.useForm();
  // 新增角色数据状态

  // 获取用户列表逻辑
  const fetchRoles = async () => {
    try {
      setLoading(true);
      const response = await apiAxios.get('/roles/role_data');
      setRoles(response.data);
    } catch (err) {
      setError('获取用户列表失败');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // 获取可赋予权限逻辑（与获取用户列表同级）
  const fetchDescription = async () => {
    try {
      const response = await apiAxios.get('/roles/get_all_permission_data');
      setFirstModule(response.data); // 假设接口返回格式为 string[]
    } catch (error) {
      console.error('获取角色列表失败:', error);
    }
  };

  // 删除角色逻辑
  const handleDelete = async (id: number) => {
    try {
      await apiAxios.post(`/roles/del/${id}`);
      message.success('删除成功');
      // 重新获取用户列表数据
      fetchRoles(); 
    } catch (error) {
      message.error('删除失败');
      console.error('删除用户失败:', error);
    }
  };

  //编辑用户逻辑
  const handleEditSubmit = async (value: User_Update) => {
    try {
      await apiAxios.post(`/roles/update/${currentEditRole!.id}`, value);
      message.success('编辑成功');
      
    } catch (error) {
      message.error('编辑失败');
      console.error('编辑用户失败:', error);
    }
    setIsEditModalVisible(false)
    fetchRoles();
  };

  useEffect(() => {
    fetchRoles();
  }, []);

  useEffect(() => {
    if (isEditModalVisible && currentEditRole) {
      console.log('isEditModalVisible:',isEditModalVisible)
      form.setFieldsValue(currentEditRole);
    }
  }, [isEditModalVisible, currentEditRole, form]);

  const handleEdit = (role: Role) => {
    setCurrentEditRole(role); // 记录当前编辑的角色信息
    fetchDescription(); // 确保在编辑用户时重新获取权限列表
    setIsEditModalVisible(true); // 显示模态框
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

  const onChange = (newValue: string[]) => {
    setSelectedPermissions(newValue);
  };

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

  if (loading) return <div>加载中...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className={styles['user-list']}>
      <h3>角色列表</h3>
      <table className={styles['user-list-table']}>
        <thead>
          <tr>
            <th>ID</th>
            <th>角色名</th>
            <th>角色描述</th>
            <th>状态</th>
            <th>编辑用户</th>
            <th>删除用户</th>
          </tr>
        </thead>
        <tbody>
          {roles.map(role => (
            <tr key={role.id}>
              <td>{role.id}</td>
              <td>{role.name}</td>
              <td>{role.description}</td>
              <td>
              {role.is_deleted ? (
                  <span className="user-list-status user-list-status-deleted" style={{ color: 'red' }}>禁用</span>
                ) : (
                  <span className="user-list-status user-list-status-active">启用</span>
                )}
              </td>
              <td><button className="edit-btn" onClick={() => handleEdit(role)} disabled={!role.is_deletable || role.is_deleted}>
                {!role.is_deletable || role.is_deleted ? (
                  <span className='user-list-status user-list-status-disabled'>禁止编辑</span>
                ):(<span className='user-list-status user-list-status-disabled'>修改</span>)}
                  </button></td>
             
              <td className="user-list-cell">
                <button className="delete-btn" onClick={() => handleDelete(role.id)} disabled={!role.is_deletable}>
                  {!role.is_deletable ? (
                    <span className="user-list-status user-list-status-disabled">禁止删除</span>
                  ) : (role.is_deleted ? (
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
        // 由于 currentEditUser 可能为 null，这里需要做非空判断，避免类型错误
          form={form}
          initialValues={currentEditRole ? currentEditRole : undefined}
          onFinish={handleEditSubmit}
        >
          <Form.Item
            name="name"
            label="角色名"
            rules={[{ required: true, message: '请输入角色名' }]}
          >
            <Input placeholder="请输入角色名" />
          </Form.Item>
          <Form.Item
            name="description"
            label="角色描述"
            rules={[{ required: true, message: '请输入角色描述' }]}
          >
            <Input placeholder="请输入角色描述" />
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
        </Form>
      </Modal>
    </div>
  );
};

export default RoleList;




