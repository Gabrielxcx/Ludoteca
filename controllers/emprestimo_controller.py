# controllers/emprestimo_controller.py
import json
from bottle import post, put, get, request, response, abort
from models.emprestimo import Emprestimo
from controllers.auth_controller import login_required

EMPRESTIMOS_FILE = './data/emprestimos.json'
JOGOS_FILE = './data/jogos.json'


def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)



@post('/emprestimos')
@login_required(role="regular") 
def realizar_emprestimo():
    """
    Realiza um empréstimo de um jogo.
    POST /emprestimos
    Body: {"id_jogo": "..."}
    Header: Authorization: <user_id>:<user_role>
    """
    data = request.json
    id_jogo = data.get('id_jogo')
    if not id_jogo:
        abort(400, "O 'id_jogo' é obrigatório.")
        
    id_usuario = request.user['id'] 
    
    jogos = load_data(JOGOS_FILE)
    jogo_idx, jogo = next(((i, j) for i, j in enumerate(jogos) if j['id'] == id_jogo), (None, None))
    
    if not jogo:
        abort(404, "Jogo não encontrado.")
    
    if not jogo['disponivel']:
        abort(409, "Jogo indisponível para empréstimo.")
        
    novo_emprestimo = Emprestimo(id_usuario=id_usuario, id_jogo=id_jogo)
    emprestimos = load_data(EMPRESTIMOS_FILE)
    emprestimos.append(novo_emprestimo.to_dict())
    save_data(emprestimos, EMPRESTIMOS_FILE)
    
    
    jogo['disponivel'] = False
    jogos[jogo_idx] = jogo
    save_data(jogos, JOGOS_FILE)
    
    response.status = 201
    return novo_emprestimo.to_dict()

@put('/emprestimos/<id_emprestimo>/devolver')
@login_required(role="regular")
def devolver_jogo(id_emprestimo):
    """
    Registra a devolução de um jogo.
    PUT /emprestimos/<id_emprestimo>/devolver
    Header: Authorization: <user_id>:<user_role>
    """
    emprestimos = load_data(EMPRESTIMOS_FILE)
    emp_idx, emprestimo = next(((i, e) for i, e in enumerate(emprestimos) if e['id'] == id_emprestimo), (None, None))

    if not emprestimo:
        abort(404, "Empréstimo não encontrado.")

    
    if emprestimo['id_usuario'] != request.user['id'] and request.user['role'] != 'admin':
        abort(403, "Você não tem permissão para realizar esta ação.")
        
    if emprestimo.get('data_devolucao'):
        abort(409, "Este jogo já foi devolvido.")
    
    
    from datetime import datetime
    emprestimo['data_devolucao'] = datetime.now().isoformat()
    emprestimos[emp_idx] = emprestimo
    save_data(emprestimos, EMPRESTIMOS_FILE)
    
    
    jogos = load_data(JOGOS_FILE)
    id_jogo = emprestimo['id_jogo']
    jogo_idx, jogo = next(((i, j) for i, j in enumerate(jogos) if j['id'] == id_jogo), (None, None))
    
    if jogo:
        jogo['disponivel'] = True
        jogos[jogo_idx] = jogo
        save_data(jogos, JOGOS_FILE)
        
    return emprestimo

@get('/usuarios/me/emprestimos')
@login_required(role="regular")
def listar_meus_emprestimos():
    """
    Lista todos os empréstimos (ativos e passados) do usuário logado.
    GET /usuarios/me/emprestimos
    Header: Authorization: <user_id>:<user_role>
    """
    id_usuario = request.user['id']
    emprestimos = load_data(EMPRESTIMOS_FILE)
    
    meus_emprestimos = [e for e in emprestimos if e['id_usuario'] == id_usuario]
    
    return {"emprestimos": meus_emprestimos}