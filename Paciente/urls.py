from django.urls import path

from .views import cadastro_paciente, exclusao_paciente, inclusao_paciente, paciente


urlpatterns = [
    path('paciente/', paciente, name="paciente"),
    path('cadastro/', cadastro_paciente, name="cadastro_paciente"),
    path('inserir/', inclusao_paciente, name="inserir_paciente"),
    path('excluir/', exclusao_paciente, name="excluir_paciente"),
    path('editar/', cadastro_paciente, name="editar_paciente")
]