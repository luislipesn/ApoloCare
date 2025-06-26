from django.shortcuts import render, redirect
from .decorators import usuario_logado

def login(request):
    return render (request, "login.html")

@usuario_logado
def home(request):
    return render(request, "home.html", {"user": request.user})
