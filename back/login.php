<?php
session_start();

// Configuração de conexão com o banco de dados
$host = 'localhost';
$db = 'projeto_diario';
$user = 'root';  // Usuário do MySQL
$pass = '';  // Substitua pela senha correta

// Conexão com o banco de dados
try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die('Erro na conexão com o banco: ' . $e->getMessage());
}

// Verificar se o formulário foi enviado
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $usuario = $_POST['usuario'];
    $senha = $_POST['senha'];

    // Consultar o banco de dados para encontrar o usuário
    $sql = "SELECT * FROM usuarios WHERE email = :usuario";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([':usuario' => $usuario]);

    $user = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if ($user && password_verify($senha, $user['senha'])) {
        // Login bem-sucedido
        $_SESSION['usuario'] = $user['email'];
        header('Location: TelaMenuInicial.html');
        exit();
    } else {
        echo "<script>alert('Usuário ou senha inválidos.'); window.location.href='index.html';</script>";
    }
}
?>
