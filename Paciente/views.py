from django.shortcuts import render

from ApoloCare.decorators import usuario_logado

@usuario_logado
def paciente(request):
    return render(request, "paciente.html")

def cadastro_paciente(request):
    return render(request, "cadastro_paciente.html")