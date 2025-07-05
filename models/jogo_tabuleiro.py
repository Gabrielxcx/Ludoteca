# models/jogo_tabuleiro.py
import uuid

class JogoTabuleiro:
    """
    Classe que representa um Jogo de Tabuleiro na ludoteca.
    Implementa Abstração e Encapsulamento.
    """
    def __init__(self, nome: str, descricao: str, categoria: str, max_jogadores: int):
        self._id = str(uuid.uuid4())
        self._nome = nome
        self._descricao = descricao
        self._categoria = categoria
        self._max_jogadores = max_jogadores
        self._disponivel = True

    # --- Properties para Encapsulamento ---
    @property
    def id(self): return self._id
    @property
    def nome(self): return self._nome
    @property
    def descricao(self): return self._descricao
    @property
    def categoria(self): return self._categoria
    @property
    def max_jogadores(self): return self._max_jogadores
    @property
    def disponivel(self): return self._disponivel

    @disponivel.setter
    def disponivel(self, value: bool):
        self._disponivel = value
        
    def to_dict(self):
        """Converte o objeto para um dicionário para serialização em JSON."""
        return {
            "id": self._id,
            "nome": self._nome,
            "descricao": self._descricao,
            "categoria": self._categoria,
            "max_jogadores": self._max_jogadores,
            "disponivel": self._disponivel,
        }