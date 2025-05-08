<?php
session_start();
session_destroy();  // Destroi a sessão para deslogar
header('Location: login.html');  // Redireciona para a tela de login
exit;
?>
