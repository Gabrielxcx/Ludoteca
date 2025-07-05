# models/emprestimo.py
import uuid
from datetime import datetime

class Emprestimo:
    """
    Classe que representa a relação de empréstimo entre um Usuário e um Jogo.
    """
    def __init__(self, id_usuario: str, id_jogo: str):
        self._id = str(uuid.uuid4())
        self._id_usuario = id_usuario
        self._id_jogo = id_jogo
        self._data_emprestimo = datetime.now()
        self._data_devolucao = None

    # --- Properties para Encapsulamento ---
    @property
    def id(self): return self._id
    @property
    def id_usuario(self): return self._id_usuario
    @property
    def id_jogo(self): return self._id_jogo
    @property
    def data_emprestimo(self): return self._data_emprestimo
    @property
    def data_devolucao(self): return self._data_devolucao

    def devolver(self):
        """Registra a data e hora da devolução."""
        self._data_devolucao = datetime.now()

    def to_dict(self):
        """Converte o objeto para um dicionário para serialização em JSON."""
        return {
            "id": self._id,
            "id_usuario": self._id_usuario,
            "id_jogo": self._id_jogo,
            # Converte datetime para string no formato ISO para ser compatível com JSON
            "data_emprestimo": self._data_emprestimo.isoformat() if self._data_emprestimo else None,
            "data_devolucao": self._data_devolucao.isoformat() if self._data_devolucao else None,
        }