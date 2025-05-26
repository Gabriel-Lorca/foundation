from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.models import Role, PrimaryModule, SecondaryModule, RoleModule, User
from server.dependencies import get_db, get_current_user

router = APIRouter(prefix="/menu", tags=["roles"])

"""
获取当前用户的菜单权限

Args:
    db (Session): 数据库会话
    current_user (User): 当前用户对象

Returns:
    list: 包含用户有权限访问的菜单列表，每个菜单项包含以下字段：
        - key: 主模块ID
        - label: 主模块名称
        - children: 子模块列表，每个子模块包含：
            - key: 主模块ID-子模块ID
            - label: 子模块名称
"""


@router.get("/")
async def read_menu(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 获取当前用户角色
    role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not role:
        return []

    # 获取该角色对应的模块权限
    role_modules = db.query(RoleModule).filter(RoleModule.role_id == role.id).all()

    # 获取所有主模块
    primary_modules = db.query(PrimaryModule).all()

    # 构建返回结果
    result = []
    for primary_module in primary_modules:
        # 获取当前主模块下的二级模块
        secondary_modules = db.query(SecondaryModule).filter(
            SecondaryModule.primary_module_id == primary_module.id,
            SecondaryModule.id.in_([rm.secondary_module_id for rm in role_modules])
        ).all()

        if secondary_modules:
            module_data = {
                "key": primary_module.id,
                "label": primary_module.name,
                "children": [
                    {
                        "key": str(primary_module.id) + "-" + str(secondary_module.id),
                        "label": secondary_module.name,
                    } for secondary_module in secondary_modules
                ]
            }
            result.append(module_data)
    return result


"""
创建主模块

Args:
    name (str): 主模块名称
    db (Session): 数据库会话

Returns:
    dict: 包含成功消息和创建的主模块ID

Raises:
    HTTPException: 如果数据库操作失败
"""


@router.post("/primary-modules")
async def create_primary_module(name: str, db: Session = Depends(get_db)):
    primary_module = PrimaryModule(name=name)
    try:
        db.add(primary_module)
        db.commit()
        db.refresh(primary_module)
        
        # 获取管理员角色
        admin_role = db.query(Role).filter(Role.name == "系统管理员").first()
        if admin_role:
            # 为管理员角色添加新主模块的权限
            role_module = RoleModule(
                role_id=admin_role.id,
                primary_module_id=primary_module.id
            )
            db.add(role_module)
            db.commit()
            db.refresh(role_module)
        
        return {"message": "Primary module created successfully", "module_id": primary_module.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


"""
创建子模块

Args:
    name (str): 子模块名称
    primary_module_id (int): 所属主模块ID
    db (Session): 数据库会话

Returns:
    dict: 包含成功消息和创建的子模块ID

Raises:
    HTTPException: 如果数据库操作失败
"""


@router.post("/secondary-modules")
async def create_secondary_module(name: str, primary_module_id: int, db: Session = Depends(get_db)):
    secondary_module = SecondaryModule(name=name, primary_module_id=primary_module_id)
    try:
        db.add(secondary_module)
        db.commit()
        db.refresh(secondary_module)
        return {"message": "Secondary module created successfully", "module_id": secondary_module.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


"""
更新主模块信息

Args:
    module_id (int): 要更新的主模块ID
    name (str): 新的主模块名称
    db (Session): 数据库会话

Returns:
    dict: 包含成功消息

Raises:
    HTTPException: 如果主模块不存在或数据库操作失败
"""


@router.put("/primary-modules/{module_id}")
async def update_primary_module(module_id: int, name: str, db: Session = Depends(get_db)):
    primary_module = db.query(PrimaryModule).filter(PrimaryModule.id == module_id).first()
    if not primary_module:
        raise HTTPException(status_code=404, detail="Primary module not found")

    primary_module.name = name
    try:
        db.commit()
        db.refresh(primary_module)
        return {"message": "Primary module updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


"""
更新子模块信息

Args:
    module_id (int): 要更新的子模块ID
    name (str): 新的子模块名称
    db (Session): 数据库会话

Returns:
    dict: 包含成功消息

Raises:
    HTTPException: 如果子模块不存在或数据库操作失败
"""


@router.put("/secondary-modules/{module_id}")
async def update_secondary_module(module_id: int, name: str, db: Session = Depends(get_db)):
    secondary_module = db.query(SecondaryModule).filter(SecondaryModule.id == module_id).first()
    if not secondary_module:
        raise HTTPException(status_code=404, detail="Secondary module not found")

    secondary_module.name = name
    try:
        db.commit()
        db.refresh(secondary_module)
        return {"message": "Secondary module updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


"""
删除主模块

Args:
    module_id (int): 要删除的主模块ID
    db (Session): 数据库会话

Returns:
    dict: 包含成功消息

Raises:
    HTTPException: 如果主模块不存在或数据库操作失败
"""


@router.delete("/primary-modules/{module_id}")
async def delete_primary_module(module_id: int, db: Session = Depends(get_db)):
    primary_module = db.query(PrimaryModule).filter(PrimaryModule.id == module_id).first()
    if not primary_module:
        raise HTTPException(status_code=404, detail="Primary module not found")

    try:
        db.delete(primary_module)
        db.commit()
        return {"message": "Primary module deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


"""
删除子模块

Args:
    module_id (int): 要删除的子模块ID
    db (Session): 数据库会话

Returns:
    dict: 包含成功消息

Raises:
    HTTPException: 如果子模块不存在或数据库操作失败
"""


@router.delete("/secondary-modules/{module_id}")
async def delete_secondary_module(module_id: int, db: Session = Depends(get_db)):
    secondary_module = db.query(SecondaryModule).filter(SecondaryModule.id == module_id).first()
    if not secondary_module:
        raise HTTPException(status_code=404, detail="Secondary module not found")

    try:
        db.delete(secondary_module)
        db.commit()
        return {"message": "Secondary module deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
