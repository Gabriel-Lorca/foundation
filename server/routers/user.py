from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.models import Role
from server.schemas.user import UserCreate, UserUpdate
from server.models.user import User
from server.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/add_user")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    新增用户接口
    :param user:
    :param db:
    :return:
    """
    db_user = User(name=user.name, phone_num=user.phone_num, username=user.username,
                   role_name=user.role_name,is_deleted=False,s_deletable=True)
    db_user.set_password(user.password_hash)
    db_user.set_role_id(db.query(Role).filter_by(name=user.role_name).first().id)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User created successfully", "user_id": db_user.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all")
async def get_all_users(db: Session = Depends(get_db)):
    """
    获取用户列表接口
    :param db:
    :return:
    """
    users = db.query(User).all()
    return users

@router.post("/del/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    软删除指定用户接口
    :param user_id:
    :param db:
    :return:
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.s_deletable:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        if user.is_deleted:
            user.set_is_deleted(False)
        else:
            user.set_is_deleted(True)
        db.commit()
        return {"message": "User deleted successfully", "user_id": user_id}

@router.post("/update/{user_id}")
async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """
    编辑用户接口
    :param user_id:
    :param user:
    :param db:
    :return:
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or user.id == 1:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        if user.is_deleted:
            raise HTTPException(status_code=404, detail="User is deleted")
        else:
            user.set_name(user_data.name)
            user.set_phone_num(user_data.phone_num)
            user.set_role_name(user_data.role_name)
            user.set_role_id(db.query(Role).filter_by(name=user_data.role_name).first().id)
            db.commit()
            db.refresh(user)
            return {"message": "User update successfully", "user_id": user.id}