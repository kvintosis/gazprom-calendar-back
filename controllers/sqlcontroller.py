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
            self._engine = create_engine('sqlite:///../databases/employees.sqlite', echo=True)
            self._base = automap_base()
            self._base.prepare(autoload_with=self._engine)
        except sqlalchemy.exc.OperationalError:
            pass

    def create_user(self, user: User):
        with Session(self._engine) as session:
            salt = bcrypt.gensalt()
            user.password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
            session.add(user)
            session.commit()
