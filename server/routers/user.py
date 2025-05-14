from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.schemas.user import UserCreate
from server.models.user import User
from server.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print(user)
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
