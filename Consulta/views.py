from django.shortcuts import redirect, render
from psycopg2 import sql
from django.contrib import messages
from Avaliacao.views import exclusao_avaliacao, inserir_avaliacao
from ApoloCare.decorators import usuario_logado
from ApoloCare.database import conectar_banco

@usuario_logado
def consulta(request):
    consultas = []  # Valor padrão vazio

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        if request.session['tipo_usuario'] == "N":
            query = sql.SQL("""
                SELECT id_nutricionista FROM Nutricionista WHERE id_usuario = %s
            """)
            cursor.execute(query, (request.session['id_usuario'],))
            id_nutricionista = cursor.fetchone()
            #id_nutricionista = request.session.get("id_usuario")
            query = sql.SQL("""
                SELECT c.id_consulta, p.nome AS paciente, n.nome AS nutricionista, 
                       c.dt_consulta, c.hr_consulta, c.peso, c.altura 
                FROM Consulta c 
                JOIN Paciente p ON c.id_paciente = p.id_paciente  
                JOIN Nutricionista n ON c.id_nutricionista = n.id_nutricionista 
                WHERE n.id_nutricionista = %s
            """)
            cursor.execute(query, (id_nutricionista,))
        else:
            query = sql.SQL("""
                SELECT c.id_consulta, p.nome AS paciente, n.nome AS nutricionista, 
                       c.dt_consulta, c.hr_consulta, c.peso, c.altura 
                FROM Consulta c 
                JOIN Paciente p ON c.id_paciente = p.id_paciente  
                JOIN Nutricionista n ON c.id_nutricionista = n.id_nutricionista
            """)
            cursor.execute(query)

        consultas = cursor.fetchall()
        cursor.close()
        conn.close()

    except Exception as e:
        messages.error(request, f"Erro ao buscar consultas: {str(e)}")
        # Ignora o erro e segue com consultas vazio

    return render(request, "consulta.html", {'consultas': consultas})

@usuario_logado
def cadastro_consulta(request):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Buscar dados da consulta, se for edição
    dados_consulta = None

    id = request.POST.get("id", None)
    if id:
        cursor.execute("SELECT * FROM consulta WHERE id_consulta = %s", [id])
        dados_consulta = cursor.fetchone()

    # Carregar dados auxiliares para selects
    cursor.execute("SELECT id_paciente, nome FROM paciente")
    pacientes = cursor.fetchall()

    cursor.execute("SELECT id_nutricionista, nome FROM nutricionista")
    nutricionistas = cursor.fetchall()

    cursor.close()
    
    contexto = {
        'dados_consulta': dados_consulta,
        'pacientes': pacientes,
        'nutricionistas': nutricionistas,
    }

    return render(request, "cadastro_consulta.html", contexto)

@usuario_logado
def deletar_consulta(request):
    if request.session["tipo_usuario"] == 'A':
        
        try:

            exclusao_avaliacao(request)
        
            conn = conectar_banco()
            cursor = conn.cursor()

            query = sql.SQL("DELETE FROM Consulta WHERE id_consulta = %s")
            cursor.execute(query,(request.POST['id'],))
            conn.commit()

            cursor.close()
            conn.close()
        
        except Exception as e:
            if conn:
                conn.rollback()  # desfaz tudo que foi feito antes do commit
            messages.error(request, f"{str(e)}")
            return redirect(request, "consulta")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        messages.error(request, f"Você não tem permissão para excluir!")
    return redirect("consulta")

def incluir_consulta(request):
    if request.method == "POST":
        id_consulta = request.POST.get("id_consulta", None)
        dt_consulta = request.POST.get("dt_consulta")
        hr_consulta = request.POST.get("hr_consulta")
        
        altura = float(request.POST.get("altura").replace(",", "."))
        peso = float(request.POST.get("peso").replace(",", "."))
        bioimpedancia = request.POST.get("bioimpedancia")
        observacoes = request.POST.get("observacoes")
        id_paciente = request.POST.get("id_paciente")
        id_nutricionista = request.POST.get("id_nutricionista")
        id_usuario = request.session["id_usuario"]

        conn = conectar_banco()
        cursor = conn.cursor()

        try:
            if id_consulta:
                # Atualizar
                cursor.execute("""
                    UPDATE consulta SET
                        dt_consulta = %s,
                        hr_consulta = %s,
                        altura = %s,
                        peso = %s,
                        bioimpedancia = %s,
                        observacoes = %s,
                        id_paciente = %s,
                        id_nutricionista = %s,
                        id_usuario = %s
                    WHERE id_consulta = %s
                """, [dt_consulta, hr_consulta, altura, peso, bioimpedancia, observacoes, id_paciente, id_nutricionista, id_usuario, id_consulta])
                conn.commit()
            else:
                # Inserir nova
                cursor.execute("""
                    INSERT INTO consulta (
                        dt_consulta, hr_consulta, altura, peso,
                        bioimpedancia, observacoes, id_paciente,
                        id_nutricionista, id_usuario
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [dt_consulta, hr_consulta, altura, peso, bioimpedancia, observacoes, id_paciente, id_nutricionista, id_usuario])
                conn.commit()
                inserir_avaliacao(request)

            
            messages.success(request, "Consulta salva com sucesso.")
            cursor.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            messages.error(request, f"Erro ao salvar consulta: {str(e)}")
        
        
        return redirect("consulta")  # Ajuste para o nome real da URL de listagem

    

