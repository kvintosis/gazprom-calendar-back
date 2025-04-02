from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)  # ISO8601: 'YYYY-MM-DD'
    position = Column(String, nullable=False)
    department = Column(String)
    skills = Column(String)  # Список навыков через запятую
    interests = Column(String)  # Интересы через запятую
    email = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String, default='user')  # Простые роли: admin/user


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, nullable=False)  # ISO8601: 'YYYY-MM-DD HH:MM'
    end_time = Column(DateTime, nullable=False)
    type = Column(String, CheckConstraint("type IN ('meeting', 'birthday', 'other')"))
    organizer_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"))


class EventParticipant(Base):
    __tablename__ = "event_participants"

    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), primary_key=True)
    status = Column(String, default='invited')


class Schedule(Base):
    __tablename__ = "schedule"

    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
