from django.urls import path

from .views import cadastro_usuario, inclusao_usuario, logout_view, validaLogin


urlpatterns = [
    path('valida-login/', validaLogin, name='valida_login'),
    path('logout/', logout_view, name='logout'),
    path('cadastro/', cadastro_usuario, name='cadastro_usuario'),
    path('inclusao_usuario/', inclusao_usuario, name='inserir-usuario'),
]