# main.py
import os
from bottle import Bottle, run, static_file
from database import criar_tabelas

criar_tabelas()



app = Bottle()

@app.hook('after_request')
def enable_cors():
    response = app.response
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization'


@app.route('/')
def serve_index():
    return static_file('index.html', root='./static/')

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    
    return static_file(filepath, root='./static/')

from controllers import auth_controller
from controllers import jogo_controller
from controllers import emprestimo_controller

if __name__ == '__main__':
    print("Iniciando a criação das tabelas do banco de dados (se não existirem)...")
    criar_tabelas() 
    print("Tabelas verificadas. Iniciando o servidor...")
    
    run(app, host='localhost', port=8080, debug=True, reloader=True)