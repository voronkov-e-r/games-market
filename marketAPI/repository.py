from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from database import UsersORM, GamesORM, PaymentORM
from schemas import SUserAdd, SCheckUser, SGameAdd, SGame, SPaymentAdd
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

            return {'name':user.name, 'balance':user.balance, 'id':user.id}



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


class PaymentRepository:
    @classmethod
    async def buy_one_game(cls, data:SPaymentAdd) -> int:
        async with new_session() as session:
            if data.value <= 0:
                raise HTTPException(400, detail='Некорректная сумма платежа')

            query = select(PaymentORM).where(PaymentORM.payment_id == data.payment_id, PaymentORM.user_id == data.user_id, PaymentORM.value == data.value, PaymentORM.idempotence_key == data.idempotence_key)

            res = await session.execute(query)
            pay_model = res.scalar_one_or_none()

            if pay_model:
                raise HTTPException(208, detail='Платеж уже обрабатывается')

            query = select(UsersORM).where(UsersORM.id == data.user_id)
            res = await session.execute(query)
            res_model = res.scalar_one_or_none()

            if not res_model:
                raise HTTPException(404, detail='Пользователь не найден')

            if res_model.balance < data.value:
                raise HTTPException(400, detail='Недостаточно средств')

            res_model.balance -= data.value

            data_dict = data.model_dump()
            data_dict['status'] = 'completed'
            pay = PaymentORM(**data_dict)
            session.add(pay)

            await session.flush()
            await session.commit()

            return pay.id


    @classmethod
    async def topup_balance(cls, data:SPaymentAdd) -> int:
        async with new_session() as session:
            if data.value <= 0:
                raise HTTPException(400, detail='Некорректная сумма платежа')

            query = select(PaymentORM).where(PaymentORM.payment_id == data.payment_id,
                                             PaymentORM.user_id == data.user_id, PaymentORM.value == data.value,
                                             PaymentORM.idempotence_key == data.idempotence_key, PaymentORM.status == 'processing')

            res = await session.execute(query)
            pay_model = res.scalar_one_or_none()

            if pay_model:
                raise HTTPException(208, detail='Платеж уже обрабатывается')

            query = select(UsersORM).where(UsersORM.id == data.user_id)
            res = await session.execute(query)
            res_model = res.scalar_one_or_none()

            if not res_model:
                raise HTTPException(404, detail='Пользователь не найден')

            res_model.balance += data.value

            data_dict = data.model_dump()
            data_dict['status'] = 'completed'
            pay = PaymentORM(**data_dict)
            session.add(pay)

            await session.flush()
            await session.commit()

            return pay.id