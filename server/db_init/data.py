import sys

from sqlalchemy.orm import Session
from server.models import Role, PrimaryModule, SecondaryModule, RoleModule, User
from server.main import config


def initialize_primary_modules(db: Session, first_menu):
    """
    初始化primary_modules表数据

    参数:
        db: 数据库会话对象

    返回:
        PrimaryModule: 默认模块对象
    """
    module = db.query(PrimaryModule).filter(PrimaryModule.name == first_menu).first()
    if not module:
        add_primarymodule = PrimaryModule()
        add_primarymodule.set_name(first_menu)
        db.add(add_primarymodule)
        db.commit()

        return db.query(PrimaryModule).filter(PrimaryModule.name == first_menu).first()

    return module


def initialize_secondary_modules(db: Session, default_module, second_menu_name):
    """
    初始化secondary_modules表数据

    参数:
        db: 数据库会话对象
        default_module: 默认主模块对象
    """

    # 向数据库添加'用户管理'二级模块,其父级模块为'系统管理'
    sig_up_module_user = db.query(SecondaryModule).filter(SecondaryModule.name == second_menu_name).first()
    if not sig_up_module_user:
        add_secondarymodule = SecondaryModule()
        add_secondarymodule.set_name(second_menu_name)
        add_secondarymodule.set_primary_module_id(default_module.get_id())
        db.add(add_secondarymodule)
        db.commit()


def initialize_roles(db: Session, default_roles: Role) -> None:
    """
    初始化角色表数据

    参数:
        db: 数据库会话对象

    该函数负责向数据库插入默认角色数据
    """

    # 向数据库添加'系统管理员'角色
    role = db.query(Role).filter(Role.name == default_roles.get_name()).first()
    if not role:
        db.add(default_roles)
        db.commit()


def initialize_role_modules(db: Session, default_roles: Role) -> None:
    """
    初始化RoleModule表数据

    参数:
        db: 数据库会话对象
    """

    # 从数据库获取系统管理员对象
    sys_role = db.query(Role).filter(Role.name == default_roles.get_name()).first()

    # 获取所有二级模块
    SecondaryModules = db.query(SecondaryModule).all()

    # 循环检查,关联关系是否存在
    for secondary_module in SecondaryModules:
        role_module = db.query(RoleModule).filter(RoleModule.role_id == sys_role.id, RoleModule.primary_module_id ==
                                                  secondary_module.primary_module_id, RoleModule.secondary_module_id
                                                  == secondary_module.id).first()
        if not role_module:
            new_role = RoleModule()
            new_role.set_role_id(sys_role.id)
            new_role.set_primary_module_id(secondary_module.primary_module_id)
            new_role.set_secondary_module_id(secondary_module.id)
            db.add(new_role)
            db.commit()


def add_users(db: Session, sys_role: Role, sys_user: User) -> None:
    """
    初始化Users表数据

    参数：
        db:数据库会话对象
    """
    # 获取系统管理员角色
    sys_role_id = db.query(Role).filter(Role.name == sys_role.get_name()).first().id

    if not sys_role:
        print("基础角色未创建,删除数据库文件后重新启动程序.")
        sys.exit(1)

    # 添加系统管理员用户
    user_sys = db.query(User).filter(User.username == sys_user.get_username()).first()
    if not user_sys:
        sys_user.set_role_id(sys_role_id)
        sys_user.set_is_deleted(False)
        db.add(sys_user)
        db.commit()


def init_menus_data(db: Session, menus: list) -> None:
    """
    初始化一二级模块数据
    :param db:
    :param menus:
    :return:
    """
    for menu_map in menus:
        first_menu_name = menu_map.get("name")
        second_menu = menu_map.get("children")

        # 初始化primary_modules表数据,返回值:插入后从数据库查询到的数据
        primary_module = initialize_primary_modules(db, first_menu_name)

        for second_menu_name in second_menu:
            # 初始化secondary_modules表数据
            initialize_secondary_modules(db, primary_module, second_menu_name)


def initialize_data(db: Session):
    """
    初始化数据库数据

    参数:
        db: 数据库会话对象

    该函数负责向数据库插入初始化数据，如默认角色、默认用户等
    """
    # 配置文件数据
    menus = config.get("menus", {})
    default_role = config.get("default_role")
    default_user = config.get("default_user")

    # 初始化一二级模块数据
    init_menus_data(db, menus)

    # 初始化initialize_roles表数据
    new_role = Role(name=default_role.get("name"), description=default_role.get("description"),
                    is_deleted=default_role.get("is_deleted"), is_deletable=default_role.get("is_deleted"))
    initialize_roles(db, new_role)

    # 初始化RoleModule表数据
    initialize_role_modules(db, new_role)

    # 初始化Users表数据
    new_user = User(name=default_user.get("name"), phone_num=default_user.get("phone_num"),
                    username=default_user.get("username"), role_name=default_user.get("role_name"),
                    is_deleted=default_user.get("is_deleted"), s_deletable=default_user.get("s_deletable"))
    new_user.set_password(default_user.get("password"))
    add_users(db, new_role, new_user)
