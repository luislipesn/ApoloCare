from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
from psycopg2 import sql
import re
from ApoloCare.decorators import usuario_logado
from ApoloCare.database import conectar_banco


@usuario_logado #Obriga o usuário estar logado para acessar a pagina
def nutricionista(request):
    conn = conectar_banco() #Conexão com o banco de dados
    cursor = conn.cursor()

    query = sql.SQL("SELECT id_nutricionista, nome, crn FROM nutricionista ORDER BY nome") #Consulta no banco de dados
    cursor.execute(query)
    resultado = cursor.fetchall() #Pega todos as linhas da consulta e atribui a váriavel "Resultado"
    cursor.close()
    conn.close()
    contexto = {
        "nutricionistas": resultado 
    }
    return render(request, 'nutricionista.html', contexto) #Retorna para a a pagina de consulta do nutricionista


@usuario_logado
def cadastro_nutricionista(request):
    id = request.POST.get('id', None)
    if id:
        conn = conectar_banco()
        cursor = conn.cursor()

        query = sql.SQL("SELECT id_nutricionista, nome, cpf, crn, dt_nasc, sexo, telefone, email FROM nutricionista WHERE id_nutricionista = %s")
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        contexto = {
            'dados_nutri' : resultado
        }
        return render(request, "cadastro_nutricionista.html", contexto)

    return render(request, "cadastro_nutricionista.html")


@usuario_logado
def inclusao_nutricionista(request):
    try:
        if request.method == "POST": #Verifica se os dados estão sendo passado pelo metodo POST
            nome = request.POST["nome"]
            crn = request.POST["crn"]
            dt_nasc = request.POST["data_nascimento"]
            cpf = re.sub(r"\D", "", request.POST["cpf"])
            telefone = re.sub(r"\D", "", request.POST["telefone"])
            sexo = request.POST["sexo"]
            email = request.POST["email"]

            conn = conectar_banco() #Conexão com o banco de dados
            cursor = conn.cursor()
            id = request.POST.get('id_nutricionista', None) #Se estiver chegando o 'id_nutricionista' atribuir a variavel 'id', caso não venha, atribuir como None/Nulo

            if id: #Caso tenha um ID, ele será um update
                query = sql.SQL(
                    "UPDATE Nutricionista SET nome=%s, cf=%s, crn=%s, dt_nasc=%s, sexo=%s, telefone=%s, email=%s WHERE id_nutricionista=%s"
                )
                cursor.execute(query, (nome, cpf, crn, dt_nasc, sexo, telefone, email, id))
                messages.error(request, f"Alterado com sucesso!")
            else: #Caso não, ele será um insert
                query = sql.SQL(
                    "INSERT INTO Nutricionista(nome, cpf, crn, dt_nasc, sexo, telefone, email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                )
                cursor.execute(query, (nome, cpf, crn, dt_nasc, sexo, telefone, email))
            conn.commit()
            cursor.close()
            conn.close()
        return redirect("nutricionista")
    
    except Exception as e:
        messages.error(request, f"{str(e)}")
        return redirect("nutricionista")
        

@usuario_logado
def excluir_nutricionista(request):
    id = request.POST.get('id', None) #Se estiver chegando pelo post o 'id', atribuir a variavel 'id', caso não venha, atribuir como None/Nulo
    try:
        if id: #Verifica se o id não está nulo
            conn = conectar_banco() 
            cursor = conn.cursor()

            query = sql.SQL("DELETE FROM Nutricionista WHERE id_nutricionista = %s") #Script de exclusão
            cursor.execute(query, (id,))
            conn.commit()
            cursor.close()
            conn.close()
            messages.error(request, f"Excluído com sucesso!")
        return redirect("nutricionista") #Retorno para a consulta de nutricionista
    except Exception as e:
        messages.error(
            request, f"Erro ao tentar excluir: {str(e)}"
        )  # CASO DÊ ERRO NA CONEXÃO COM O BANCO
        return redirect("nutricionista")
