// Fechar o componente de alerta de erro de login
document.addEventListener("DOMContentLoaded", function () {
  const botaoFechar = document.getElementById("fechar-alerta");
  const alerta = document.getElementById("alerta-erro");

  if (botaoFechar && alerta) {
    botaoFechar.addEventListener("click", function () {
      alerta.style.display = "none";
    });
  }
});

// Exibir modal de confirmação ao enviar o formulário de reserva
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("formReserva");

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault(); // Impede o envio padrão do formulário

      const formData = new FormData(form);

      fetch(window.location.pathname, {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.erro) {
            // Exibe alerta com erro vindo do backend
            alert(data.erro);
            return;
          }

          // Preenche o modal com os dados da reserva
          const modalBody = document.getElementById("modalConteudo");
          modalBody.innerHTML = `
            <p><strong>Jogo:</strong> ${data.nome_jogo}</p>
            <p><strong>Nome:</strong> ${data.nome_usuario}</p>
            <p><strong>Identidade:</strong> ${data.identidade}</p>
            <p><strong>Valor:</strong> R$ ${data.valor.toFixed(2)}</p>
          `;

          const modal = new bootstrap.Modal(
            document.getElementById("modalConfirmacao")
          );
          modal.show();
        })
        .catch((error) => {
          console.error("Erro ao enviar a reserva:", error);
          alert("Erro ao enviar a reserva. Tente novamente.");
        });
    });
  }
});
