from typing import Annotated

from django.db.models.expressions import result
from fastapi import APIRouter, Depends

from repository import UsersRepository, GamesRepository
from schemas import SUserAdd, SCheckUser, SGameAdd


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
    return {'ok':True, 'name':result['name'], 'balance':result['balance']}

@game_router.post('/addGame')
async def add_game(game: Annotated[SGameAdd, Depends()]):
    result = await GamesRepository.add_one(game)
    return {'ok':True, 'result':result}

@game_router.get('/getGames')
async def get_games():
    result = await GamesRepository.get_all()
    return {'ok':True, 'result':result}