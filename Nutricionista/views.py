from django.shortcuts import render
from psycopg2 import sql

from ApoloCare.decorators import usuario_logado
from ApoloCare.database import conectar_banco

@usuario_logado
def consulta_nutri(request):

    conn = conectar_banco()
    cursor = conn.cursor()

    query = sql.SQL("SELECT id_nutricionista, nome, crn FROM nutricionista")
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado
