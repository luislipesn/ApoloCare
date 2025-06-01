from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from psycopg2 import sql
from django.contrib.auth import logout
from .database import conectar_banco
from django.contrib.auth.decorators import login_required


def validaLogin(request):
    if request.method == "POST":
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            username = request.POST["login"]
            senha = request.POST["senha"]

            query = sql.SQL("SELECT id, password FROM auth_user WHERE username = %s")
            cursor.execute(query, (username,))
            resultado = cursor.fetchone()

            cursor.close()
            conn.close()

            if resultado and check_password(senha, resultado[1]):
                return redirect("home")  # essa URL precisa existir no seu urls.py
            else:
                messages.error(request, "Usuário ou senha incorretos.")
                return redirect("login")  # redireciona para login com mensagem de erro

        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {str(e)}")
            return redirect("login")
    return redirect("login")

def logout_view(request):
    logout(request)
    return redirect('login')  # redireciona para a tela de login

@login_required(login_url='login')
def home(request):
    return render(request, 'dashboard.html', {'user': request.user})
