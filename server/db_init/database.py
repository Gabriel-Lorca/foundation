"""
数据库创建模块

该模块负责检查数据库是否存在，并在不存在时创建数据库
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


def check_and_create_db(db_url: str):
    """
    检查并创建数据库

    参数:
        db_url: 数据库连接URL

    返回:
        bool: 如果数据库是新创建的返回True,否则返回False
    """
    if not database_exists(db_url):
        create_database(db_url)
        return True
    return False


"""
获取数据库会话

参数:
    db_url: 数据库连接URL

返回:
    Session: 数据库会话对象
"""


def get_db_session(db_url: str):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()
