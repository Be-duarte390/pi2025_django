from django.urls import path
from . import views

urlpatterns = [
    path('guiche/', views.pagina_guiche, name='pagina_guiche'),
    path('guiche/<int:guiche_numero>/atendimento/', views.atendimento_guiche, name='atendimento_guiche'),
    path('painel-tv1/', views.painel_tv1, name='painel_tv1'),
    path('painel/ultima_senha/', views.ultima_senha_chamada, name='ultima_senha_chamada'),
]