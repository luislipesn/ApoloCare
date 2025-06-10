from django.shortcuts import render
from psycopg2 import sql

from ApoloCare.database import conectar_banco

def consulta_nutri(request):

    conn = conectar_banco()
    cursor = conn.cursor()

    query = sql.SQL("SELECT")
