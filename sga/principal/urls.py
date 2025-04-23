from django.urls import path
from . import views

urlpatterns = [
    path('recepcionista/', views.pagina_recepcao, name='pagina_recepcionista'),
    path('confirmar-agendamento/', views.confirmar_agendamento, name='confirmar_agendamento'),
    path('cadastrar-funcionario/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('administrador/', views.pagina_administrador, name='pagina_administrador'),
    path('cadastrar-funcionario/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
]