# main.py
import os
import json
from bottle import Bottle, run, response

# --- Configuração Inicial ---
# Cria a pasta 'data' e os arquivos JSON se não existirem.
# Isso garante que a aplicação não quebre na primeira execução.
if not os.path.exists('./data'):
    os.makedirs('./data')

files_to_create = ['./data/usuarios.json', './data/jogos.json', './data/emprestimos.json']
for file_path in files_to_create:
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

# --- Instância da Aplicação ---
# É uma boa prática usar uma instância de Bottle em vez da global
app = Bottle()

# --- Hook para CORS ---
# Permite que um frontend em outro domínio (ex: localhost:3000)
# acesse esta API (ex: localhost:8080)
@app.hook('after_request')
def enable_cors():
    """Adiciona cabeçalhos CORS a todas as respostas."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization'

# --- Importação dos Controllers para Registrar as Rotas ---
# Ao importar, o código dentro de cada controller é executado,
# e as rotas são registradas na instância padrão do Bottle.
from controllers import auth_controller
from controllers import jogo_controller
from controllers import emprestimo_controller

# --- Ponto de Entrada Principal ---
if __name__ == '__main__':
    # O reloader=True faz o servidor reiniciar automaticamente após salvar alterações no código.
    # O debug=True fornece páginas de erro detalhadas.
    # Precisamos passar a instância 'app' para o run() para que ele use nossas rotas.
    run(app, host='localhost', port=8080, debug=True, reloader=True)