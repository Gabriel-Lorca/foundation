from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import User, RoleModule, Role

router = APIRouter()

# JWT配置
SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# 创建JWT令牌
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({
        "exp": expire,
        "role_name": data.get("role_name"),
        "role_id": data.get("role_id"),
        "primary_modules": data.get("primary_modules", []),
        "secondary_modules": data.get("secondary_modules", [])
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 用户认证
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 通过role_modules表查询角色权限信息
    role = db.query(Role).filter(Role.id == user.role_id).first()

    role_modules = db.query(RoleModule).filter(RoleModule.role_id == user.role_id).all()
    primary_modules = list(set([rm.primary_module_id for rm in role_modules]))
    secondary_modules = list(set([rm.secondary_module_id for rm in role_modules]))

    access_token = create_access_token(
        data={
            "sub": user.username,
            "role_name": role.name,
            "role_id": role.id,
            "primary_modules": primary_modules,
            "secondary_modules": secondary_modules
        }, expires_delta=access_token_expires
    )
    data = {
        "access_token": access_token,
        "token_type": "bearer"
    }
    return data
