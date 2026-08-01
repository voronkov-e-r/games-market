from django.shortcuts import render

def index(request):
    return render(request,'login.html')

def registration(request):
    return render(request, 'reg.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')
