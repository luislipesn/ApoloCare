from django.contrib import messages
import re
from django.shortcuts import redirect, render
from psycopg2 import sql
from ApoloCare.database import conectar_banco
from ApoloCare.decorators import usuario_logado

@usuario_logado
def paciente(request):

    conn = conectar_banco() #Conexão com o banco de dados
    cursor = conn.cursor()

    query = sql.SQL("SELECT id_paciente, nome, cpf FROM Paciente ORDER BY nome")
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    contexto = {
        "pacientes" : resultado
    }
    return render(request, 'paciente.html', contexto)

@usuario_logado
def cadastro_paciente(request):
    return render(request, "cadastro_paciente.html")

@usuario_logado
def inclusao_paciente(request):
    try:
        if request.method == "POST":
    
            nome = request.POST["nome"]
            cpf = re.sub(r"\D", "", request.POST["cpf"])
            dt_nasc = request.POST["dt_nasc"]
            sexo = request.POST["sexo"]
            endereco = request.POST["endereco"]
            telefone = re.sub(r"\D", "", request.POST["telefone"])
            email = request.POST["email"]
            convenio = request.POST["convenio"]

            conn = conectar_banco()
            cursor = conn.cursor()

            query = sql.SQL("INSERT INTO paciente(nome, dt_nasc, cpf, sexo, endereco, telefone, email, convenio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(query, (nome, dt_nasc, cpf, sexo, endereco, telefone, email, convenio))
            conn.commit()
            cursor.close()
            return redirect("paciente")
    except Exception as e:
        messages.error(request, f"Erro ao cadastrar paciente: {str(e)}")
        print(e)
        return redirect("cadastro_paciente")

def exclusao_paciente(request):
    
    id = request.POST.get('id', None) #Se estiver chegando pelo post o 'id', atribuir a variavel 'id', caso não venha, atribuir como None/Nulo
    try:
        if id: #Verifica se o id não está nulo
            conn = conectar_banco() 
            cursor = conn.cursor()

            query = sql.SQL("DELETE FROM Paciente WHERE id_paciente = %s") #Script de exclusão
            cursor.execute(query, (id,))
            conn.commit()
            cursor.close()
            conn.close()
            messages.success(request, f"Excluído com sucesso!")
        return redirect("paciente") #Retorno para a consulta de nutricionista
    except Exception as e:
        messages.error(
            request, f"Erro ao tentar excluir: {str(e)}"
        )  # CASO DÊ ERRO NA CONEXÃO COM O BANCO
        return redirect("paciente")