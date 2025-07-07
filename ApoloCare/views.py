from django.shortcuts import render
from psycopg2 import sql
from .database import conectar_banco
from .decorators import usuario_logado

def login(request):
    return render (request, "login.html")

@usuario_logado
def home(request):

    conn = conectar_banco()
    cursor = conn.cursor()

    query = sql.SQL("SELECT c.dt_consulta, c.hr_consulta, p.nome FROM Consulta c, Paciente p WHERE c.id_paciente = p.id_paciente and dt_consulta >= CURRENT_DATE ORDER BY c.dt_consulta, c.hr_consulta")
    cursor.execute(query)
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return render(request, "home.html", {"consultas": resultado})
