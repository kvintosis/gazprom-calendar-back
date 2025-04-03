from enum import Enum
from pydantic import BaseModel, EmailStr

class UserType(str, Enum):
    user = "user" # Работник
    admin = "admin" # Доступ к админпанели
class User(BaseModel):
    password_hash: str
    first_name: str
    last_name: str
    email: EmailStr
    birth_date: str
    skills: str
    interests: str
    role: UserType
    department: str
    position: str
