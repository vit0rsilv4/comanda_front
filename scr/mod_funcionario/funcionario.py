from flask import Blueprint, render_template, request, redirect, url_for, jsonify, send_file
import requests
from mod_login.login import validaSessao, validaToken
from funcoes import Funcoes
from settings import getHeadersAPI, ENDPOINT_FUNCIONARIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from funcoes import Funcoes
bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

''' rotas dos formulários '''
@bp_funcionario.route('/', methods=['GET', 'POST'])
@validaSessao
def formListaFuncionario():
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI())
        result = response.json()
        print(result)

        if (response.status_code != 200):    
            raise Exception(result)
        
        return render_template('formListaFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

""" restante dos dados omitidos """

@bp_funcionario.route('/form-funcionario/',)
def formFuncionario():
    return render_template('formFuncionario.html')

@bp_funcionario.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        id_funcionario = 0
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        senha = Funcoes.get_password_hash(request.form['senha'])
        
        # monta o JSON para envio a API
        payload = {
            'id_funcionario': id_funcionario,
            'nome': nome,
            'matricula': matricula,
            'cpf': cpf,
            'telefone': telefone,
            'grupo': grupo,
            'senha': senha
        }
        
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI(), json=payload)
        result = response.json()
        print(result)  # [{'msg': 'Cadastrado com sucesso!', 'id': 13}, 200]
        print(response.status_code)  # 200
        
        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)
        
        return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
    
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])
    
@bp_funcionario.route("/form-edit-funcionario", methods=['POST'])
@validaToken
def formEditFuncionario():
    try:
        # ID enviado via FORM
        id_funcionario = request.form['id']

        # executa o verbo GET da API buscando somente o funcionário selecionado,
        # obtendo o JSON do retorno
        response = requests.get(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200:
            raise Exception(result)

        # renderiza o form passando os dados retornados
        return render_template('formFuncionario.html', result=result[0])

    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/edit', methods=['POST'])
def edit():
    try:
        # Dados enviados via FORM
        id_funcionario = request.form['id']
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        senha = Funcoes.cifraSenha(request.form['senha'])

        # Monta o JSON para envio a API
        payload = {
            'id_funcionario': id_funcionario,
            'nome': nome,
            'matricula': matricula,
            'cpf': cpf,
            'telefone': telefone,
            'grupo': grupo,
            'senha': senha
        }

        # Executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI(), json=payload)
        result = response.json()

        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)

        return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))

    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/delete', methods=['POST'])
def delete():
    try:
        # Dados enviados via FORM
        id_funcionario = request.form['id']

        # Executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)

        return jsonify(erro=False, msg=result[0])

    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])
    
def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2.0, height - 50, "Funcionarios Cadastrados")

    response = requests.get(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI())
    result = response.json()

    if response.status_code != 200:    
        raise Exception(result)
    
    funcionarios = result[0]
    c.setFont("Helvetica", 12)
    y_position = height - 100

    for funcionario in funcionarios:
        nome = funcionario.get('nome', 'Nome não disponível')
        grupo = funcionario.get('grupo', 'Cargo não disponível')
        matricula = funcionario.get('matricula', 'Matricula não disponível')
        telefone = funcionario.get('telefone', 'Telefone não disponível')

        c.drawString(100, y_position, f"Nome: {nome}")
        y_position -= 20
        c.drawString(100, y_position, f"Cargo: {grupo}")
        y_position -= 20 
        c.drawString(100, y_position, f"Matricula: {matricula}")
        y_position -= 20
        c.drawString(100, y_position, f"Telefone: {telefone}")
        y_position -= 20

        c.setStrokeColor(colors.red)
        c.line(100, y_position, 500, y_position)

        y_position -= 20  # Espaçamento entre os funcionários

        if y_position < 100:
            c.showPage()
            y_position = height - 100
            c.setFont("Helvetica", 12)

    c.showPage()
    c.save()
    
@bp_funcionario.route('/generate_pdf', methods=['GET'])
def generate_pdf():
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200:
            raise Exception(result)

        filename = "funcionarios_cadastrados.pdf"
        title = "Funcionarios Cadastrados"
        data = result[0]
        fields = ['nome', 'grupo', 'matricula', 'telefone']
        Funcoes.create_pdf(filename, title, data, fields)
        
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500