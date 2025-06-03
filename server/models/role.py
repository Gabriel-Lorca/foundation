from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint, Boolean
from .base import Base


class PrimaryModule(Base):
    """
    主模块表, 用于存储系统的主要功能模块
    Attributes:
        id: 主键, 自增整数, 唯一标识每个主模块
        name: 模块名称, 字符串类型, 最大长度50, 唯一且不能为空, 用于标识模块
    """
    __tablename__ = 'primary_modules'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name


class SecondaryModule(Base):
    """
    子模块表, 用于存储主模块下的子功能模块
    Attributes:
        id: 主键, 自增整数, 唯一标识每个子模块
        name: 模块名称, 字符串类型, 最大长度50, 不能为空, 用于标识子模块
        primary_module_id: 外键, 关联主模块表, 表示该子模块所属的主模块
    """
    __tablename__ = 'secondary_modules'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    primary_module_id = Column(Integer, ForeignKey('primary_modules.id'))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_primary_module_id(self):
        return self.primary_module_id

    def set_name(self, name):
        self.name = name

    def set_primary_module_id(self, primary_module_id):
        self.primary_module_id = primary_module_id


class Role(Base):
    """
    角色表, 用于存储系统中的用户角色信息
    Attributes:
        id: 主键, 自增整数, 唯一标识每个角色
        name: 角色名称, 字符串类型, 最大长度50, 唯一且不能为空, 用于标识角色
        description: 角色描述, 字符串类型, 最大长度255, 可以为空, 用于描述角色的详细功能
        is_deleted: 布尔类型, 默认值为False, 用于软删除标记
        is_deletable: 布尔类型, 默认值为True, 表示该角色是否允许删除
    """
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    is_deletable = Column(Boolean, default=True, nullable=False, comment='表示该角色是否允许删除')

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_is_deleted(self):
        return self.is_deleted

    def get_is_deletable(self):
        return self.is_deletable

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_is_deleted(self, is_deleted):
        self.is_deleted = is_deleted

    def set_is_deletable(self, is_deletable):
        self.is_deletable = is_deletable


class RoleModule(Base):
    """
    角色模块关联表, 用于建立角色与模块之间的权限关系
    Attributes:
        role_id: 外键, 关联角色表, 不能为空, 表示关联的角色
        primary_module_id: 外键, 关联主模块表, 不能为空, 表示关联的主模块
        secondary_module_id: 外键, 关联子模块表, 不能为空, 表示关联的子模块
    """
    __tablename__ = 'role_modules'
    __table_args__ = (
        PrimaryKeyConstraint('role_id', 'primary_module_id', 'secondary_module_id'),
    )

    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    primary_module_id = Column(Integer, ForeignKey('primary_modules.id'), nullable=False)
    secondary_module_id = Column(Integer, ForeignKey('secondary_modules.id'), nullable=False)

    def get_role_id(self):
        return self.role_id

    def set_role_id(self, role_id):
        self.role_id = role_id

    def get_primary_module_id(self):
        return self.primary_module_id

    def get_secondary_module_id(self):
        return self.secondary_module_id

    def set_primary_module_id(self, primary_module_id):
        self.primary_module_id = primary_module_id

    def set_secondary_module_id(self, secondary_module_id):
        self.secondary_module_id = secondary_module_id
