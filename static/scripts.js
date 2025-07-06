document.addEventListener("DOMContentLoaded", function () {
    const botaoFechar = document.getElementById("fechar-alerta");
    const alerta = document.getElementById("alerta-erro");

    if (botaoFechar && alerta) {
        botaoFechar.addEventListener("click", function () {
            alerta.style.display = "none";
        });
    }
});
