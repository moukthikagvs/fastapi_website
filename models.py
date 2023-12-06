from sqlalchemy import Column, String, Integer, Boolean, Enum, Text
from sqlalchemy.types import Enum as SQLAlchemyEnum  
from schema import Roles
from connection import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, unique=False, index=True)
    is_active = Column(Boolean, server_default="false") 
    role = Column(SQLAlchemyEnum(Roles), default="user")

class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, index=True)
