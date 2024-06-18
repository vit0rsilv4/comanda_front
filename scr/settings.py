from dotenv import load_dotenv, find_dotenv
import os
from flask import session

# Localiza o arquivo .env
dotenv_file = find_dotenv()
# Carrega o arquivo .env
load_dotenv(dotenv_file)

# Configurações da APP
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DEBUG = os.getenv("DEBUG")

# Configurações da API
URL_API = os.getenv("URL_API")

# Configuração dos endpoints
ENDPOINT_TOKEN = os.getenv("ENDPOINT_TOKEN")
ENDPOINT_FUNCIONARIO = os.getenv("ENDPOINT_FUNCIONARIO")
ENDPOINT_CLIENTE = os.getenv("ENDPOINT_CLIENTE")
ENDPOINT_PRODUTO = os.getenv("ENDPOINT_PRODUTO")

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def getHeadersAPI():
    return {
        'accept': 'application/json',
        'Authorization': f'Bearer {session["access_token"] if "access_token" in session else ""}'
    }

TEMPO_SESSION = os.getenv("TEMPO_SESSION")
