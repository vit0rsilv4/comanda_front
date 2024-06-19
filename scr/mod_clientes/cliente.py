from flask import Blueprint, render_template, request, redirect, send_file, url_for, jsonify
import requests
from mod_login.login import validaSessao, validaToken
from funcoes import Funcoes
from settings import getHeadersAPI, ENDPOINT_CLIENTE

bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

''' rotas dos formulários '''
@bp_cliente.route('/', methods=['GET', 'POST'])
@validaSessao
@validaToken
def formListaCliente():
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers=getHeadersAPI())
        result = response.json()
        print(result)

        if (response.status_code != 200):    
            raise Exception(result)
        
        return render_template('formListaCliente.html', result=result[0])
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/form-cliente/')
def formCliente():
    return render_template('formCliente.html')

@bp_cliente.route('/insert', methods=['POST'])
def insert():
    try:
        id_cliente = 0
        nome = request.form['nome']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        senha = Funcoes.get_password_hash(request.form['senha'])

        payload = {
            'id_cliente': id_cliente,
            'nome': nome,
            'telefone': telefone,
            'cpf': cpf,
            'senha': senha
        }

        response = requests.post(ENDPOINT_CLIENTE, headers=getHeadersAPI(), json=payload)
        result = response.json()
        print(result)
        print(response.status_code)

        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)
        
        return redirect(url_for('cliente.formListaCliente', msg=result[0]))
    
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route("/form-edit-cliente", methods=['POST'])
@validaSessao
def formEditCliente():
    try:
        id_cliente = request.form['id']
        response = requests.get(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI())
        result = response.json()
        print('result')

        print(result)

        if response.status_code != 200:
            raise Exception(result)

        return render_template('formCliente.html', result=result[0])

    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/edit')
def edit():
    try:
        id_cliente = request.form['id']
        nome = request.form['nome']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        senha = Funcoes.get_password_hash(request.form['senha'])

        payload = {
            'id_cliente': id_cliente,
            'nome': nome,
            'telefone': telefone,
            'cpf': cpf,
            'senha': senha
        }

        response = requests.put(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI(), json=payload)
        result = response.json()

        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)

        return redirect(url_for('cliente.formListaCliente', msg=result[0]))

    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/delete', methods=['POST'])
def delete():
    try:
        id_cliente = request.form['id']
        response = requests.delete(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)

        return jsonify(erro=False, msg=result[0])

    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])
    
@bp_cliente.route('/generate_pdf', methods=['GET'])
def generate_pdf():
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200:
            raise Exception(result)

        filename = "clientes_cadastrados.pdf"
        title = "Clientes Cadastrados"
        data = result[0]
        fields = ['id_cliente', 'nome', 'telefone']
        Funcoes.create_pdf(filename, title, data, fields)
        
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500