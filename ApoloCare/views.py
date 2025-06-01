from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from psycopg2 import sql
from django.contrib.auth import logout
from .database import conectar_banco
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login


def validaLogin(request):
    if request.method == "POST":
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            username = request.POST["login"]
            senha = request.POST["senha"]

            # Busca o hash da senha pelo username
            query = sql.SQL("SELECT id, password FROM auth_user WHERE username = %s")
            cursor.execute(query, (username,))
            resultado = cursor.fetchone()

            cursor.close()
            conn.close()

            if resultado:
                user_id, hashed_password = resultado

                if check_password(senha, hashed_password):
                    # Buscar o objeto User para criar sessão
                    try:
                        user = User.objects.get(pk=user_id)
                        login(request, user)
                        return redirect("home")
                    except User.DoesNotExist:
                        messages.error(request, "Usuário existe no banco, mas não no sistema.")
                else:
                    messages.error(request, "Senha incorreta.")
            else:
                messages.error(request, "Usuário não encontrado.")

        except Exception as e:
            messages.error(request, f"Erro ao tentar login: {str(e)}")

    return redirect("login")

def logout_view(request):
    logout(request)
    return redirect('login')  # redireciona para a tela de login

@login_required
def home(request):
    return render(request, 'home.html', {'user': request.user})
