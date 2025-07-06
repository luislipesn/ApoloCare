from django.urls import path
from .views import cadastro_consulta, consulta, deletar_consulta, incluir_consulta


urlpatterns = [
    path('', consulta, name="consulta"),
    path('cadastro/', cadastro_consulta, name="cadastro_consulta"),
    path('incluir_consulta/', incluir_consulta, name="incluir_consulta"),
    path('deletar_consulta/', deletar_consulta, name="deletar_consulta")
]