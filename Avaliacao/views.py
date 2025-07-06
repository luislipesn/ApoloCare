from django.shortcuts import redirect, render
from psycopg2 import sql
from ApoloCare.decorators import usuario_logado
from ApoloCare.database import conectar_banco


@usuario_logado
def exclusao_avaliacao (id):

    conn = conectar_banco()
    cursor = conn.cursor()

    query = sql.SQL("DELETE FROM avaliacao_atendimento WHERE id_consulta = %s")
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()
    cursor.close()

@usuario_logado
def inserir_avaliacao():
    conn = conectar_banco()
    cursor = conn.cursor()

    query = sql.SQL("SELECT MAX(id_consulta) FROM Consulta")
    cursor.execute(query)

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

    if request.session['tipo_usuario'] == 'A':
        cursor.execute("""
            SELECT a.id_consulta, c.dt_consulta, c.hr_consulta, n.nome, a.nota, a.comentario
            FROM avaliacao_atendimento a, consulta c, nutricionista n
            WHERE a.id_consulta = c.id_consulta
            AND c.id_nutricionista = n.id_nutricionista
            ORDER BY c.dt_consulta DESC, c.hr_consulta DESC
        """)
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
            }
            for row in resultados
        ]
    elif request.session['tipo_usuario'] == 'P':
        cursor.execute(""" SELECT id_paciente FROM Consulta c, Avaliacao_atendimento a WHERE a.id_consulta = c.id_consulta""")
        resultado = cursor.fetchone()

        query = sql.SQL("SELECT a.id_consulta, c.dt_consulta, c.hr_consulta, n.nome, a.nota, a.comentario FROM avaliacao_atendimento a, consulta c, nutricionista n WHERE a.id_consulta = c.id_consulta AND c.id_nutricionista = n.id_nutricionista AND a.id_consulta = %s ORDER BY c.dt_consulta DESC, c.hr_consulta DESC")
        cursor.execute(query, (resultado,))
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
            }
            for row in resultados
        ]
    else:
        return redirect("home")

    return render(request, "avaliacoes.html", {"avaliacoes": avaliacoes})

@usuario_logado
def avaliacao_atendimento(request):
    print("Oi")

# Create your views here.
