from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)  # Храним дату в формате 'YYYY-MM-DD'
    position = Column(String, nullable=False)
    department = Column(String, nullable=True)
    skills = Column(Text, nullable=True)  # Список навыков через запятую
    interests = Column(Text, nullable=True)  # Список интересов через запятую
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(Text, nullable=False)
    role = Column(String, default='user', nullable=False)  # Значение по умолчанию 'user'
