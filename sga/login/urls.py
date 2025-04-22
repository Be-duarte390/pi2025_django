from django.urls import path
from . import views

urlpatterns = [
    path('<str:funcao>/', views.login_funcao, name='login_funcao'),
]