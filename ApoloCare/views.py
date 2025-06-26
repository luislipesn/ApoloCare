from django.shortcuts import render, redirect
from .decorators import usuario_logado

@usuario_logado
def home(request):
    return render(request, "home.html", {"user": request.user})
