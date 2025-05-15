<?php
session_start(); // Inicia a sessão

if (!isset($_SESSION['usuario'])) {
    header('Location: login.php'); // Se não estiver logado, redireciona para a tela de login
    exit;
}

echo "Bem-vindo, " . $_SESSION['usuario'] . "!";
echo "<br><a href='logout.php'>Sair</a>";
?>
