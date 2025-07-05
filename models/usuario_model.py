from database.db import conectar

def criar_usuario(nome, email, senha_hash, role='usuario'):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, email, senha_hash, role)
        VALUES (?, ?, ?, ?)
    ''', (nome, email, senha_hash, role))
    conn.commit()
    conn.close()

def buscar_usuario_por_email(email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        colunas = ['id', 'nome', 'email', 'senha_hash', 'role']
        return dict(zip(colunas, row))
    return None

def buscar_usuario_por_id(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
    row = cursor.fetchone()
    conn.close()
    if row:
        colunas = ['id', 'nome', 'email', 'senha_hash', 'role']
        return dict(zip(colunas, row))
    return None
