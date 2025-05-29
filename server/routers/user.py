from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.models import Role
from server.schemas.user import UserCreate
from server.models.user import User
from server.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username)
    db_user.set_password(user.password)
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
    users = db.query(User).all()
    return users

@router.post("/del/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or user.id == 1:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        if user.is_deleted:
            user.set_is_deleted(False)
        else:
            user.set_is_deleted(True)
        db.commit()
        return {"message": "User deleted successfully", "user_id": user_id}

