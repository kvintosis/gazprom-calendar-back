from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import select
from passlib.hash import pbkdf2_sha256
import sqlalchemy.exc
from model.Event import Event
from model.User import User
from model.tables import Employee


class AsyncSQLController:
    def __init__(self, address: str):
        try:
            self.__engine = create_async_engine(address, echo=True)
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

    async def login(self, login: str, password: str):
        async with self.async_session() as session:
            # Проверка существования пользователя
            user = await session.execute(select(Employee).where(Employee.email == login))
            db_user = user.scalar()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            if not pbkdf2_sha256.verify(password, db_user.password_hash):
                raise HTTPException(status_code=401, detail="Invalid password")
            return True

    async def create_event(self, event: Event):
        async with self.async_session() as session:
            session.add(event)
            await session.commit()

    async def get_all_events(self):
        async with self.async_session() as session:
            result = await session.execute(select(Event))
            return result.scalars().all()