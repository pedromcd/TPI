<?php
$host = 'localhost';
$db = 'sistema_login';
$user = 'root';  // Usuário do MySQL
$pass = '';      // Senha do MySQL, geralmente vazio no localhost

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Erro de conexão: " . $e->getMessage());
}
?>
