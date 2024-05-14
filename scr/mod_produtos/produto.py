from flask import Blueprint, render_template
import requests

from mod_login.login import validaSessao
from settings import ENDPOINT_PRODUTO, getHeadersAPI
bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

''' rotas dos formulários '''
@bp_produto.route('/', methods=['GET', 'POST'])
@validaSessao
def formListaProduto():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers=getHeadersAPI())
        result = response.json()
        
        if (response.status_code != 200):    
            raise Exception(result)
        
        return render_template('formListaProduto.html', result=result[0])
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/form-produto/')
def formProduto():
    return render_template('formProduto.html')