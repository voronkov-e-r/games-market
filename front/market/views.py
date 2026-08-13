from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import kafka_manager

def index(request):
    if not request.COOKIES.get('is_reged'):
        return HttpResponseRedirect('/')

    user = User(request.COOKIES.get('name'), request.COOKIES.get('balance'))
    games_serial = kafka_manager.kafka_feedback('getgames', {})
    games = [Game(**data) for data in games_serial.get('result', 1234)]

    return render(request, 'main_market.html', {'games':games, 'user':user})


def library(request):
    if not request.COOKIES.get('is_reged'):
        return HttpResponseRedirect('/')

    user = User(request.COOKIES.get('name'), request.COOKIES.get('balance'))

    return render(request, 'library.html', {'user':user, 'library_games':[]})


def topup(request):
    if not request.COOKIES.get('is_reged'):
        return HttpResponseRedirect('/')

    user = User(request.COOKIES.get('name'), request.COOKIES.get('balance'))

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