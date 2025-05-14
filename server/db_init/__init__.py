"""
数据库初始化模块

该模块负责数据库的完整初始化流程，包括创建数据库、同步表结构、初始化数据等操作
"""
from .database import check_and_create_db, get_db_session
from .tables import check_and_sync_tables
from .data import initialize_data


def initialize_database(db_url: str, Base):
    """
    初始化数据库

    参数:
        db_url: 数据库连接URL
        Base: SQLAlchemy的Base类

    返回:
        Session: 初始化后的数据库会话对象
    """
    # 创建数据库
    check_and_create_db(db_url)
    # 获取数据库会话
    db = get_db_session(db_url)
    # 同步表结构
    check_and_sync_tables(db.bind, Base)
    # 初始化数据
    initialize_data(db)
    return db
