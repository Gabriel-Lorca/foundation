from sqlalchemy.orm import Session

from server.models import Role, PrimaryModule, SecondaryModule, RoleModule, User


def initialize_primary_modules(db: Session):
    """
    初始化primary_modules表数据

    参数:
        db: 数据库会话对象

    返回:
        PrimaryModule: 默认模块对象
    """
    module = db.query(PrimaryModule).filter(PrimaryModule.name == '系统管理').first()
    if not module:
        add_primarymodule = PrimaryModule()
        add_primarymodule.set_name('系统管理')
        db.add(add_primarymodule)
        db.commit()

        return db.query(PrimaryModule).filter(PrimaryModule.name == '系统管理').first()

    return module


def initialize_secondary_modules(db: Session, default_module):
    """
    初始化secondary_modules表数据

    参数:
        db: 数据库会话对象
        default_module: 默认主模块对象
    """

    # 向数据库添加'用户管理'二级模块,其父级模块为'系统管理'
    sig_up_module_user = db.query(SecondaryModule).filter(SecondaryModule.name == '用户管理').first()
    if not sig_up_module_user:
        add_secondarymodule = SecondaryModule()
        add_secondarymodule.set_name('用户管理')
        add_secondarymodule.set_primary_module_id(default_module.get_id())
        db.add(add_secondarymodule)
        db.commit()

    # 向数据库添加'角色管理'二级模块,其父级模块为'系统管理'
    sig_up_module_role = db.query(SecondaryModule).filter(SecondaryModule.name == '角色管理').first()
    if not sig_up_module_role:
        add_secondarymodule = SecondaryModule()
        add_secondarymodule.set_name('角色管理')
        add_secondarymodule.set_primary_module_id(default_module.get_id())
        db.add(add_secondarymodule)
        db.commit()

    # 向数据库添加'模块管理'二级模块,其父级模块为'系统管理'
    sig_up_module_role = db.query(SecondaryModule).filter(SecondaryModule.name == '模块管理').first()
    if not sig_up_module_role:
        add_secondarymodule = SecondaryModule()
        add_secondarymodule.set_name('模块管理')
        add_secondarymodule.set_primary_module_id(default_module.get_id())
        db.add(add_secondarymodule)
        db.commit()


def initialize_roles(db: Session):
    """
    初始化角色表数据

    参数:
        db: 数据库会话对象

    该函数负责向数据库插入默认角色数据
    """

    # 向数据库添加'系统管理员'角色
    role = db.query(Role).filter(Role.name == '系统管理员').first()
    if not role:
        new_role = Role()
        new_role.set_name('系统管理员')
        new_role.set_description('全权限管理员')
        new_role.set_is_deleted(False)
        new_role.set_is_deletable(False)
        db.add(new_role)
        db.commit()

def initialize_role_modules(db: Session):
    """
    初始化RoleModule表数据

    参数:
        db: 数据库会话对象
    """

    # 从数据库获取系统管理员对象
    sys_role = db.query(Role).filter(Role.name == '系统管理员').first()

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


def add_users(db: Session):
    """
    初始化Users表数据

    参数：
        db:数据库会话对象
    """
    # 获取系统管理员和普通用户角色
    sys_role = db.query(Role).filter(Role.name == '系统管理员').first()

    if not sys_role:
        return "基础角色未创建."

    # 添加系统管理员用户
    user_sys = db.query(User).filter(User.username == "admin").first()
    if not user_sys:
        new_user = User()
        new_user.set_username("admin")
        new_user.set_password("admin123")
        new_user.set_role_id(sys_role.id)
        new_user.set_is_deleted(False)
        db.add(new_user)
        db.commit()

def initialize_data(db: Session):
    """
    初始化数据库数据

    参数:
        db: 数据库会话对象

    该函数负责向数据库插入初始化数据，如默认角色、默认用户等
    """

    # 初始化primary_modules表数据,返回值:插入后从数据库查询到的数据
    primary_module = initialize_primary_modules(db)

    # 初始化secondary_modules表数据
    initialize_secondary_modules(db, primary_module)

    # 初始化initialize_roles表数据
    initialize_roles(db)

    # 初始化RoleModule表数据
    initialize_role_modules(db)

    # 初始化Users表数据
    add_users(db)
