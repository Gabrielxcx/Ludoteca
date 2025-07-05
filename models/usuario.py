# models/usuario.py
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
# A linha abaixo é a correção principal: importar a classe base Pessoa
from models.pessoa import Pessoa 

class Usuario(Pessoa):
   
    def __init__(self, nome: str, email: str, senha: str, role: str = "regular"):
        # Chama o construtor da classe pai (Pessoa) para inicializar nome e email
        super().__init__(nome, email)
        
        # Atributos específicos da classe filha Usuario
        self._id = str(uuid.uuid4())
        self._senha_hash = ""
        self.set_senha(senha) # Usa o método para gerar o hash na criação
        
        if role not in ["admin", "regular"]:
            raise ValueError("A role deve ser 'admin' ou 'regular'")
        self._role = role

    @property
    def id(self) -> str:
        return self._id

    @property
    def role(self) -> str:
        return self._role

    
    def set_senha(self, senha_texto: str):
        """Gera e armazena o hash da senha."""
        self._senha_hash = generate_password_hash(senha_texto)

    def check_senha(self, senha_texto: str) -> bool:
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self._senha_hash, senha_texto)

    
    def descrever(self) -> str:
        """
        Retorna uma descrição específica para o Usuário, sobrescrevendo
        o método 'descrever' da classe Pessoa.
        """
        return f"Usuário: {self.nome}, Email: {self.email}, Role: {self.role}"
    
    def to_dict(self, include_sensitive_data=False):
        """Converte o objeto para um dicionário, para fácil serialização em JSON."""
        data = {
            "id": self._id,
            "nome": self._nome,
            "email": self._email,
            "role": self._role
        }
        if include_sensitive_data:
        
            data["_senha_hash"] = self._senha_hash
        return data
    
    @staticmethod
    def from_dict(data: dict):
        """
        Cria uma instância de Usuario a partir de um dicionário (usado ao carregar do JSON).
        Este é um método de fábrica estático.
        """
        usuario = Usuario(nome=data['nome'], email=data['email'], senha="dummy_password")
        usuario._id = data['id']
        usuario._role = data['role']
        usuario._senha_hash = data['_senha_hash'] # Carrega o hash diretamente do arquivo
        return usuario