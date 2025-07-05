# controllers/auth_controller.py
import json
from functools import wraps
from bottle import post, request, response, abort
from models.usuario import Usuario

DATA_FILE = './data/usuarios.json'


def load_users():
    """Carrega os usuários do arquivo JSON."""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    """Salva a lista de usuários no arquivo JSON."""
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)


def login_required(role="regular"):
    """
    Decorator para proteger rotas. Verifica um 'token' simples no cabeçalho
    e o nível de permissão do usuário.
    Para este projeto, o token será no formato 'user_id:user_role'.
    Ex: Authorization: 4e3e3b7d-62f4-4a7b-8b3c-0e7d3e3f3b7d:admin
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                abort(401, 'Nenhum token de autorização fornecido.')

            try:
                user_id, user_role = auth_header.split(':')
            except ValueError:
                abort(401, 'Formato de token inválido.')

            
            users_data = load_users()
            user_exists = any(u['id'] == user_id and u['role'] == user_role for u in users_data)
            
            if not user_exists:
                abort(401, 'Token inválido ou usuário não encontrado.')

           
            if role == "admin" and user_role != "admin":
                abort(403, 'Acesso negado: Requer permissão de administrador.')

            
            request.user = {'id': user_id, 'role': user_role}
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


@post('/usuarios')
def register_user():
    """
    Rota para cadastrar um novo usuário.
    POST /usuarios
    Body: {"nome": "...", "email": "...", "senha": "..."}
    """
    data = request.json
    if not all(k in data for k in ['nome', 'email', 'senha']):
        abort(400, 'Dados incompletos para cadastro.')

    users_data = load_users()
    if any(u['email'] == data['email'] for u in users_data):
        abort(409, 'Este email já está cadastrado.')

    
    novo_usuario = Usuario(
        nome=data['nome'],
        email=data['email'],
        senha=data['senha'],
        role=data.get('role', 'regular') 
    )
    
   
    users_data.append(novo_usuario.to_dict(include_sensitive_data=True))
    save_users(users_data)
    
    response.status = 201
    
    return novo_usuario.to_dict()


@post('/login')
def login_user():
    """
    Rota para login.
    POST /login
    Body: {"email": "...", "senha": "..."}
    """
    data = request.json
    if not data or 'email' not in data or 'senha' not in data:
        abort(400, 'Email e senha são obrigatórios.')

    users_data = load_users()
    user_data = next((u for u in users_data if u['email'] == data['email']), None)

    if not user_data:
        abort(404, 'Usuário não encontrado.')

    
    usuario = Usuario.from_dict(user_data)
    
    if not usuario.check_senha(data['senha']):
        abort(401, 'Senha incorreta.')

    token = f"{usuario.id}:{usuario.role}"
    
    return {
        "message": "Login bem-sucedido!",
        "user": usuario.to_dict(),
        "token": token
    }