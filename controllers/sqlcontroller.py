from model.LoginCred import LoginCred
import sqlalchemy
from sqlalchemy import select
from passlib.hash import pbkdf2_sha256
from model.User import User
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class SQLController:
    _base = None
    _engine = None
    _employees = None
    def __init__(self, address):
        try:
            self._engine = create_engine(address, echo=True)
            self._base = automap_base()
            self._base.prepare(autoload_with=self._engine, reflect=True)
            self._employees = self._base.classes.employees
        except sqlalchemy.exc.OperationalError:
            pass

    def create_user(self, user: User):
        with Session(self._engine) as session:
            user.password = pbkdf2_sha256.hash(user.password)
            session.add(self._employees(first_name=user.first_name,
                        last_name=user.last_name,
                        birth_date=user.birth_date,
                        position=user.position,
                        department=user.department,
                        skills=user.skills,
                        interests=user.interests,
                        email=user.email,
                        password_hash=user.password,
                        role=user.role))
            session.commit()

    def login(self, login_credentials: LoginCred):
        with Session(self._engine) as session:
            db_user = session.execute(
                select(self._employees)
                .where(self._employees.email == login_credentials.login)).scalar()
            if pbkdf2_sha256.verify(login_credentials.password, db_user.password_hash):
                return True
            else:
                raise ValueError("Invalid password")
