from flask import Blueprint, redirect, render_template, request, jsonify, send_file, url_for
import requests
import base64
from mod_login.login import validaSessao, validaToken
from funcoes import Funcoes
from settings import ENDPOINT_PRODUTO, getHeadersAPI
bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

''' rotas dos formulários '''
@bp_produto.route('/', methods=['GET', 'POST'])
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
@validaToken
def formProduto():
    return render_template('formProduto.html')

@bp_produto.route("/form-edit-produto", methods=['POST', 'GET'])
@validaToken
def formEditProduto():
    try:
        id_produto = request.form['id']

        response = requests.get(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI())
        result = response.json()
        
        if response.status_code != 200:
            raise Exception(result)
        
        return render_template('formProduto.html', result=result)
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])



@bp_produto.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        id_produto = 0
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor_unitario = request.form['valor_unitario']
        
        # converte em base64
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")
        
        # monta o JSON para envio a API
        payload = {
            'id_produto': id_produto,
            'nome': nome,
            'descricao': descricao,
            'foto': foto,
            'valor_unitario': valor_unitario
        }
        
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_PRODUTO, headers=getHeadersAPI(), json=payload)
        result = response.json()
        print(result)
        
        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)
        
        return redirect(url_for('produto.formListaProduto', msg=result[0]))
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/edit', methods=['POST'])
@validaToken
def edit():
    try:
        # dados enviados via FORM
        id_produto = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor_unitario = request.form['valor_unitario']
        
        # converte em base64
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")
        
        # monta o JSON para envio a API
        payload = {
            'id_produto': id_produto,
            'nome': nome,
            'descricao': descricao,
            'foto': foto,
            'valor_unitario': valor_unitario
        }
        
        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI(), json=payload)
        result = response.json()
        
        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)
        
        return redirect(url_for('produto.formListaProduto', msg=result[0]))
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])
    
@bp_produto.route('/delete', methods=['POST'])
@validaToken
def delete():
    try:
        # dados enviados via FORM
        id_produto = request.form['id_produto']
        print("ADSADSADASDASDASDAS")
        print(id_produto)
        
        # executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI())
        result = response.json()
        
        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)
        
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])
    
@bp_produto.route('/generate_pdf', methods=['GET'])
def generate_pdf():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200:
            raise Exception(result)

        filename = "produtos_cadastrados.pdf"
        title = "Produtos Cadastrados"
        data = result[0]
        fields = ['nome', 'descricao', 'valor_unitario', 'foto']
        Funcoes.create_pdf(filename, title, data, fields)
        
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500