from django.contrib import messages
from django.shortcuts import redirect, render
from psycopg2 import sql
import re
from ApoloCare.decorators import usuario_logado
from ApoloCare.database import conectar_banco


@usuario_logado
def nutricionista(request):
    conn = conectar_banco()
    cursor = conn.cursor()

    query = sql.SQL("SELECT id_nutricionista, nome, crn FROM nutricionista")
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    contexto = {
        "nutricionistas": resultado
    }
    return render(request, 'nutricionista.html', contexto)


@usuario_logado
def cadastro_nutricionista(request, id=None):
    if id:
        conn = conectar_banco()
        cursor = conn.cursor()

        query = sql.SQL("SELECT id_nutricionista, nome, cpf, crn, dt_nasc, sexo, telefone, email FROM nutricionista WHERE id_nutricionista = '%s'")
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
        if request.method == "POST":
            nome = request.POST["nome"]
            crn = request.POST["crn"]
            dt_nasc = request.POST["data_nascimento"]
            cpf = re.sub(r"\D", "", request.POST["cpf"])
            telefone = re.sub(r"\D", "", request.POST["telefone"])
            sexo = request.POST["sexo"]
            email = request.POST["email"]

            conn = conectar_banco()
            cursor = conn.cursor()

            if request.POST["id_nutricionista"]:
                id = request.POST["id_nutricionista"]
                query = sql.SQL(
                    "UPDATE Nutricionista SET nome=%s, cpf=%s, crn=%s, dt_nasc=%s, sexo=%s, telefone=%s, email=%s WHERE id_nutricionista=%s"
                )
                cursor.execute(query, (nome, cpf, crn, dt_nasc, sexo, telefone, email, id))
            else:
                query = sql.SQL(
                    "INSERT INTO Nutricionista(nome, cpf, crn, dt_nasc, sexo, telefone, email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                )
                cursor.execute(query, (nome, cpf, crn, dt_nasc, sexo, telefone, email))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect("nutricionista")
    except Exception as e:
        messages.error(
            request, f"{str(e)}"
        )  # CASO DÊ ERRO NA CONEXÃO COM O BANCO
        if request.POST["id_nutricionista"]:
            return redirect("/cadastro_nutricionista/" + request.POST['id_nutricionista'] + "/")
        

@usuario_logado
def excluir_nutricionista(request, id):
    
    try:
        if id:
            conn = conectar_banco()
            cursor = conn.cursor()

            query = sql.SQL("DELETE FROM Nutricionista WHERE id_nutricionista = '%s'")
            cursor.execute(query, (id,))
            conn.commit()
            cursor.close()
            conn.close()
        return redirect("nutricionista")
    except Exception as e:
        messages.error(
            request, f"Erro ao tentar cadastrar: {str(e)}"
        )  # CASO DÊ ERRO NA CONEXÃO COM O BANCO
        return redirect("nutricionista")
