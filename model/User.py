from pydantic import BaseModel
class User(BaseModel):
    password = ''
    login = ''
    first_name = ''
    last_name = ''
    email = ''
    skills = []
    interests = []
    role = ''
    position = ''
