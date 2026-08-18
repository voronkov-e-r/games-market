from django.shortcuts import render
from . import kafka_manager
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect

@csrf_protect
def index(request):
    if request.COOKIES.get('is_reged'):
        return HttpResponseRedirect('/market')

    result = {}
    if request.method == 'POST':
        mail = request.POST.get('email')
        password = request.POST.get('password')

        result = kafka_manager.kafka_feedback('checkreg', {'mail':mail, 'password':password})

        if result['result']:
            max_age = 600
            response = HttpResponseRedirect('/market')
            response.set_cookie('is_reged', True, max_age)

            user_data = kafka_manager.kafka_feedback('getuser', {'mail':mail, 'password':password})
            response.set_cookie('name', user_data['name'], max_age)
            response.set_cookie('balance', user_data['balance'], max_age)
            response.set_cookie('id', user_data['id'], max_age)

            return response

    return render(request,'login.html', context=result)


@csrf_protect
def registration(request):
    if request.COOKIES.get('is_reged'):
        return HttpResponseRedirect('/market')

    context = {}
    if request.method == 'POST':
        name = request.POST.get('username')
        mail = request.POST.get('email')
        password = request.POST.get('password')
        pass_conf = request.POST.get('confirm')

        if password == pass_conf:
            result = kafka_manager.kafka_feedback('adduser', {'name':name, 'mail':mail, 'password':password})

            if result.get('id'):
                return HttpResponseRedirect('/')
            else:
                context['detail'] = result['detail']

        else:
            context['detail'] = 'Пароли не совпадают'

    return render(request, 'reg.html', context=context)

def forgot_password(request):
    if request.COOKIES.get('is_reged'):
        return HttpResponseRedirect('/market')
    # заглушка
    return render(request, 'forgot_password.html')
