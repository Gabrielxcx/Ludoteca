from bottle import Bottle, run, template, static_file, request, redirect, response
import os
from bottle import TEMPLATE_PATH
import json
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
jogos = [
        {
            'nome': 'Catan',
            'descricao': 'Jogo de estratégia e colonização.',
            'imagem': '/static/catan.jpg',
            'valor': 15.00
        },
        {
            'nome': 'Ticket to Ride',
            'descricao': 'Construção de rotas de trem.',
            'imagem': '/static/ticket.jpg',
            'valor': 12.00
        },
        {
            'nome': 'Dobble',
            'descricao': 'Jogo rápido de reconhecimento visual.',
            'imagem': '/static/dobble.jpg',
            'valor': 10.00
        }
    ]
# Tela de Login /
@app.route('/', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.forms.get('usuario')
        senha = request.forms.get('senha')

        #To do - Realiza o login
        for u in usuarios:
            if u['usuario'] == usuario and u['senha'] == senha:
                return redirect('/home')

        return template('login', erro='Usuário ou senha inválidos')

    return template('login', erro=None)

# Tela de cadastro
@app.route('/cadastro', method=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        novo_usuario = request.forms.get('usuario')
        nova_senha = request.forms.get('senha')

        # To do - Realiza o cadastro e retorna mensagem de erro se o usuário já existir

        # Verifica se já existe
        for u in usuarios:
            if u['usuario'] == novo_usuario:
                return template('cadastro', erro='Nome de usuário já existe')

        # Adiciona novo usuário
        usuarios.append({'usuario': novo_usuario, 'senha': nova_senha})
        return redirect('/home')

    return template('cadastro', erro=None)

# Tela de Home
@app.route('/home', method=['GET', 'POST'])
def home():
    # To do -  Get Jogos
    return template('home', jogos=jogos)

@app.route('/reserva/<jogo_id>', method=['GET', 'POST'])
def reserva(jogo_id):
    # Função auxiliar para buscar o jogo pela posição
    def buscar_jogo_por_id(lista, id_busca):
        for id, jogo in enumerate(lista):
            if id == int(id_busca):
                return jogo
        return {'nome': 'Jogo não encontrado', 'descricao': '', 'imagem': '', 'valor': 0.0}

    jogo = buscar_jogo_por_id(jogos, jogo_id)

    # Inicializa o dicionário de reservas, se ainda não existir
    if not hasattr(app, 'reservas'):
        app.reservas = {}

    if request.method == 'POST':
        nome = request.forms.get('nome')
        identidade = request.forms.get('identidade')

        response.content_type = 'application/json'

        # Verifica se o jogo já foi reservado
        if app.reservas.get(jogo_id):
            return json.dumps({
                'erro': 'Este jogo já foi reservado por outra pessoa.'
            })
        else:
            # Armazena a reserva
            app.reservas[jogo_id] = {
                'nome_jogo': jogo['nome'],
                'valor': jogo['valor'],
                'nome_usuario': nome,
                'identidade': identidade,
                'reservado': True
            }
            return json.dumps(app.reservas[jogo_id])

    # GET: renderiza o template de reserva com informações se já estiver reservado
    reservado = app.reservas.get(jogo_id) if hasattr(app, 'reservas') else None
    return template('reserva', jogo=jogo, jogo_id=jogo_id, reservado=reservado)
if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True, reloader=True)
