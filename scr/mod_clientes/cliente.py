from flask import Blueprint, render_template
import requests

from mod_login.login import validaSessao
from settings import ENDPOINT_CLIENTE, getHeadersAPI
bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

''' rotas dos formulários '''
@bp_cliente.route('/',  methods=['GET', 'POST'])
@validaSessao
def formListaCliente():
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers=getHeadersAPI())
        result = response.json()

        if (response.status_code != 200):    
            raise Exception(result)
        
        return render_template('formListaCliente.html', result=result[0])
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/form-cliente/')
def formCliente():
    return render_template('formCliente.html')

