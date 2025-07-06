<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Login - Ludoteca</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/style.css">
    <script src="/static/scripts.js"></script>
</head>
<body class="d-flex justify-content-center align-items-center vh-100 bg-light">

    <div class="card p-4 shadow login-card">
        <h3 class="mb-4 text-center">Login - Ludoteca</h3>
        % if erro:
            <div class="alert alert-danger" id="alerta-erro">
                {{ erro }}
                <button type="button" id="fechar-alerta" class="btn-close" style="float:right;" aria-label="Fechar"></button>
            </div>
        % end


        <form method="POST">
            <div class="mb-3">
                <label for="usuario" class="form-label">Usuário</label>
                <input type="text" class="form-control" id="usuario" name="usuario" required>
            </div>
            <div class="mb-3">
                <label for="senha" class="form-label">Senha</label>
                <input type="password" class="form-control" id="senha" name="senha" required>
            </div>
            <div class="d-flex justify-content-between">
                <button type="submit" class="btn btn-primary">Entrar</button>
                <a href="/cadastro" class="btn btn-outline-secondary">Cadastrar</a>
            </div>
        </form>
    </div>

</body>
</html>
