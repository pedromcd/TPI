<script>
    function cadastrarUsuario(event) {
        event.preventDefault(); // Impede o envio padrão do formulário

        const nome = document.getElementById('nome').value;
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;

        // Fazendo a requisição para o PHP que irá inserir no banco
        fetch('cadastrar.php', {
            method: 'POST',
            body: JSON.stringify({ nome, email, senha }), // Envia os dados para o PHP
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);  // Mensagem de sucesso
                window.location.href = 'TelaLogin.html'; // Redireciona para a tela de login
            } else {
                alert('Erro: ' + data.message);  // Mensagem de erro
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao cadastrar usuário!');
        });
    }
</script>
