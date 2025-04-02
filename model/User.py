from pydantic import BaseModel, EmailStr


class User(BaseModel):
    password_hash: str
    first_name: str
    last_name: str
    email: EmailStr
    birth_date: str
    skills: str
    interests: str
    role: str
    department: str
    position: str
