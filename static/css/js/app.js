// app.js

document.addEventListener('DOMContentLoaded', () => {
    
    const API_URL = 'http://localhost:8080';
    const appContent = document.getElementById('app-content');

    
    const navLinks = {
        jogos: document.getElementById('nav-jogos'),
        meusEmprestimos: document.getElementById('nav-meus-emprestimos'),
        addJogo: document.getElementById('nav-add-jogo'),
        login: document.getElementById('nav-login'),
        registrar: document.getElementById('nav-registrar'),
        logout: document.getElementById('nav-logout'),
    };

    
    const getToken = () => localStorage.getItem('authToken');
    const getUser = () => JSON.parse(localStorage.getItem('authUser'));
    const setAuthData = (token, user) => {
        localStorage.setItem('authToken', token);
        localStorage.setItem('authUser', JSON.stringify(user));
    };
    const clearAuthData = () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('authUser');
    };

    
    const apiFetch = async (endpoint, options = {}) => {
        const token = getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };
        if (token) {
            headers['Authorization'] = token;
        }

        const response = await fetch(`${API_URL}${endpoint}`, { ...options, headers });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.body || 'Ocorreu um erro na requisição.');
        }

        
        if (response.status === 204) {
            return;
        }
        
        return response.json();
    };

    

    const renderLoginPage = () => {
        appContent.innerHTML = `
            <div class="form-container">
                <h2>Login</h2>
                <form id="login-form">
                    <div class="form-group">
                        <label for="email">Email:</label>
                        <input type="email" id="email" required>
                    </div>
                    <div class="form-group">
                        <label for="senha">Senha:</label>
                        <input type="password" id="senha" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Entrar</button>
                </form>
            </div>
        `;
        document.getElementById('login-form').addEventListener('submit', handleLogin);
    };

    const renderRegisterPage = () => {
        appContent.innerHTML = `
            <div class="form-container">
                <h2>Registrar</h2>
                <form id="register-form">
                    <div class="form-group">
                        <label for="nome">Nome:</label>
                        <input type="text" id="nome" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email:</label>
                        <input type="email" id="email" required>
                    </div>
                    <div class="form-group">
                        <label for="senha">Senha:</label>
                        <input type="password" id="senha" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Registrar</button>
                </form>
            </div>
        `;
        document.getElementById('register-form').addEventListener('submit', handleRegister);
    };
    
    const renderJogosPage = async () => {
        try {
            const { jogos } = await apiFetch('/jogos');
            const user = getUser();

            let content = '<h2>Jogos Disponíveis</h2>';
            if (jogos.length === 0) {
                content += '<p>Nenhum jogo cadastrado ainda.</p>';
            } else {
                content += '<div class="card-container">';
                jogos.forEach(jogo => {
                    content += `
                        <div class="card">
                            <h3>${jogo.nome}</h3>
                            <p><strong>Categoria:</strong> ${jogo.categoria}</p>
                            <p>${jogo.descricao}</p>
                            <p><strong>Jogadores:</strong> Até ${jogo.max_jogadores}</p>
                            <p class="card-status ${jogo.disponivel ? 'status-disponivel' : 'status-emprestado'}">
                                ${jogo.disponivel ? 'Disponível' : 'Emprestado'}
                            </p>
                            <div class="actions">
                                ${user && jogo.disponivel ? `<button class="btn btn-success" data-action="emprestar" data-id="${jogo.id}">Emprestar</button>` : ''}
                                ${user && user.role === 'admin' ? `
                                    <button class="btn btn-secondary" data-action="editar-jogo" data-id="${jogo.id}">Editar</button>
                                    <button class="btn btn-danger" data-action="excluir-jogo" data-id="${jogo.id}">Excluir</button>
                                ` : ''}
                            </div>
                        </div>
                    `;
                });
                content += '</div>';
            }
            appContent.innerHTML = content;
        } catch (error) {
            appContent.innerHTML = `<p style="color:red;">Erro ao carregar jogos: ${error.message}</p>`;
        }
    };

    const renderMeusEmprestimosPage = async () => {
        try {
            const { emprestimos } = await apiFetch('/usuarios/me/emprestimos');
            const { jogos } = await apiFetch('/jogos'); 

            let content = '<h2>Meus Empréstimos</h2>';
            if (emprestimos.length === 0) {
                content += '<p>Você não possui nenhum empréstimo.</p>';
            } else {
                 content += '<div class="card-container">';
                emprestimos.forEach(emp => {
                    const jogoInfo = jogos.find(j => j.id === emp.id_jogo);
                    const nomeJogo = jogoInfo ? jogoInfo.nome : 'Jogo não encontrado';
                    const dataEmp = new Date(emp.data_emprestimo).toLocaleDateString('pt-BR');
                    const dataDev = emp.data_devolucao ? new Date(emp.data_devolucao).toLocaleDateString('pt-BR') : null;

                    content += `
                        <div class="card">
                            <h3>${nomeJogo}</h3>
                            <p><strong>Data do Empréstimo:</strong> ${dataEmp}</p>
                            <p class="card-status ${!dataDev ? 'status-emprestado' : 'status-disponivel'}">
                                <strong>Status:</strong> ${!dataDev ? 'Emprestado' : `Devolvido em ${dataDev}`}
                            </p>
                            <div class="actions">
                                ${!dataDev ? `<button class="btn btn-primary" data-action="devolver" data-id="${emp.id}">Devolver</button>` : ''}
                            </div>
                        </div>
                    `;
                });
                content += '</div>';
            }
             appContent.innerHTML = content;
        } catch (error) {
            appContent.innerHTML = `<p style="color:red;">Erro ao carregar empréstimos: ${error.message}</p>`;
        }
    };

    const renderAddJogoPage = () => {
         appContent.innerHTML = `
            <div class="form-container">
                <h2>Adicionar Novo Jogo</h2>
                <form id="add-jogo-form">
                     <div class="form-group">
                        <label for="nome">Nome:</label>
                        <input type="text" id="nome" required>
                    </div>
                     <div class="form-group">
                        <label for="descricao">Descrição:</label>
                        <textarea id="descricao" required></textarea>
                    </div>
                     <div class="form-group">
                        <label for="categoria">Categoria:</label>
                        <input type="text" id="categoria" required>
                    </div>
                     <div class="form-group">
                        <label for="max_jogadores">Máx. de Jogadores:</label>
                        <input type="number" id="max_jogadores" required min="1">
                    </div>
                    <button type="submit" class="btn btn-primary">Adicionar Jogo</button>
                </form>
            </div>
        `;
        document.getElementById('add-jogo-form').addEventListener('submit', handleAddJogo);
    };


    const handleLogin = async (e) => {
        e.preventDefault();
        const email = e.target.elements.email.value;
        const senha = e.target.elements.senha.value;
        try {
            const data = await apiFetch('/login', {
                method: 'POST',
                body: JSON.stringify({ email, senha }),
            });
            setAuthData(data.token, data.user);
            updateNav();
            navigateTo('/jogos');
        } catch (error) {
            alert(`Erro no login: ${error.message}`);
        }
    };
    
    const handleRegister = async (e) => {
        e.preventDefault();
        const nome = e.target.elements.nome.value;
        const email = e.target.elements.email.value;
        const senha = e.target.elements.senha.value;
        try {
            await apiFetch('/usuarios', {
                method: 'POST',
                body: JSON.stringify({ nome, email, senha }),
            });
            alert('Usuário registrado com sucesso! Faça o login.');
            navigateTo('/login');
        } catch (error) {
            alert(`Erro no registro: ${error.message}`);
        }
    };
    
    const handleLogout = () => {
        clearAuthData();
        updateNav();
        navigateTo('/login');
    };

    const handleAddJogo = async (e) => {
        e.preventDefault();
        const form = e.target;
        const jogoData = {
            nome: form.elements.nome.value,
            descricao: form.elements.descricao.value,
            categoria: form.elements.categoria.value,
            max_jogadores: parseInt(form.elements.max_jogadores.value),
        };
        try {
            await apiFetch('/jogos', {
                method: 'POST',
                body: JSON.stringify(jogoData),
            });
            alert('Jogo adicionado com sucesso!');
            navigateTo('/jogos');
        } catch (error) {
             alert(`Erro ao adicionar jogo: ${error.message}`);
        }
    };
    
    const handleAppClick = async (e) => {
        const action = e.target.dataset.action;
        const id = e.target.dataset.id;

        if (!action) return;

        try {
            switch (action) {
                case 'emprestar':
                    if (confirm('Deseja realmente emprestar este jogo?')) {
                        await apiFetch('/emprestimos', {
                            method: 'POST',
                            body: JSON.stringify({ id_jogo: id }),
                        });
                        alert('Jogo emprestado com sucesso!');
                        renderJogosPage(); // Recarrega a página de jogos
                    }
                    break;
                case 'devolver':
                     if (confirm('Deseja realmente devolver este jogo?')) {
                        await apiFetch(`/emprestimos/${id}/devolver`, { method: 'PUT' });
                        alert('Jogo devolvido com sucesso!');
                        renderMeusEmprestimosPage(); // Recarrega a página de empréstimos
                    }
                    break;
                case 'excluir-jogo':
                    if (confirm('ATENÇÃO: Deseja realmente excluir este jogo? Esta ação é irreversível.')) {
                        await apiFetch(`/jogos/${id}`, { method: 'DELETE' });
                        alert('Jogo excluído com sucesso!');
                        renderJogosPage();
                    }
                    break;
            
            }
        } catch (error) {
            alert(`Erro: ${error.message}`);
        }
    };

   

    const navigateTo = (path) => {
        window.location.hash = path;
    };
    
    const router = () => {
        const path = window.location.hash.replace('#', '') || '/jogos';
        const user = getUser();
        
       
        if ((path === '/emprestimos' || path === '/adicionar-jogo') && !user) {
            navigateTo('/login');
            return;
        }
        if (path === '/adicionar-jogo' && user.role !== 'admin') {
            alert('Acesso negado.');
            navigateTo('/jogos');
            return;
        }

        switch (path) {
            case '/login':
                renderLoginPage();
                break;
            case '/registrar':
                renderRegisterPage();
                break;
            case '/jogos':
                renderJogosPage();
                break;
            case '/emprestimos':
                renderMeusEmprestimosPage();
                break;
            case '/adicionar-jogo':
                renderAddJogoPage();
                break;
            default:
                renderJogosPage();
        }
    };
    
    const updateNav = () => {
        const user = getUser();
        if (user) {
            navLinks.login.classList.add('hidden');
            navLinks.registrar.classList.add('hidden');
            navLinks.logout.classList.remove('hidden');
            navLinks.meusEmprestimos.classList.remove('hidden');
            
            if (user.role === 'admin') {
                navLinks.addJogo.classList.remove('hidden');
            } else {
                navLinks.addJogo.classList.add('hidden');
            }
        } else {
            navLinks.login.classList.remove('hidden');
            navLinks.registrar.classList.remove('hidden');
            navLinks.logout.classList.add('hidden');
            navLinks.meusEmprestimos.classList.add('hidden');
            navLinks.addJogo.classList.add('hidden');
        }
    };

    
    navLinks.logout.addEventListener('click', handleLogout);
    appContent.addEventListener('click', handleAppClick); 
    window.addEventListener('hashchange', router);
    
 
    updateNav();
    router();
});