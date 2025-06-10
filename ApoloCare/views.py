from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from psycopg2 import sql
from django.contrib.auth import logout
from .database import conectar_banco
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from Nutricionista.models import Nutricionista


def validaLogin(request): #CLASSE DE VALIDAÇÃO DO LOGIN
    if request.method == "POST":
        try:
            conn = conectar_banco() #CONEXÃO COM O BANCO DE DADOS
            cursor = conn.cursor()

            username = request.POST["login"] #ATRIBUIÇÃO PARA A VARIAVEL LOGIN A INFORMAÇÃO VINDA DO HTML
            senha = request.POST["senha"] #ATRIBUIÇÃO PARA A VARIAVEL SENHA A INFORMAÇÃO VINDA DO HTML

            query = sql.SQL("SELECT id, password, first_name, username FROM auth_user WHERE username = %s") #PROCURA NO BANCO DE DADOS 
            cursor.execute(query, (username,))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()

            if resultado:
                user_id, hashed_password, nome, usuario = resultado
                print(senha, " + ", make_password(senha))
                if check_password(senha, hashed_password): #CHECA SE A SENHA ESTA CORRETA
                    try:
                        user = User.objects.get(pk=user_id)
                        login(request, user)
                        request.session['first_name'] = nome
                        request.session['username'] = usuario
                        return redirect("home") #CASO O LOGIN E A SENHA ESTIVEREM CORRETOS, REDIRECIONAR PARA A PAGINA HOME
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

@login_required
def lista_nutricionistas(request):
    nutricionistas = Nutricionista.objects.all()
    return render(request, 'cadastro_nutricionista.html', {'nutricionistas': nutricionistas})

@login_required
def nutricionista(request):
    return render(request, 'nutricionista.html', {'user': request.user})
