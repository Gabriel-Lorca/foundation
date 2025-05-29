from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    phone_num: str
    role_name: str
    username: str
    password_hash: str


class UserUpdate(BaseModel):
    name: str
    phone_num: str
    role_name: str


class User(BaseModel):
    id: int
    username: str
