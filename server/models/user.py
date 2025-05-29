from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from .base import Base
from passlib.context import CryptContext


class User(Base):
    """
    用户表ORM对象,用于管理系统用户信息
    Attributes:
        id: 主键，自增整数，唯一标识每个用户
        name:用户名称,字符串类型,用于区分用户.
        phone_num:用户手机号.
        username: 用户名，字符串类型，唯一且必须索引，用于用户登录
        password_hash: 密码哈希值，字符串类型，存储加密后的用户密码
        role_name: 角色名称
        role_id: 外键，关联角色表，表示用户所属角色
        is_deleted: 布尔类型,默认值为False,用于软删除标记
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_num = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role_name = Column(String, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    is_deleted = Column(Boolean, default=False, nullable=False)

    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_phone_num(self, phone_num):
        self.phone_num = phone_num

    def get_phone_num(self):
        return self.phone_num

    def set_username(self, username: str):
        self.username = username

    def get_username(self) -> str:
        return self.username

    def set_role_name(self, role_name: str):
        self.role_name = role_name

    def get_role_name(self):
        return self.role_name

    def set_role_id(self, role_id: int):
        self.role_id = role_id

    def get_role_id(self) -> int:
        return self.role_id

    def set_is_deleted(self, is_deleted: bool):
        self.is_deleted = is_deleted

    def get_is_deleted(self) -> bool:
        return self.is_deleted

    def set_password(self, password):
        """
        设置用户密码，将明文密码加密后存储
        Args:
            password (str): 用户输入的明文密码
        Returns:
            None
        """
        self.password_hash = self.pwd_context.hash(password)

    def verify_password(self, password):
        """
        验证用户密码，将输入的密码与存储的哈希值进行比对
        Args:
            password (str): 用户输入的明文密码
        Returns:
            bool: 密码匹配返回True,否则返回False
        """
        return self.pwd_context.verify(password, self.password_hash)
