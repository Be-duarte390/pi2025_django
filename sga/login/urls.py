from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_funcionario, name='login_funcionario'),
]