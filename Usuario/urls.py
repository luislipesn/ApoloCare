from django.urls import path

from .views import alterar_status, cadastro_usuario, inclusao_usuario, listar_usuarios, logout_view, validaLogin


urlpatterns = [
    path('', listar_usuarios, name="usuario"),
    path('valida-login/', validaLogin, name='valida_login'),
    path('logout/', logout_view, name='logout'),
    path('cadastro/', cadastro_usuario, name='cadastro_usuario'),
    path('inclusao_usuario/', inclusao_usuario, name='inserir-usuario'),
    path('alterar_status/', alterar_status, name='alterar_status')
]