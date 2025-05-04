from django.urls import path
from . import views

urlpatterns = [
    path('recepcionista/', views.pagina_recepcao, name='pagina_recepcionista'),
    path('confirmar-agendamento/', views.confirmar_agendamento, name='confirmar_agendamento'),
    path('administrador/', views.pagina_administrador, name='pagina_administrador'),
    path('cadastrar-funcionario/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('funcionarios/', views.lista_funcionarios, name='lista_funcionarios'),
    path('relatorio-logins/', views.relatorio_logins, name='relatorio_logins'),
    path('cadastrar-guiche/', views.cadastrar_guiche, name='cadastrar_guiche'),
]