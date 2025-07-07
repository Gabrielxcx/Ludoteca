
import json
from bottle import get, post, put, delete, request, response, abort
from models.jogo_tabuleiro import JogoTabuleiro
from controllers.auth_controller import login_required 

DATA_FILE = './data/jogos.json'


def load_jogos():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_jogos(jogos):
    with open(DATA_FILE, 'w') as f:
        json.dump(jogos, f, indent=4)



@get('/jogos')
def list_jogos():
    """Lista todos os jogos. Rota pública."""
    return {"jogos": load_jogos()}

@get('/jogos/<id>')
def get_jogo(id):
    """Busca um jogo específico pelo ID. Rota pública."""
    jogos = load_jogos()
    jogo = next((j for j in jogos if j['id'] == id), None)
    if jogo:
        return jogo
    abort(404, 'Jogo não encontrado.')

@post('/jogos')
@login_required(role="admin")
def add_jogo():
    """Adiciona um novo jogo. Rota protegida para administradores."""
    data = request.json
    if not all(k in data for k in ['nome', 'descricao', 'categoria', 'max_jogadores']):
        abort(400, 'Dados incompletos para adicionar o jogo.')

    novo_jogo = JogoTabuleiro(
        nome=data['nome'],
        descricao=data['descricao'],
        categoria=data['categoria'],
        max_jogadores=data['max_jogadores']
    )
    
    jogos = load_jogos()
    jogos.append(novo_jogo.to_dict())
    save_jogos(jogos)
    
    response.status = 201
    return novo_jogo.to_dict()

@put('/jogos/<id>')
@login_required(role="admin")
def update_jogo(id):
    """Atualiza um jogo existente. Rota protegida para administradores."""
    jogos = load_jogos()
    jogo_idx, jogo_data = next(((i, j) for i, j in enumerate(jogos) if j['id'] == id), (None, None))
    
    if not jogo_data:
        abort(404, 'Jogo não encontrado.')
        
    update_data = request.json
    
    
    for key, value in update_data.items():
        if key in jogo_data and key != 'id': 
            jogo_data[key] = value
            
    jogos[jogo_idx] = jogo_data
    save_jogos(jogos)
    return jogo_data

@delete('/jogos/<id>')
@login_required(role="admin")
def remove_jogo(id):
    """Remove um jogo. Rota protegida para administradores."""
    jogos = load_jogos()
    jogo_encontrado = any(j['id'] == id for j in jogos)
    
    if not jogo_encontrado:
        abort(404, 'Jogo não encontrado.')
        
    
    jogos_filtrados = [j for j in jogos if j['id'] != id]
    save_jogos(jogos_filtrados)
    
    response.status = 204 
    return