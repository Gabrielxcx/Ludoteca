# models/pessoa.py

class Pessoa:
    """
    Classe base que representa uma Pessoa.
    Implementa os conceitos de Abstração e Encapsulamento.
    """
    def __init__(self, nome: str, email: str):
        # Atributos privados para garantir o encapsulamento
        self._nome = nome
        self._email = email

    # --- Encapsulamento com Properties (Getters e Setters) ---
    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, nome: str):
        self._nome = nome

    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, email: str):
        self._email = email

    # --- Polimorfismo: Método a ser sobrescrito pelas classes filhas ---
    def descrever(self) -> str:
        """
        Retorna uma descrição genérica da pessoa.
        Este método é um exemplo de Polimorfismo, pois será sobrescrito na classe filha.
        """
        return f"Pessoa: {self.nome}, Email: {self.email}"