import React from 'react';
import { Menu } from 'antd';
import type { MenuProps } from 'antd';

/**
 * SidebarMenu组件属性接口
 * @property {MenuProps['items']} [items] - 可选的菜单项数组
 */
interface SidebarMenuProps {
  items?: MenuProps['items'];
  onMenuClick?: (modulePath: string) => void;
}

/**
 * 侧边栏菜单组件
 * @param {SidebarMenuProps} props - 组件属性
 * @returns {React.ReactElement} 返回Ant Design的Menu组件
 */
const SidebarMenu: React.FC<SidebarMenuProps> = ({ items: propItems, onMenuClick }) => {
  // 菜单项状态管理
  const [items, setItems] = React.useState(propItems || []);

  // 组件挂载时获取菜单数据
  React.useEffect(() => {
    /**
 * 异步获取菜单数据
 * 1. 从localStorage获取登录凭证
 * 2. 使用Bearer Token认证
 * 3. 请求后端接口获取菜单数据
 * 4. 更新菜单项状态
 */
const fetchMenuData = async () => {
  try {
    // 获取本地存储的登录凭证
    const loginResponse = localStorage.getItem('loginResponse');
    // 解析并获取access_token
    const token = loginResponse? JSON.parse(loginResponse).access_token : '';
    // 请求菜单数据接口
    const response = await fetch('http://127.0.0.1:8000/menu/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    // 解析响应数据
    const data = await response.json();
    // 更新菜单项状态
    setItems(data);
  } catch (error) {
    console.error('Failed to fetch menu:', error);
  }
};

    fetchMenuData();
  }, []);

  return (
    <Menu
      mode="inline"
      defaultOpenKeys={[]}
      style={{ width: '100%', height: '100%' }}
      items={items}
      onClick={({ keyPath }) => {
        if (onMenuClick) {
          for (const item of items) {
            if (item && 'children' in item && 'label' in item && item?.key?.toString() === keyPath[1]) {
              console.log('item:', item.label);
              const children = item.children || [];
              if (children.length > 0) {
                for (const child of children) {
                  if (child && 'label' in child && child?.key?.toString() === keyPath[0]) {
                    console.log('child:', child.label);
                    const modulePath = `${item.label}-${child.label}`;
                    onMenuClick(modulePath);
                  }
                }
              }
            }
          }
        }
      }}
    />
  );
};

export default SidebarMenu;