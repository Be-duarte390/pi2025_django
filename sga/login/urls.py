from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_funcionario, name='login_funcionario'),
    path('escolher-funcao/', views.escolher_funcao, name='escolher_funcao'),
    path('logout/', views.logout_funcionario, name='logout'),
]