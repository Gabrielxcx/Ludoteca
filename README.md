# Backend da Aplicação de Ludoteca (EP3 - POO)

Este projeto é o backend completo para uma aplicação de gerenciamento de uma biblioteca de jogos de tabuleiro (Ludoteca), desenvolvido como projeto final para a disciplina de Programação Orientada a Objetos.

## Tecnologias e Padrões

*   **Linguagem:** Python
*   **Framework Web:** Bottle
*   **Arquitetura:** Model-View-Controller (MVC)
*   **Persistência de Dados:** Arquivos JSON
*   **Bibliotecas Adicionais:** `werkzeug` (para hashing de senhas)

## Estrutura do Projeto

O projeto segue a estrutura MVC para separação de responsabilidades:

*   `/models`: Contém as classes que representam as entidades do sistema (`Usuario`, `JogoTabuleiro`, `Emprestimo`), demonstrando os 4 pilares da POO (Abstração, Encapsulamento, Herança e Polimorfismo).
*   `/controllers`: Contém a lógica de negócio e as rotas da API, manipulando as requisições HTTP e interagindo com os modelos.
*   `/data`: Armazena os dados da aplicação em formato JSON.
*   `main.py`: Ponto de entrada da aplicação, responsável por configurar e iniciar o servidor web.

## Como Executar

1.  **Instale as dependências:**

    ```bash
    pip install bottle werkzeug
    ```

2.  **Inicie o servidor:**

    Na raiz do projeto (`/ludoteca-backend`), execute o comando:

    ```bash
    python app.py
    ```

    O servidor estará rodando em `http://localhost:8080`.

## Exemplos de Uso da API (usando `curl`)

### 1. Cadastrar um Usuário

```bash
curl -X POST http://localhost:8080/usuarios \
-H "Content-Type: application/json" \
-d '{"nome": "Alice",  "senha": "senha123"}'
