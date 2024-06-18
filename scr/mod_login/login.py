from flask import Blueprint, render_template, request, redirect, url_for, session
import requests
from settings import ENDPOINT_TOKEN, SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta
from jose import jwt
bp_login = Blueprint('login', __name__, url_prefix='/', template_folder='templates')
from functools import wraps

@bp_login.route("/", methods=['GET', 'POST'])
def login():
    return render_template("formLogin.html")

@bp_login.route('/login', methods=['POST'])
def validaLogin():
    try:
        session.clear()
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'username': request.form['usuario'],
            'password': request.form['senha'],
            'grant_type': '', 'scope': '', 'client_id': '', 'client_secret': ''
        }
        response = requests.post(ENDPOINT_TOKEN, headers=headers, data=data)
        access_token = response.json()
        if response.status_code != 200:
            raise Exception(access_token)

        # Decodifica o token para extrair as informações
        token_payload = jwt.decode(access_token['access_token'], SECRET_KEY, algorithms=[ALGORITHM])

        # Registra os dados do token e do usuário na sessão, armazenando o login do usuário
        session['access_token'] = access_token['access_token']
        session['expire_minutes'] = (token_payload['exp'] - datetime.now().timestamp()) / 60  # Calcula o tempo de expiração em minutos
        session['token_type'] = access_token['token_type']
        session['token_validade'] = token_payload['exp']
        ### Futuramente alterar a API para retornar os dados do usuário
        session['nome'] = request.form['usuario']
        session['login'] = request.form['usuario']
        session['grupo'] = "1"
        # Abre a aplicação na tela home
        return redirect(url_for('index.formIndex'))
    except Exception as e:
        # Retorna para a tela de login
        return redirect(url_for('login.login', msgErro=e.args[0], msgException=e.args[0]))

@bp_login.route("/logoff", methods=['GET'])
def logoff():
    # Limpa um valor individual
    session.pop('login', None)
    # Limpa toda sessão
    session.clear()
    # Retorna para a tela de login
    return redirect(url_for('login.login'))

def is_token_expired():
    token_validade = session.get('token_validade')
    if token_validade:
        return datetime.now().timestamp() > token_validade
    return True

def refresh_token():
    try:
        access_token = session.get('access_token')
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(f"{ENDPOINT_TOKEN}/refresh-token", headers=headers)
        if response.status_code == 200:
            new_token = response.json()
            session['access_token'] = new_token['access_token']
            session['token_type'] = new_token['token_type']
            # Atualiza a validade do token na sessão
            token_payload = jwt.decode(new_token['access_token'], SECRET_KEY, algorithms=[ALGORITHM])
            session['token_validade'] = token_payload['exp']
        else:
            raise Exception("Erro ao renovar token")
    except Exception as e:
        print(f"Erro ao renovar token: {e}")
        return redirect(url_for('login.login', msgErro="Erro ao renovar token"))

def fetch_protected_data(url):
    if is_token_expired():
        refresh_token()
    access_token = session.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def validaSessao(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            return redirect(url_for('login.login', msgErro='Usuário não logado!'))
        else:
            return f(*args, **kwargs)
    return decorated_function

def validaToken(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token_validade' in session and session['token_validade'] > datetime.timestamp(datetime.now()):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login.login', msgErro='Usuário não logado! Token expirado!'))
    return decorated_function
