from django.urls import path

from .views import paciente


urlpatterns = [
    path('paciente/', paciente, name="paciente"),
]