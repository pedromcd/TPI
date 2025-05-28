# FinanceControl

**FinanceControl** é um aplicativo desktop de controle financeiro pessoal, desenvolvido com o objetivo de oferecer uma solução simples e eficiente para o registro e acompanhamento de entradas e saídas financeiras. A aplicação foi construída utilizando Python com a biblioteca Tkinter para a interface gráfica e SQLite como banco de dados local, garantindo praticidade e desempenho.

## 📋 Índice

- [Visão Geral do Projeto](#visão-geral-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como Usar](#como-usar)
- [Créditos](#créditos)

## 📌 Visão Geral do Projeto

O **FinanceControl** surgiu da necessidade de organizar lançamentos financeiros de forma prática, permitindo que qualquer usuário possa visualizar e controlar seu saldo com facilidade. O sistema contempla uma tela de login, onde usuários podem se autenticar, e uma interface principal com recursos completos para o controle das finanças.

O foco é na usabilidade e clareza das informações financeiras, com um histórico detalhado, cálculo de saldo em tempo real e opções para edição e exclusão de lançamentos.

## ✅ Funcionalidades

- **Login de Usuário**: Tela de autenticação segura com senhas criptografadas.
- **Cadastro de Lançamentos**: Registro de entradas e saídas, com descrição, valor, data e tipo de movimentação.
- **Visualização de Histórico**: Exibição de todos os lançamentos anteriores com filtros por data e tipo.
- **Edição e Exclusão**: Lançamentos podem ser modificados ou removidos diretamente do histórico.
- **Cálculo de Saldo**: Atualização automática do saldo com base nos lançamentos.
- **Interface Responsiva**: Layout adaptado para resolução 1280x720 com imagem de fundo personalizada.

## 🛠 Tecnologias Utilizadas

- Python 3
- Tkinter (interface gráfica)
- Docker
- Git e Github
- SQLite (banco de dados local)
- `hashlib` (criptografia de senhas)
- `unittest` (testes automatizados)

## ▶️ Como Usar

### 1. Pré-requisitos

- [Python 3](https://www.python.org/downloads/)

### 2. Instalação

```bash
git clone https://github.com/seu-usuario/FinanceControl.git
cd FinanceControl
```

Crie e ative um ambiente virtual (opcional):

```bash
python -m venv venv
# Ativação:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 3. Executando a Aplicação

```bash
python app.py
```

### 4. Executando os Testes

```bash
python -m unittest test_app.py
```

## 👥 Créditos

- Guilherme Borges  
- Pedro Marques Correa Domingues  
- Kauê Alcântara  
- Lucas Borges  
- Vinicius Trabuco