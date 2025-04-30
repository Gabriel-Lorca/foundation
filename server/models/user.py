from sqlalchemy import Column, Integer, String
from .base import Base
from passlib.context import CryptContext


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def set_password(self, password):
        self.password_hash = self.pwd_context.hash(password)

    def verify_password(self, password):
        return self.pwd_context.verify(password, self.password_hash)
