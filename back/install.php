<?php
$host = 'localhost';
$user = 'root'; // Altere se necessário
$pass = '';     // Altere se necessário

try {
    // Conecta ao MySQL sem banco definido ainda
    $pdo = new PDO("mysql:host=$host", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Cria banco de dados
    $pdo->exec("CREATE DATABASE IF NOT EXISTS projeto_diario CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci");
    echo "✅ Banco de dados 'projeto_diario' criado ou já existia.<br>";

    // Seleciona o banco de dados
    $pdo->exec("USE projeto_diario");

    // Cria tabela 'usuarios'
    $pdo->exec("
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            senha VARCHAR(255) NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ");
    echo "✅ Tabela 'usuarios' criada.<br>";

    // Cria tabela 'dailys'
    $pdo->exec("
        CREATE TABLE IF NOT EXISTS dailys (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT NOT NULL,
            data DATE NOT NULL,
            oque_foi_feito TEXT NOT NULL,
            oque_fara_amanha TEXT NOT NULL,
            impedimentos TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ");
    echo "✅ Tabela 'dailys' criada.<br>";

    // Cria tabela 'usuarios_dono' (caso haja relação de dono/liderança)
    $pdo->exec("
        CREATE TABLE IF NOT EXISTS usuarios_dono (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT NOT NULL,
            dono_id INT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (dono_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ");
    echo "✅ Tabela 'usuarios_dono' criada.<br>";

} catch (PDOException $e) {
    echo "Erro: " . $e->getMessage();
}
?>