from django.shortcuts import render, redirect

from .database import conectar_banco
from .decorators import usuario_logado

def login(request):
    return render (request, "login.html")

@usuario_logado
def home(request):

    conn = conectar_banco()
    cursor = conn.cursor()

    query = sql.SQL("SELECT c.dt_consulta, c.hr_consulta, p.nome FROM Consulta p, Paciente p WHERE dt_consulta > CURRENT_DATE")
    return render(request, "home.html", {"user": request.user})
