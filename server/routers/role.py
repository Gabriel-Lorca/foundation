from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.dependencies import get_db
from server.schemas.role import RoleCreate, RoleUpdate
from server.models import Role, PrimaryModule, SecondaryModule, RoleModule

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/all")
async def get_all_role(db: Session = Depends(get_db)):
    """
    查询所有角色名称,以列表形式返回
    :param db:
    :return:
    """
    roles = db.query(Role).filter(Role.is_deleted == False).all()
    return [role.name for role in roles]


@router.get("/role_data")
async def all_role(db: Session = Depends(get_db)):
    """
    查询所有角色信息,以列表形式返回
    :param db:
    :return:
    """
    roles = db.query(Role).all()
    return roles


@router.post("/add_role")
async def add_role(role: RoleCreate, db: Session = Depends(get_db)):
    """
    添加新角色
    :param role:
    :param db:
    :return:
    """
    db_role = Role(name=role.name, description=role.description, is_deleted=False, is_deletable=True)
    try:
        # 添加角色信息,并获取添加后的大数据
        db.add(db_role)
        db.commit()
        db.refresh(db_role)

        # 向角色权限对应表中,写入该角色的权限
        for mode_id in role.permission:
            if '-' in mode_id:
                db_roleModule = RoleModule(role_id=db_role.id, primary_module_id=int(mode_id.split('-')[0]),
                                           secondary_module_id=int(mode_id.split('-')[1]))
                db.add(db_roleModule)
                db.commit()
            else:
                second_module_list = (db.query(SecondaryModule).
                                      filter(SecondaryModule.primary_module_id == int(mode_id)).all())
                for s_mode in second_module_list:
                    db_roleModule = RoleModule(role_id=db_role.id, primary_module_id=int(mode_id),
                                               secondary_module_id = s_mode.id)
                    db.add(db_roleModule)
                    db.commit()

        return {"message": "Role created successfully", "role_id": db_role.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_all_permission_data")
async def get_all_permission_data(db: Session = Depends(get_db)):
    modules = []

    # 查询所有一级模块列表
    primary_modules = db.query(PrimaryModule).all()
    for p_module in primary_modules:
        first_module = {"id": p_module.id, "name": p_module.name, "children": []}
        secondary_modules = db.query(SecondaryModule).filter(SecondaryModule.primary_module_id == p_module.id).all()
        for s_module in secondary_modules:
            second_module = {"id": s_module.id, "name": s_module.name, "primary_module_id": p_module.id}
            first_module["children"].append(second_module)
        modules.append(first_module)

    return modules


@router.post("/del/{role_id}")
async def del_role(role_id: int, db: Session = Depends(get_db)):
    """
    通过修改删除标记,实现软删除角色
    :param role_id:
    :param db:
    :return:
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None or not role.is_deletable:
        raise HTTPException(status_code=404, detail="Role not found")
    else:
        if role.is_deleted:
            role.set_is_deleted(False)
        else:
            role.set_is_deleted(True)
        db.commit()
        return {"message": "User deleted successfully", "role_name": role.name}


@router.post("/update/{role_id}")
async def update_role(role_id: int,up_data: RoleUpdate,db: Session = Depends(get_db)):

    try:
        db_role = db.query(Role).filter(Role.id == role_id).first()
        if db_role is None or not db_role.is_deletable:
            raise HTTPException(status_code=404, detail="Role not found")
        else:
            # 更新角色表数据
            db_role.name = up_data.name
            db_role.description = up_data.description
            db.commit()
            db.refresh(db_role)

            # 删除原本角色-权限关系表数据
            db.query(RoleModule).filter(RoleModule.role_id == db_role.id).delete()
            db.commit()

            # 建立新的角色-权限关系
            for mode_id in up_data.permission:
                if '-' in mode_id:
                    db_roleModule = RoleModule(role_id=db_role.id, primary_module_id=int(mode_id.split('-')[0]),
                                               secondary_module_id=int(mode_id.split('-')[1]))
                    db.add(db_roleModule)
                    db.commit()
                else:
                    second_module_list = (db.query(SecondaryModule).
                                          filter(SecondaryModule.primary_module_id == int(mode_id)).all())
                    for s_mode in second_module_list:
                        db_roleModule = RoleModule(role_id=db_role.id,primary_module_id=int(mode_id),
                                                   secondary_module_id=s_mode.id)
                        db.add(db_roleModule)
                        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "User updated successfully", "role_id": role_id}