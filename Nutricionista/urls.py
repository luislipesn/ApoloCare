from django.urls import path

from .views import (
    cadastro_nutricionista,
    excluir_nutricionista,
    inclusao_nutricionista,
    nutricionista,
)

urlpatterns = [
    path("nutricionista/", nutricionista, name="nutricionista"),
    path("cadastro_nutricionista/", cadastro_nutricionista, name="cadastro_nutricionista"),
    path("cadastro_nutricionista/<int:id>/", cadastro_nutricionista, name="editar_nutricionista"),
    path("inserir_nutricionista/", inclusao_nutricionista, name="inclusao_nutricionista"),
    path("deletar_nutricionista/", excluir_nutricionista, name="deletar_nutricionista"),
]
