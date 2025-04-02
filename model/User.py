from pydantic import BaseModel, EmailStr


class User(BaseModel):
    password: str
    login: str
    first_name: str
    last_name: str
    email: EmailStr
    skills: list[str]
    interests: list[str]
    role: str
    position: str
