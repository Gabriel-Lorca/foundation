from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.models import Role, PrimaryModule, SecondaryModule, RoleModule, User
from server.dependencies import get_db, get_current_user

router = APIRouter(prefix="/menu", tags=["roles"])


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
