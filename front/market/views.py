from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import kafka_manager
import uuid

def str_to_list(list_str:str) -> list:
    list_str = list_str.replace('[', '')
    list_str = list_str.replace(']', '')

    if list_str == '':
        return []

    new_list = list_str.split(',')
    new_list = [int(i) for i in new_list]

    return new_list


def index(request):
    if not request.COOKIES.get('is_reged'):
        return HttpResponseRedirect('/')

    context = {}

    if request.method == 'POST':
        game_name = request.POST.get('game_name')
        game_price = float(request.POST.get('game_price').replace(',','.'))
        game_id = int(request.POST.get('game_id'))
        user_id = request.COOKIES.get('id')
        idemp_key = str(uuid.uuid4())

        result = kafka_manager.kafka_feedback('buygame', {'user_id':user_id, 'value':game_price, 'payment_id':game_name, 'idempotence_key':idemp_key})

        if not result.get('result'):
            context['error'] = result['detail']
        else:
            temp_lib_str = request.COOKIES.get('library')
            temp_lib = str_to_list(temp_lib_str)
            temp_lib.append(game_id)
            response = HttpResponseRedirect('/market')
            new_balance = float(request.COOKIES.get('balance')) - game_price
            response.set_cookie('balance', new_balance, 600)
            response.set_cookie('library', temp_lib, 600)
            return response

    user = User(request.COOKIES.get('name'), request.COOKIES.get('balance'))
    games_serial = kafka_manager.kafka_feedback('getgames', {})
    games = [Game(**data) for data in games_serial.get('result', 1234)]

    available_games = []
    user_lib_id_str = request.COOKIES.get('library')
    user_lib_id = str_to_list(user_lib_id_str)

    for game in games:
        if game.id not in user_lib_id:
            available_games.append(game)

    context['games'] = available_games
    context['user'] = user

    return render(request, 'main_market.html', context)


def library(request):
    if not request.COOKIES.get('is_reged'):
        return HttpResponseRedirect('/')

    user = User(request.COOKIES.get('name'), request.COOKIES.get('balance'))
    user_lib_id_str = request.COOKIES.get('library')
    user_lib_id = str_to_list(user_lib_id_str)

    games_serial = kafka_manager.kafka_feedback('getgames', {})
    games = [Game(**data) for data in games_serial.get('result', 1234)]

    user_lib_games = []
    for game in games:
        if game.id in user_lib_id:
            user_lib_games.append(game)

    return render(request, 'library.html', {'user':user, 'library_games':user_lib_games})


def topup(request):
    if not request.COOKIES.get('is_reged'):
        return HttpResponseRedirect('/')

    user = User(request.COOKIES.get('name'), request.COOKIES.get('balance'))

    if request.method == 'POST':
        payment_value = int(request.POST.get('amount'))
        idemp_key = str(uuid.uuid4())

        result = kafka_manager.kafka_feedback('pupbalance', {'user_id':request.COOKIES.get('id'), 'value':payment_value, 'payment_id':'pup', 'idempotence_key':idemp_key})

        if not result.get('result'):
            detail = result['detail']
            return render(request, 'topup.html', {'user':user, 'error':detail})

        response = HttpResponseRedirect('/market')
        new_balance = float(request.COOKIES.get('balance')) + payment_value
        response.set_cookie('balance', new_balance, 600)
        return response


    return render(request, 'topup.html', {'user':user})




class Game:
    def __init__(self, name:str, price:int, id:int):
        self.name = name
        self.price = price
        self.id = id

class User:
    def __init__(self, name:str, balance:float):
        self.name = name
        self.balance = balance