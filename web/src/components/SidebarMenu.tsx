import React from 'react';
import { Menu } from 'antd';
import type { MenuProps } from 'antd';


interface SidebarMenuProps {
  items?: MenuProps['items'];
}

const SidebarMenu: React.FC<SidebarMenuProps> = ({ items: propItems }) => {
  const [items, setItems] = React.useState(propItems || []);

  React.useEffect(() => {
    const fetchMenuData = async () => {
      try {
        const loginResponse = localStorage.getItem('loginResponse');
        const token = loginResponse? JSON.parse(loginResponse).access_token : '';
        const response = await fetch('http://127.0.0.1:8000/menu/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const data = await response.json();
        console.log('Menu data:', data);
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
    />
  );
};

export default SidebarMenu;