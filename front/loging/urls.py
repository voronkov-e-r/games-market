from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.registration, name='regs'),
    path('', views.index, name='login'),
    path('forgot-password', views.forgot_password, name='forgot-pass')
]