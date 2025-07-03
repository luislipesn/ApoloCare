from django.urls import path
from .views import cadastro_consulta


urlpatterns = [
    path('cadastro/', cadastro_consulta, name="cadastro_consulta")
]