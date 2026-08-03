from django.db.models.expressions import result
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from database import UsersORM, GamesORM
from schemas import SUserAdd, SCheckUser, SGameAdd, SGame
from database import new_session
from sqlalchemy import select


class UsersRepository:
    @classmethod
    async def create_one(cls, data:SUserAdd) -> int:
        async with new_session() as session:
            try:
                user_dict = data.model_dump()

                user = UsersORM(**user_dict)
                session.add(user)

                await session.flush()
                await session.commit()
                return user.id

            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(status_code=409,detail='Пользователь с такой почтой уже существует')

    @classmethod
    async def delete_one(cls, user_id:int) -> bool:
        async with new_session() as session:
            query = select(UsersORM).where(UsersORM.id == user_id)

            result = await session.execute(query)
            user_model = result.scalar_one_or_none()

            if not user_model:
                return False

            await session.delete(user_model)
            await session.commit()
            return True

    @classmethod
    async def check_registration(cls, mail:EmailStr, password:str) -> bool:
        async with new_session() as session:
            query = select(UsersORM).where(UsersORM.mail == mail, UsersORM.password == password)

            result = await session.execute(query)
            user_model = result.scalar_one_or_none()

            if not user_model:
                return False

            return True

    @classmethod
    async def get_user_data(cls, data:SCheckUser) -> dict:
        async with new_session() as session:
            query = select(UsersORM).where(UsersORM.mail == data.mail, UsersORM.password == data.password)

            result = await session.execute(query)
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(404, detail='Пользователь не найден')

            return {'name':user.name, 'balance':user.balance}



class GamesRepository:
    @classmethod
    async def add_one(cls, data:SGameAdd) -> int:
        async with new_session() as session:
            data_dict = data.model_dump()

            game = GamesORM(**data_dict)
            session.add(game)

            await session.flush()
            await session.commit()

            return game.id

    @classmethod
    async def get_all(cls) -> list[SGame]:
        async with new_session() as session:
            query = select(GamesORM)

            res = await session.execute(query)
            game_models = res.scalars().all()
            games = [SGame.model_validate(game) for game in game_models]

            return games