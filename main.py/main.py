import os
import json
from bottle import Bottle, run, response

if not os.path.exists('./data'):
    os.makedirs('./data')

files_to_create = ['./data/usuarios.json', './data/jogos.json', './data/emprestimos.json']
for file_path in files_to_create:
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

app = Bottle()

@app.hook('after_request')
def enable_cors():
    """Adiciona cabeçalhos CORS a todas as respostas."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization'

from controllers import auth_controller
from controllers import jogo_controller
from controllers import emprestimo_controller


if __name__ == '__main__':
    
    run(app, host='localhost', port=8080, debug=True, reloader=True)
