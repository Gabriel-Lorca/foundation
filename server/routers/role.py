from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.models import Role
from server.dependencies import get_db

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/all")
async def get_all_role(db: Session = Depends(get_db)):
    """
    查询所有角色名称,以列表形式返回
    :param db:
    :return:
    """
    print("Role")
    roles = db.query(Role).filter(Role.is_deleted == False).all()
    return [role.name for role in roles]
