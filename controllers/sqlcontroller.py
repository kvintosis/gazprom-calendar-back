from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select, inspect
from passlib.hash import pbkdf2_sha256
import sqlalchemy.exc
from model.Dto_Event import Dto_Event
from model.User import User
from model.tables import Employee, Event


class AsyncSQLController:
    def __init__(self, address: str):
        try:
            self.__engine = create_async_engine(address)
        except sqlalchemy.exc.OperationalError:
            pass
        self.async_session = async_sessionmaker(self.__engine, expire_on_commit=False)

    async def create_user(self, user: User):
        async with self.async_session() as session:
            new_user = Employee(
                first_name=user.first_name,
                last_name=user.last_name,
                birth_date=user.birth_date,
                position=user.position,
                department=user.department,
                skills=user.skills,
                interests=user.interests,
                email=user.email,
                password_hash=pbkdf2_sha256.hash(user.password_hash),
                role=user.role
            )
            session.add(new_user)
            await session.commit()
    async def get_role(self, login: str) -> str:
        """Получение роли user/admin у работника"""
        async with self.async_session() as session:
            role = await session.execute(select(Employee.role).where(Employee.email == login))
            role = role.scalar()
            if role is None:
                raise HTTPException(status_code=404)
            return role
    async def login(self, login: str, password: str):
        async with self.async_session() as session:
            user = await session.execute(select(Employee).where(Employee.email == login))
            db_user = user.scalar()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            if not pbkdf2_sha256.verify(password, db_user.password_hash):
                raise HTTPException(status_code=400, detail="Invalid password")
            return True

    async def get_all_employers(self):
        async with self.async_session() as session:
            columns = [c for c in inspect(Employee).c if
                       c.name != "password_hash" and c.name != "role" and c.name != "id"]
            result = await session.execute(select(*columns).order_by(Employee.first_name, Employee.last_name))
            data = [dict(zip([column.name for column in columns], row)) for row in result.all()]
            return data

    async def create_event(self, event: Dto_Event):
        async with self.async_session() as session:
            new_event = Event(**event.model_dump())
            print(new_event)
            session.add(new_event)
            await session.commit()

    async def get_all_events(self):
        async with self.async_session() as session:
            columns = [c for c in inspect(Event).c if
                       c.name != "id" and c.name != "organizer_id"]
            result = await session.execute(select(*columns))
            data = [dict(zip([column.name for column in columns], row)) for row in result.all()]
            return data
