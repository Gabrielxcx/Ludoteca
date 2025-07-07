<!DOCTYPE html>
<html lang="pt-br">
  <head>
    <meta charset="UTF-8" />
    <title>Reserva - {{ jogo["nome"] }}</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    />
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/scripts.js"></script>
  </head>
  <body class="bg-light">
    <div class="container py-5">
      <h2 class="mb-4">Reserva de {{ jogo["nome"] }}</h2>
      <img
        src="{{ jogo['imagem'] }}"
        alt="{{ jogo['nome'] }}"
        class="img-fluid mb-3"
        style="max-height: 300px"
      />
      <p><strong>Descrição:</strong> {{ jogo["descricao"] }}</p>
      <p><strong>Valor do Aluguel:</strong> R$ {{ jogo["valor"] }}</p>
      <p>ID do jogo: {{ jogo_id }}</p>

      <form id="formReserva" method="POST" class="mt-4">
        <div class="mb-3">
          <label for="nome" class="form-label">Nome completo</label>
          <input
            type="text"
            class="form-control"
            id="nome"
            name="nome"
            required
          />
        </div>
        <div class="mb-3">
          <label for="identidade" class="form-label">Identidade</label>
          <input
            type="text"
            class="form-control"
            id="identidade"
            name="identidade"
            required
          />
        </div>
        <button type="submit" class="btn btn-success">Confirmar Reserva</button>
        <a href="/home" class="btn btn-secondary">Cancelar</a>
      </form>
    </div>
    <!-- Modal de confirmação -->
    <div
      class="modal fade"
      id="modalConfirmacao"
      tabindex="-1"
      aria-labelledby="modalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Reserva confirmada!</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Fechar"
            ></button>
          </div>
          <div class="modal-body" id="modalConteudo"></div>
          <div class="modal-footer">
            <a href="/home" class="btn btn-secondary">Voltar à Home</a>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
