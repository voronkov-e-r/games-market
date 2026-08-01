from django.shortcuts import render

def index(request):
    return render(request, 'main_market.html', {'games':[Game('Team workers 2', 800) for i in range(10)], 'user':User('Анатолий',1286.31)})

# Пока что имитация получения каких-то данных
class Game:
    def __init__(self, name:str, price:int):
        self.name = name
        self.price = price

class User:
    def __init__(self, name:str, balance:float):
        self.name = name
        self.balance = balance