from database.db import conectar
from datetime import datetime

def emprestar_jogo(id_usuario, id_jogo):
    conn = conectar()
    cursor = conn.cursor()

   
    cursor.execute("UPDATE jogos SET disponivel = 0 WHERE id = ?", (id_jogo,))
    
    data_emprestimo = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO emprestimos (id_usuario, id_jogo, data_emprestimo)
        VALUES (?, ?, ?)
    ''', (id_usuario, id_jogo, data_emprestimo))

    conn.commit()
    conn.close()

def devolver_jogo(id_emprestimo):
    conn = conectar()
    cursor = conn.cursor()

    
    data_devolucao = datetime.now().isoformat()
    cursor.execute("UPDATE emprestimos SET data_devolucao = ? WHERE id = ?", (data_devolucao, id_emprestimo))

   
    cursor.execute("SELECT id_jogo FROM emprestimos WHERE id = ?", (id_emprestimo,))
    row = cursor.fetchone()
    if row:
        id_jogo = row[0]
        cursor.execute("UPDATE jogos SET disponivel = 1 WHERE id = ?", (id_jogo,))

    conn.commit()
    conn.close()

def listar_emprestimos_por_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM emprestimos
        WHERE id_usuario = ?
        ORDER BY data_emprestimo DESC
    ''', (id_usuario,))
    colunas = [col[0] for col in cursor.description]
    emprestimos = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    conn.close()
    return emprestimos

