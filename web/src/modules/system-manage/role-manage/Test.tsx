import React from 'react';
import styles from './Test.module.css';

import { useEffect, useState } from 'react';
import apiAxios from '@../../../src/config/axios'; // 假设apiAxios路径正确，根据项目实际路径调整

interface ChildMenu {
  id: number;
  name: string;
  primary_module_id: number;
}

interface MenuData {
  id: number;
  name: string;
  children: ChildMenu[];
}

const Test: React.FC = () => {
  const [menuData, setMenuData] = useState<MenuData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMenuData = async () => {
    try {
      const response = await apiAxios.get('/ket');
      setMenuData(response.data);
      setError(null);
    } catch (err) {
      setError('数据请求失败，请稍后重试');
      console.error('请求失败:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMenuData();
  }, []);

  return (
    <div className={styles.container}>
      <h2>Test Component - 菜单数据</h2>
      {loading ? (
        <p>数据加载中...</p>
      ) : error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : (
        <ul>
          {menuData.map((menu) => (
            <li key={menu.id}>
              <h3>{menu.name}</h3>
              <ul>
                {menu.children.map((child) => (
                  <li key={child.id}>{child.name}</li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Test;