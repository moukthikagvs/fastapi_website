from datetime import date
from pydantic import BaseModel, EmailStr, Field  
from enum import Enum
from fastapi import Form

class UserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

    class Config:
        alias_generator = lambda string: string  
class Roles(str, Enum):
    USER = "user"
    ADMIN = "admin"
