from django.urls import path

from .views import cadastro_paciente, inclusao_paciente, paciente


urlpatterns = [
    path('paciente/', paciente, name="paciente"),
    path('cadastro/', cadastro_paciente, name="cadastro_paciente"),
    path('inserir/', inclusao_paciente, name="inserir_paciente")
]