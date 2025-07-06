from django.urls import path
from Avaliacao.views import avaliacao_atendimento, listar_avaliacoes


urlpatterns = [

    path('', listar_avaliacoes, name="avaliacao"),
    path('avaliacao_atendimento', avaliacao_atendimento, name="avaliacao_atendimento")
]