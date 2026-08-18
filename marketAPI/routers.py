from typing import Annotated

from fastapi import APIRouter, Depends

from repository import UsersRepository, GamesRepository, PaymentRepository
from schemas import SUserAdd, SCheckUser, SGameAdd, SPaymentAdd


user_router = APIRouter(prefix='/user', tags=['Users'])
game_router = APIRouter(prefix='/game', tags=['Games'])
payment_router = APIRouter(prefix='/pay', tags=['Payment'])


@user_router.post('/addUser', tags=[])
async def add_user(user: Annotated[SUserAdd, Depends()]):
    user = await UsersRepository.create_one(user)
    return {'ok':True, 'id':user}

@user_router.delete('/deleteUser')
async def delete_user(user_id:int):
    result = await UsersRepository.delete_one(user_id)
    return {'ok':True, 'result':result}

@user_router.get('/checkReg')
async def check_registration(user: Annotated[SCheckUser, Depends()]):
    result = await UsersRepository.check_registration(user.mail, user.password)
    return {'ok':True, 'result':result}

@user_router.get('/getUserData')
async def get_user_data(user: Annotated[SCheckUser, Depends()]):
    result = await UsersRepository.get_user_data(user)
    return {'ok':True, 'name':result['name'], 'balance':result['balance'], 'id':result['id'], 'library':result['library']}

@game_router.post('/addGame')
async def add_game(game: Annotated[SGameAdd, Depends()]):
    result = await GamesRepository.add_one(game)
    return {'ok':True, 'result':result}

@game_router.get('/getGames')
async def get_games():
    result = await GamesRepository.get_all()
    return {'ok':True, 'result':result}

@payment_router.post('/buyGame')
async def buy_one_game(pay: Annotated[SPaymentAdd, Depends()]):
    result = await PaymentRepository.buy_one_game(pay)
    return {'ok':True, 'result':result}

@payment_router.post('/pupBalance')
async def pup_balance(pay: Annotated[SPaymentAdd, Depends()]):
    result = await PaymentRepository.topup_balance(pay)
    return {'ok':True, 'result':result}