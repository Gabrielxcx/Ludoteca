<!DOCTYPE html>
<html lang="pt-br">
  <head>
    <meta charset="UTF-8" />
    <title>Bem-vindo à Ludoteca</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    />
    <link rel="stylesheet" href="/static/style.css" />
  </head>
  <body class="bg-light">
    <div class="container py-5">
      <h1 class="text-center mb-4">Ludoteca</h1>
      <p class="lead text-center">
        Bem-vindo à Ludoteca! Aqui você pode explorar, reservar e jogar diversos
        jogos de tabuleiro. Nossa missão é tornar os jogos mais acessíveis e
        proporcionar momentos de diversão para todos!
      </p>

      <h2 class="mt-5">Jogos disponíveis</h2>
      <div class="row mt-3">
        % for id, jogo in enumerate(jogos):
        <div class="col-md-4 mb-4">
          <div class="card h-100">
            <img
              src="{{ jogo['imagem'] }}"
              class="card-img-top"
              alt="{{ jogo['nome'] }}"
            />
            <div class="card-body">
              <h5 class="card-title">{{ jogo["nome"] }}</h5>
              <p class="card-text">{{ jogo["descricao"] }}</p>
              <a href="/reserva/{{ id }}" class="btn btn-primary">Reservar</a>
            </div>
          </div>
        </div>
        % end
      </div>

      <div class="text-center mt-5">
        <a href="/" class="btn btn-outline-secondary">Sair</a>
      </div>
    </div>
  </body>
</html>
