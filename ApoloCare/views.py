
from django.shortcuts import redirect, render
from ApoloCare.ApoloCare.database import conectar_banco
from psycopg2 import sql
from django.contrib.auth.hashers import make_password
from django.contrib import messages

def validaLogin(request):
    
    if request.method == 'POST':
        conn = conectar_banco()
        cursor = conn.cursor()
        username = request.POST['username']
        senha = make_password(request.POST['username'])

        query = sql.SQL("SELECT id FROM auth_user WHERE username = %s AND password = %s")
        cursor.execute(query,(username, senha))

        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        if resultado is not None:
            return redirect('home')
        else:
            messages.error(request, 'Senha incorreta.')
    
    return render(request, 'login.html')

