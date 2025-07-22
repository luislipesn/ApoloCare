from datetime import datetime
from django.shortcuts import redirect, render
from psycopg2 import sql
from ApoloCare.decorators import usuario_logado
from ApoloCare.database import conectar_banco
from django.contrib import messages


def exclusao_avaliacao(request):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        query = sql.SQL("DELETE FROM avaliacao_atendimento WHERE id_consulta = %s")
        cursor.execute(query, (request.POST["id"],))
        conn.commit()

        conn.close()
    except Exception as e:
        print(f"Erro ao excluir avaliação: {e}")


@usuario_logado
def inserir_avaliacao(request):
    conn = conectar_banco()
    cursor = conn.cursor()

    query = sql.SQL("SELECT MAX(id_consulta) FROM Consulta WHERE id_usuario=%s")
    cursor.execute(query,(request.session['id_usuario'],))

    consulta = cursor.fetchone()

    query = sql.SQL("INSERT INTO avaliacao_atendimento (id_consulta) VALUES (%s)")
    cursor.execute(query, (consulta,))
    conn.commit()
    conn.close()
    cursor.close()


@usuario_logado
def listar_avaliacoes(request):
    conn = conectar_banco()
    cursor = conn.cursor()

    if request.session["tipo_usuario"] == "A":
        cursor.execute(
            """
            SELECT a.id_consulta, c.dt_consulta, c.hr_consulta, n.nome, a.nota, a.comentario, a.id_avaliacao_atendimento
            FROM avaliacao_atendimento a, consulta c, nutricionista n
            WHERE a.id_consulta = c.id_consulta
            AND c.id_nutricionista = n.id_nutricionista
            ORDER BY c.dt_consulta DESC, c.hr_consulta DESC
            """
        )

        resultados = cursor.fetchall()
        conn.close()

        avaliacoes = [
            {
                "id_consulta": row[0],
                "dt_consulta": row[1],
                "hr_consulta": row[2],
                "nome_nutricionista": row[3],
                "nota": row[4],
                "comentario": row[5],
                "id_avaliacao": row[6],
            }
            for row in resultados
        ]
    elif request.session["tipo_usuario"] == "P":
        query = sql.SQL("""
            SELECT 
                a.id_consulta,
                c.dt_consulta,
                c.hr_consulta,
                n.nome,
                a.nota,
                a.comentario,
                a.id_avaliacao_atendimento
            FROM avaliacao_atendimento a, consulta c, nutricionista n, paciente p
            WHERE a.id_consulta = c.id_consulta
            AND c.id_nutricionista = n.id_nutricionista
            AND c.id_paciente = p.id_paciente
            AND p.id_usuario = %s
            ORDER BY c.dt_consulta DESC, c.hr_consulta DESC
        """)
        cursor.execute(query, (request.session["id_usuario"],))
        resultados = cursor.fetchall()

        avaliacoes = [
            {
                "id_consulta": row[0],
                "dt_consulta": row[1],
                "hr_consulta": row[2],
                "nome_nutricionista": row[3],
                "nota": row[4],
                "comentario": row[5],
                "id_avaliacao": row[6],
        }
        for row in resultados
    ]


    else:
        return redirect("home")

    return render(request, "avaliacoes.html", {"avaliacoes": avaliacoes})


@usuario_logado
def avaliacao_atendimento(request):
    id_avaliacao = request.POST.get("id_avaliacao")

    dados_avaliacao = None

    if id_avaliacao:
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            query = sql.SQL(
                """
            SELECT a.id_avaliacao_atendimento, c.dt_consulta, c.hr_consulta, a.nota, a.comentario, a.id_consulta
            FROM avaliacao_atendimento a, Consulta c 
            WHERE a.id_consulta = c.id_consulta
            AND a.id_avaliacao_atendimento = %s
            """
            )

            cursor.execute(query, (id_avaliacao,))
            dados_avaliacao = cursor.fetchone()
            cursor.close()
            conn.close()

            print(dados_avaliacao)

        except Exception as e:
            messages.error(request, f"Erro ao buscar avaliação: {str(e)}")

    contexto = {"dados_avaliacao": dados_avaliacao}
    return render(request, "avaliacao_atendimento.html", contexto)


def avaliar(request):
    conn = conectar_banco()
    cursor = conn.cursor()

    dt_avaliacao = datetime.now().date()
    hr_avaliacao = datetime.now().time()

    nota = request.POST.get("nota")
    comentario = request.POST.get("comentario")
    id_avaliacao = request.POST.get("id_avaliacao_atendimento")

    if not all([nota, comentario, id_avaliacao]):
        messages.error(request, "Dados incompletos para avaliação.")
        cursor.close()
        conn.close()
        return redirect("avaliacao")

    try:
        cursor.execute(
            """
            UPDATE avaliacao_atendimento
            SET dt_avaliacao = %s, hr_avaliacao = %s, nota = %s, comentario = %s
            WHERE id_avaliacao_atendimento = %s
            """,
            (dt_avaliacao, hr_avaliacao, nota, comentario, id_avaliacao),
        )
        conn.commit()
        messages.success(request, "Atendimento avaliado com sucesso.")
    except Exception as e:
        messages.error(request, f"Erro ao atualizar avaliação: {str(e)}")
    finally:
        cursor.close()
        conn.close()

    return redirect("avaliacao")


# Create your views here.
