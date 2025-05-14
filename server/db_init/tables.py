"""
数据库表同步模块

该模块负责检查数据库表是否存在，并在不存在时创建表
"""
from sqlalchemy import inspect


def check_and_sync_tables(engine, Base):
    """
    检查并同步数据库表结构

    参数:
        engine: SQLAlchemy数据库引擎对象
        Base: SQLAlchemy的Base类

    返回:
        bool: 如果所有表都成功同步返回True,否则抛出异常
    """
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    try:
        # 检查并创建指定的表
        for table in ['primary_modules', 'secondary_modules', 'roles', 'role_modules', 'users']:
            # 如果表不存在则创建
            if table not in existing_tables:
                Base.metadata.tables[table].create(engine)
        return True
    except Exception as e:
        print(f"Error occurred while creating tables: {e}")
        raise
