from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.models import Role, PrimaryModule, SecondaryModule
from server.dependencies import get_db

router = APIRouter(prefix="/roles", tags=["roles"])

"""
创建新角色

Args:
    name (str): 角色名称
    description (str): 角色描述
    db (Session): 数据库会话

Returns:
    dict: 包含成功消息和新角色ID的字典

Raises:
    HTTPException: 如果角色已存在或数据库操作失败
"""


@router.post("/")
async def create_role(name: str, description: str, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.name == name).first()
    if role:
        raise HTTPException(status_code=400, detail="Role already exists")

    new_role = Role()
    new_role.set_name(name)
    new_role.set_description(description)
    new_role.set_is_deleted(False)
    new_role.set_is_deletable(True)

    try:
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return {"message": "Role created successfully", "role_id": new_role.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


"""
根据ID获取角色信息

Args:
    role_id (int): 角色ID
    db (Session): 数据库会话

Returns:
    Role: 角色对象

Raises:
    HTTPException: 如果角色不存在
"""


@router.get("/{role_id}")
async def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


"""
更新角色信息

Args:
    role_id (int): 角色ID
    name (str): 新角色名称
    description (str): 新角色描述
    db (Session): 数据库会话

Returns:
    dict: 包含成功消息的字典

Raises:
    HTTPException: 如果角色不存在或数据库操作失败
"""


@router.put("/{role_id}")
async def update_role(role_id: int, name: str, description: str, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    role.set_name(name)
    role.set_description(description)

    try:
        db.commit()
        db.refresh(role)
        return {"message": "Role updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


"""
删除角色

Args:
    role_id (int): 角色ID
    db (Session): 数据库会话

Returns:
    dict: 包含成功消息的字典

Raises:
    HTTPException: 如果角色不存在、不可删除或数据库操作失败
"""


@router.delete("/{role_id}")
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if not role.is_deletable:
        raise HTTPException(status_code=400, detail="Role cannot be deleted")

    try:
        db.delete(role)
        db.commit()
        return {"message": "Role deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


"""
获取所有模块信息

Args:
    db (Session): 数据库会话

Returns:
    list: 包含所有主模块及其对应子模块的列表，每个主模块包含以下字段：
        - id (int): 主模块ID
        - name (str): 主模块名称
        - secondary_modules (list): 子模块列表，每个子模块包含：
            - id (int): 子模块ID
            - name (str): 子模块名称

Raises:
    HTTPException: 如果数据库操作失败
"""


@router.get("/modules")
async def get_all_modules(db: Session = Depends(get_db)):
    primary_modules = db.query(PrimaryModule).all()
    result = []
    for primary_module in primary_modules:
        secondary_modules = db.query(SecondaryModule).filter(
            SecondaryModule.primary_module_id == primary_module.id).all()
        module_data = {
            "id": primary_module.id,
            "name": primary_module.name,
            "secondary_modules": [
                {
                    "id": secondary_module.id,
                    "name": secondary_module.name,
                } for secondary_module in secondary_modules
            ]
        }
        result.append(module_data)
    print(result)
    return result
