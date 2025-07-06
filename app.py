from bottle import Bottle, run, template, static_file, request, redirect
import os
from bottle import TEMPLATE_PATH
app = Bottle()

# importa o arquivo CSS
@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')

# Simula um banco de dados de usuários
usuarios = [
    {'usuario': 'admin', 'senha': '123', 'nivel': 'admin'},
    {'usuario': 'joao', 'senha': 'abc', 'nivel': 'regular'},
    {'usuario': 'maria', 'senha': 'xyz', 'nivel': 'usuario'},
]
# Tela de Login /
@app.route('/', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.forms.get('usuario')
        senha = request.forms.get('senha')

        #Realiza o login caso o usuário esteja na lista de usuários
        for u in usuarios:
            if u['usuario'] == usuario and u['senha'] == senha:
                return f"<h2>Bem-vindo, {usuario}!</h2>"

        return template('login', erro='Usuário ou senha inválidos')

    return template('login', erro=None)

# Tela de cadastro
@app.route('/cadastro', method=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        novo_usuario = request.forms.get('usuario')
        nova_senha = request.forms.get('senha')

        # Verifica se já existe
        for u in usuarios:
            if u['usuario'] == novo_usuario:
                return template('cadastro', erro='Nome de usuário já existe')

        # Adiciona novo usuário
        usuarios.append({'usuario': novo_usuario, 'senha': nova_senha})
        return redirect('/')

    return template('cadastro', erro=None)

# Inicia o servidor
run(app, host='localhost', port=8080, debug=True, reloader=True)
