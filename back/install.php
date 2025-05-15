<?php
include 'db_connection.php';

// Criação do banco de dados se não existir
$sql = "CREATE DATABASE IF NOT EXISTS sistema_login";
$pdo->exec($sql);

// Seleciona o banco de dados
$pdo->exec("USE sistema_login");

// Criação da tabela 'usuarios' se não existir
$sql = "
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        senha VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
";
$pdo->exec($sql);

// Inserir um usuário de exemplo
$email = 'usuario@exemplo.com';
$senha = password_hash('senha123', PASSWORD_DEFAULT);  // Usando password_hash para segurança
$sql = "INSERT INTO usuarios (email, senha) VALUES (:email, :senha)";
$stmt = $pdo->prepare($sql);
$stmt->execute([':email' => $email, ':senha' => $senha]);

echo "Banco de dados e tabela criados com sucesso!";
?>
