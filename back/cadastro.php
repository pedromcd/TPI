<?php
// Conexão com o banco de dados
include 'db_connection.php'; // Certifique-se de que a conexão com o banco de dados está funcionando corretamente

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Recuperando os dados do formulário
    $nome = $_POST['nome'];
    $email = $_POST['email'];
    $senha = $_POST['senha'];

    // Verifica se o email já está cadastrado
    $sql = "SELECT * FROM usuarios WHERE email = :email";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([':email' => $email]);
    $usuario = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($usuario) {
        // Se o email já está cadastrado
        echo "<script>alert('Esse email já está cadastrado!');</script>";
    } else {
        // Se o email não existe, insere o novo usuário no banco
        $senhaHash = password_hash($senha, PASSWORD_DEFAULT); // Criptografa a senha

        $sql = "INSERT INTO usuarios (nome, email, senha) VALUES (:nome, :email, :senha)";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([':nome' => $nome, ':email' => $email, ':senha' => $senhaHash]);

        // Cadastro realizado com sucesso
        echo "<script>alert('Cadastro realizado com sucesso!');</script>";
        echo "<script>window.location.href='login.html';</script>";
    }
}
?>

<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cadastrar Usuário</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(180deg, #9233AA, #3A1444);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .form-signin {
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
        }

        .form-signin h1 {
            font-size: 24px;
            color: #8e44ad;
            margin-bottom: 20px;
        }

        .btn-cancel {
            background-color: #58686f;
            color: white;
            margin-right: 10px;
        }

        .btn-register {
            background-color: #8e44ad;
            color: white;
        }

        .btn-register:hover {
            background-color: #732d91;
        }

        .form-floating > label {
            margin-left: 10px;
        }
    </style>
</head>
<body class="text-center">
    <main>
        <div class="form-signin">
            <!-- Formulário de Cadastro -->
            <form method="POST" action="cadastro.php" id="formCadastro">
                <h1 class="h3 mb-3 fw-normal">Cadastro de Usuário</h1>
                <div class="form-floating mb-3">
                    <input type="text" class="form-control" id="nome" name="nome" placeholder="Nome" required>
                    <label for="nome">Nome</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="email" class="form-control" id="email" name="email" placeholder="Email" required>
                    <label for="email">Email</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="password" class="form-control" id="senha" name="senha" placeholder="Senha" required>
                    <label for="senha">Senha</label>
                </div>
                <div class="d-flex justify-content-between">
                    <button class="btn btn-cancel btn-lg" type="button" onclick="window.location.href='TelaLogin.html'">Cancelar</button>
                    <button class="btn btn-register btn-lg" type="submit" onclick="goTologin()">Cadastrar</button>
                </div>
            </form>
        </div>
    </main>

    <script>
        function goTologin() {
            window.location.href = 'login.html'; 
        }
        // Função de cadastro do usuário
        function cadastrarUsuario(event) {
            event.preventDefault(); // Impede o envio padrão do formulário

            const nome = document.getElementById('nome').value;
            const email = document.getElementById('email').value;
            const senha = document.getElementById('senha').value;

            // Fazendo a requisição para o PHP que irá inserir no banco
            fetch('cadastro.php', {
                method: 'POST',
                body: JSON.stringify({ nome, email, senha }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Usuário cadastrado com sucesso!');
                    window.location.href = 'login.html'; // Redireciona para a tela de login
                } else {
                    alert('Erro ao cadastrar usuário: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro no cadastro!');
            });
        }
    </script>

    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js"></script>
</body>
</html>
