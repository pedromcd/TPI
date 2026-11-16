[English](README.en.md) | **Português**

# 💰 FinanceControl

**Aplicativo de controle financeiro pessoal com interface desktop em Python/Tkinter, banco SQLite e uma API REST em Flask para as mesmas operações.**

Trabalho em equipe da disciplina de **Tecnologias e Programação Integrada (TPI)**, do curso de Ciência da Computação da UNISAGRADO.

---

## 🎯 Objetivo

Criar uma ferramenta simples para registrar entradas e saídas de dinheiro e acompanhar o saldo, praticando ao longo do caminho:

- desenvolvimento de **interface gráfica desktop** com Tkinter;
- **persistência local** com SQLite e SQL parametrizado;
- **validação de dados** de entrada (datas, valores, campos obrigatórios);
- exposição das mesmas regras como **API REST** com Flask;
- **testes automatizados** com `unittest`;
- empacotamento com **Docker**.

---

## ✨ Funcionalidades

### Aplicativo desktop (`cadastro_clientes.py`)

- **Login e cadastro de usuário** em janelas próprias.
- **Registro de lançamentos** com data (DD/MM/AAAA), categoria (Entrada ou Saída), descrição e valor.
- **Validação** de campos obrigatórios, formato e existência da data (por exemplo, `31/02` é rejeitado) e valor numérico.
- **Histórico** em tabela, com **filtros por período** (data inicial e final) e **por categoria**.
- **Edição e exclusão** do lançamento selecionado.
- **Saldo** recalculado de acordo com os filtros aplicados.

### API REST (`api.py`)

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/registro` | Cadastra usuário (nome, e-mail, senha com hash SHA-256) |
| `POST` | `/login` | Autentica por e-mail e senha |
| `POST` | `/lancamentos` | Cria lançamento vinculado a um usuário |
| `GET` | `/lancamentos?usuario_id=` | Lista os lançamentos do usuário, do mais recente ao mais antigo |
| `PUT` | `/lancamentos/<id>` | Atualiza um lançamento |
| `DELETE` | `/lancamentos/<id>` | Exclui um lançamento |
| `GET` | `/saldo?usuario_id=` | Calcula o saldo (entradas − saídas) |

Exemplo:

```bash
curl -X POST http://127.0.0.1:5000/lancamentos \
  -H "Content-Type: application/json" \
  -d '{"data":"01/01/2024","tipo":"entrada","valor":1000,"descricao":"Salário","usuario_id":1}'
```

---

## 🗄️ Modelo de dados

O projeto evoluiu em duas etapas e hoje tem **dois esquemas**:

| | Aplicativo desktop | API e testes |
|---|---|---|
| Usuários | `usuarios(id, username, senha)` | `usuarios(id, nome, email, senha)` |
| Lançamentos | `lancamentos(id, data, categoria, descricao, valor)` | `lancamentos(id, data, tipo, valor, descricao, usuario_id)` |
| Senha | texto puro | hash SHA-256 |
| Lançamentos por usuário | não | sim (`usuario_id`) |

O banco versionado (`controle_financeiro.db`) segue o esquema do aplicativo desktop e contém apenas dados de teste. O esquema da API é a versão mais completa: vincula cada lançamento a um usuário e restringe `tipo` a `entrada` ou `saida`.

---

## 🛠️ Tecnologias

- **Python 3**
- **Tkinter / ttk**: interface desktop
- **SQLite** (`sqlite3`): banco de dados local
- **Flask**: API REST
- **hashlib**: hash de senhas na API
- **unittest**: testes automatizados
- **Docker**: imagem da API

---

## ▶️ Como executar

### 1. Clonar e instalar

```bash
git clone https://github.com/pedromcd/TPI.git
cd TPI
pip install flask requests pillow
```

> O `requirements.txt` também lista `tk` e `sqlite3`, que já fazem parte da instalação padrão do Python. Por isso, instalar as dependências manualmente, como acima, é o caminho mais seguro.

### 2. Configurar o caminho do banco

Os arquivos usam um caminho absoluto de Windows na constante `DB_PATH`. Antes de executar, altere `DB_PATH` em `cadastro_clientes.py` e em `api.py` para um caminho da sua máquina, por exemplo:

```python
DB_PATH = "controle_financeiro.db"
```

### 3. Executar

```bash
python cadastro_clientes.py   # aplicativo desktop
python api.py                 # API em http://127.0.0.1:5000
```

### 4. Testes

```bash
python -m unittest test_app.py
```

Os testes cobrem validação de datas, criação das tabelas, cadastro de usuário, inserção de lançamento e cálculo de saldo no esquema da API.

### Docker (API)

```bash
docker build -t financecontrol .
docker run -p 5000:5000 financecontrol
```

---

## 🧩 Estrutura

```text
TPI/
├── cadastro_clientes.py     # Aplicativo desktop (Tkinter): login, lançamentos, histórico, filtros e saldo
├── api.py                   # API REST (Flask) com o esquema por usuário
├── test_app.py              # Testes com unittest
├── controle_financeiro.db   # Banco SQLite de exemplo (dados de teste)
├── requirements.txt
└── Dockerfile               # Imagem da API
```

---

## ⚠️ Limitações conhecidas

Este é um projeto acadêmico e tem pontos que eu corrigiria em uma próxima versão:

- **Dois esquemas de banco:** o aplicativo desktop e a API ainda não compartilham o mesmo modelo de dados.
- **Senha em texto puro no desktop:** apenas a API aplica hash, e com SHA-256 simples. O ideal seria bcrypt ou Argon2 em ambos.
- **Caminho do banco fixo** no código, em vez de configurável por variável de ambiente.
- **Testes acoplados à interface:** `test_app.py` importa `cadastro_clientes.py`, que abre a janela de login ao ser importado.
- **Docker:** a API usa `app.run()` sem `host="0.0.0.0"`, então precisa desse ajuste para ser acessível fora do container.

## 🚧 Próximos passos

- Unificar o esquema e fazer o aplicativo desktop consumir a API.
- Separar a lógica de negócio da interface para permitir testes isolados.
- Configurar o banco por variável de ambiente.
- Usar bcrypt para senhas e adicionar autenticação por token na API.

---

## 👥 Autores

Projeto em equipe:

- Guilherme Borges
- Pedro Marques Correa Domingues
- Kauê Alcântara
- Lucas Borges
- Vinicius Trabuco
