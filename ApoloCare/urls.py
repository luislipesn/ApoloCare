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
from django.urls import include, path
from django.contrib.auth import views as auth_views

from Paciente.views import paciente
from .views import cadastro_usuario, inclusao_usuario, login, logout_view, validaLogin, home
from ApoloCare import views



urlpatterns = [
    path('home/', home, name='home'),
    path('', home, name='home'),
    #path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('valida-login/', validaLogin, name='valida_login'),
    path('logout/', logout_view, name='logout'),
    path('cadastro_usuario/', cadastro_usuario, name='cadastro_usuario'),
    path('inclusao_usuario/', inclusao_usuario, name='inserir-usuario'),
    path('paciente/', include('Paciente.urls')),
    path('nutricionista/', include('Nutricionista.urls'))
]
