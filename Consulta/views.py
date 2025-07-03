from django.shortcuts import render
from psycopg2 import sql
from ApoloCare.decorators import usuario_logado
from ApoloCare.database import conectar_banco

@usuario_logado
def cadastro_consulta(request):
    
    return (request, "cadastro_consulta.html")

@usuario_logado
def consulta(request):
    
    conn = conectar_banco() #Conexão com o banco de dados
    cursor = conn.cursor()

    if request.session['tipo_usuario'] == "N":
        query = sql.SQL("SELECT c.id_consulta, p.nome AS paciente, n.nome AS nutricionista, c.dt_consulta, c.hr_consulta, c.peso, c.altura FROM Consulta c, Paciente p, Nutricionista n WHERE c.id_paciente = p.id_paciente  AND c.id_nutricionista = n.id_nutricionista AND n.id_nutricionista = %s")
        cursor.execute(query, (id,))
    else:
        query = sql.SQL("SELECT c.id_consulta, p.nome AS paciente, n.nome AS nutricionista, c.dt_consulta, c.hr_consulta, c.peso, c.altura FROM Consulta c, Paciente p, Nutricionista n WHERE c.id_paciente = p.id_paciente  AND c.id_nutricionista = n.id_nutricionista")
    
    consultas = cursor.fetchall()

    conn.close()
    cursor.close()

    contexto = {
        'consultas' : consultas
    }
    
    
    return render(request, "consulta.html", contexto)
