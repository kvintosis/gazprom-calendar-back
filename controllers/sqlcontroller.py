import sqlalchemy
import bcrypt
from model.User import User
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class SQLController:
    _base = None
    _engine = None

    def __init__(self, address):
        try:
            self._engine = create_engine(address, echo=True)
            self._base = automap_base()
            self._base.prepare(autoload_with=self._engine, reflect=True)
        except sqlalchemy.exc.OperationalError:
            pass

    def create_user(self, user: User):
        with Session(self._engine) as session:
            salt = bcrypt.gensalt()
            user.password = str(bcrypt.hashpw(user.password.encode("utf-8"), salt))
            employees = self._base.classes.employees
            session.add(employees(first_name=user.first_name,
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
