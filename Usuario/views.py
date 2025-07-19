import re
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from psycopg2 import sql
from django.contrib.auth import logout
from ApoloCare.decorators import usuario_logado
from ApoloCare.database import conectar_banco

# Create your views here.
def validaLogin(request):  # CLASSE DE VALIDAÇÃO DO LOGIN
    if request.method == "POST":
        try:
            conn = conectar_banco()  # CONEXÃO COM O BANCO DE DADOS
            cursor = conn.cursor()

            username = request.POST["login"].lower()  # ATRIBUIÇÃO PARA A VARIAVEL LOGIN A INFORMAÇÃO VINDA DO HTML
            senha = request.POST[
                "senha"
            ]  # ATRIBUIÇÃO PARA A VARIAVEL SENHA A INFORMAÇÃO VINDA DO HTML

            query = sql.SQL(
                "SELECT id_usuario, senha, nome, login, tipo_usuario, ativo FROM Usuario WHERE login = %s"
            )  # PROCURA NO BANCO DE DADOS
            cursor.execute(query, (username,))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()  # Fechando conexão

            if resultado:
                user_id, hashed_password, nome, usuario, tipo_usuario, ativo = resultado
                if ativo:  # Verifica se o usuário está ativo ou não
                    if check_password(
                        senha, hashed_password
                    ):  # CHECA SE A SENHA ESTA CORRETA
                        request.session["id_usuario"] = user_id
                        request.session["nome"] = nome  # GUARDA O NOME NA SESSÃO
                        request.session["login"] = usuario
                        request.session["tipo_usuario"] = tipo_usuario
                        request.session["ativo"] = ativo
                        return redirect("home") # CASO O LOGIN E A SENHA ESTIVEREM CORRETOS, REDIRECIONAR PARA A PAGINA HOMEF
                    else:
                        messages.error(
                            request, "Usuário e/ou Senha incorretos."
                        )  # CASO A SENHA ESTEJA INCORRETA INFORMAR NA TELA
                else:
                    messages.error(request, "Usuário bloqueado!")
            else:
                messages.error(request, "Usuário e/ou Senha incorretos.")

        except Exception as e:
            messages.error(
                request, f"Erro ao tentar login: {str(e)}"
            )  # CASO DÊ ERRO NA CONEXÃO COM O BANCO

    return redirect("login")



def logout_view(request):
    logout(request)
    return redirect("login")  # redireciona para a tela de login

def cadastro_usuario(request):
    return render(request, "cadastro_usuario.html")

def inclusao_usuario(request):
    try:
        if request.method == "POST":
            nome = request.POST["nome"]
            dt_nasc = request.POST["dt_nasc"]
            cpf = re.sub(r"\D", "", request.POST["cpf"])
            telefone = re.sub(r"\D", "", request.POST["telefone"])
            tipo_usuario = request.POST["tipo_usuario"]
            endereco = request.POST["endereco"]
            login = request.POST["login"].lower()
            senha = make_password(request.POST["senha"])
            ativo = True

            #print(ativo)

            conn = conectar_banco()
            cursor = conn.cursor()

            query = sql.SQL(
                "INSERT INTO Usuario(nome, dt_nasc, cpf, telefone, endereco, tipo_usuario, login, senha, ativo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(
                query,
                (
                    nome,
                    dt_nasc,
                    cpf,
                    telefone,
                    endereco,
                    tipo_usuario,
                    login,
                    senha,
                    ativo,
                ),
            )
            conn.commit()
            cursor.close()
            conn.close()
        if request.session['id_usuario']:
             return redirect("usuario")  
        return redirect("login")
    except Exception as e:
        messages.error(
            request, f"Erro ao cadastrar: {str(e)}"
        )  # CASO DÊ ERRO NA CONEXÃO COM O BANCO

    return redirect("cadastro_usuario")

@usuario_logado
def listar_usuarios(request):
    #try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_usuario, nome, login, ativo, tipo_usuario FROM Usuario WHERE tipo_usuario NOT IN ('N', 'P')
        """)
        usuarios = cursor.fetchall()

        conn.close()
        return render(request, "usuarios.html", {"usuarios": usuarios})

    #except Exception as e:
        #messages.error(request, f"Erro ao buscar usuários: {str(e)}")
        #return redirect("home")
    
@usuario_logado
def alterar_status(request):
    if request.method == "POST":
        id_usuario = request.POST.get("id_usuario")

        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            # Alternar status
            cursor.execute("""
                UPDATE Usuario
                SET ativo = NOT ativo
                WHERE id_usuario = %s
            """, (id_usuario,))

            conn.commit()
            cursor.close()
            conn.close()

            messages.success(request, "Status do usuário atualizado com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao atualizar status: {str(e)}")

    return redirect("usuario")

def inclusao_nutri_paciente(request):
    try:
        if request.method == "POST":
            nome = request.POST["nome"]
            dt_nasc = request.POST["dt_nasc"]
            cpf = re.sub(r"\D", "", request.POST["cpf"])
            telefone = re.sub(r"\D", "", request.POST["telefone"])
            tipo_usuario = request.POST["tipo_usuario"]
            endereco = request.POST["endereco"]
            login = request.POST["login"].lower()
            senha = make_password(request.POST["senha"])
            ativo = True

            #print(ativo)

            conn = conectar_banco()
            cursor = conn.cursor()

            query = sql.SQL(
                "INSERT INTO Usuario(nome, dt_nasc, cpf, telefone, endereco, tipo_usuario, login, senha, ativo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(
                query,
                (
                    nome,
                    dt_nasc,
                    cpf,
                    telefone,
                    endereco,
                    tipo_usuario,
                    login,
                    senha,
                    ativo,
                ),
            )
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        messages.error(
            request, f"Erro ao cadastrar: {str(e)}"
        )  # CASO DÊ ERRO NA CONEXÃO COM O BANCO

