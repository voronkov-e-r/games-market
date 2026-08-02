from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='market'),
    path('library', views.library, name='library'),
    path('topup', views.topup, name='tupup')
]