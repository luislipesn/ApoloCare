"""
URL configuration for ApoloCare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views

from Paciente.views import paciente
from Nutricionista.views import cadastro_nutricionista, excluir_nutricionista, inclusao_nutricionista, nutricionista
from .views import cadastro_usuario, inclusao_usuario, logout_view, validaLogin, home
from ApoloCare import views



urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    #path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('valida-login/', validaLogin, name='valida_login'),
    path('logout/', logout_view, name='logout'),
    path('nutricionista/', nutricionista, name='nutricionista'),
    path('cadastro_usuario/', cadastro_usuario, name='cadastro_usuario'),
    path('inclusao_usuario/', inclusao_usuario, name='inserir-usuario'),
    path('cadastro_nutricionista/', cadastro_nutricionista, name='cadastro_nutricionista'),
    path('cadastro_nutricionista/<int:id>/', cadastro_nutricionista, name='editar_nutricionista'),
    path('inserir_nutricionista/', inclusao_nutricionista, name='inclusao_nutricionista'),
    path('deletar_nutricionista/', excluir_nutricionista, name='deletar_nutricionista'),
    path('paciente', paciente, name="paciente"),



]
