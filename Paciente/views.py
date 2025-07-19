from django.contrib import messages
import re
from django.shortcuts import redirect, render
from psycopg2 import sql
from Usuario.views import inclusao_nutri_paciente
from ApoloCare.database import conectar_banco
from ApoloCare.decorators import usuario_logado
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

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
    conn = conectar_banco()
    cursor = conn.cursor()

    id = request.POST.get('id', None)
    if id:
        query = sql.SQL(
            "SELECT id_paciente, nome, cpf, dt_nasc, endereco, sexo, telefone, email, convenio, id_usuario FROM Paciente WHERE id_paciente = %s"
        )
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()
        contexto = {"dados_paciente" : resultado}
    else:
        cursor.execute("SELECT id_usuario, nome FROM usuario u WHERE tipo_usuario = 'P' AND id_usuario NOT IN (SELECT id_usuario FROM Paciente)")
        usuarios = cursor.fetchall()
        contexto = {"usuarios": usuarios}

    cursor.close()
    conn.close()
    return render(request, "cadastro_paciente.html", contexto)


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

            id = request.POST.get('id_paciente', None)
            if id:
                query = sql.SQL("""
                UPDATE Paciente
                SET nome=%s, dt_nasc=%s, cpf=%s, sexo=%s, endereco=%s, telefone=%s, email=%s, convenio=%s
                WHERE id_paciente = %s;
                """)
                cursor.execute(query, (nome, dt_nasc, cpf, sexo, endereco, telefone, email, convenio, id))
                messages.success(request, f"Alterado com sucesso!")
            else:
                
                inclusao_nutri_paciente(request)

                query = sql.SQL("SELECT id_usuario FROM Usuario WHERE cpf = %s")
                cursor.execute(query, (cpf,))
                id_usuario = cursor.fetchone()

                if id_usuario is None:
                    raise Exception("Usuário não encontrado com o CPF informado.")

                id_usuario = id_usuario[0]

                query = sql.SQL("""
                    INSERT INTO paciente(nome, dt_nasc, cpf, sexo, endereco, telefone, email, convenio, id_usuario)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """)
                cursor.execute(query, (nome, dt_nasc, cpf, sexo, endereco, telefone, email, convenio, id_usuario))

            conn.commit()
            cursor.close()
            return redirect("paciente")
    except Exception as e:
        messages.error(request, f"Erro ao cadastrar paciente: {str(e)}")
        return redirect("cadastro_paciente")

@usuario_logado
def exclusao_paciente(request):
    
    id = request.POST.get('id', None) #Se estiver chegando pelo post o 'id', atribuir a variavel 'id', caso não venha, atribuir como None/Nulo
    try:
        if id: #Verifica se o id não está nulo
            conn = conectar_banco() 
            cursor = conn.cursor()

            query = sql.SQL("SELECT id_paciente FROM Consulta WHERE id_paciente =%s")
            cursor.execute(query, (id,))
            paciente = cursor.fetchone()
            if paciente:
                messages.error(request, f"O Paciente está cadastrado a uma consulta.")
                cursor.close()
                conn.close()
                return redirect("paciente")
            else:
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