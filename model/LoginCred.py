from pydantic import BaseModel, EmailStr
class LoginCred(BaseModel):
    login: EmailStr
    password:str
