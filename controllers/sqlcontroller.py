import sqlalchemy
import bcrypt
from model.Event import Event
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

    def create_event(self, event: Event):
        with Session(self._engine) as session:
            event= self._base.classes.event
            session.add(event(title=event.title,
                              description=event.description,
                              start_time=event.start_time,
                              end_time=event.end_time,
                              type=event.type,
                              organizer_id=event.organizer_id))
            session.commit()

    def update_event(self, event_id: int, updated_event: Event):
        with Session(self._engine) as session:
            event_table = self._base.classes.event
            event = session.query(event_table).filter_by(id=event_id).first()

            if event:
                event.title = updated_event.title
                event.description = updated_event.description
                event.start_time = updated_event.start_time
                event.end_time = updated_event.end_time
                event.type = updated_event.type
                event.organizer_id = updated_event.organizer_id

                session.commit()
                return True
            else:
                return False

    def delete_event(self, event_id: int):
        with Session(self._engine) as session:
            event_table = self._base.classes.event

            # Находим событие по ID
            event = session.query(event_table).filter_by(id=event_id).first()
            if not event:
                return False  # Если событие не найдено, возвращаем False

            session.delete(event)  # Удаляем событие
            session.commit()  # Подтверждаем изменения
            return True  # Возвращаем True, если удаление прошло успешно

    def get_all_events(self):
        with Session(self._engine) as session:
            event_table = self._base.classes.event

            events = session.query(event_table).all()

            return [
                {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "start_time": str(event.start_time),
                    "end_time": str(event.end_time),
                    "type": event.type,
                    "organizer_id": event.organizer_id,
                }
                for event in events
            ]
