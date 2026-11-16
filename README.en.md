**English** | [Português](README.md)

# 💰 FinanceControl

**A personal finance tracker with a Python/Tkinter desktop interface, a SQLite database, and a Flask REST API for the same operations.**

A team project for the **Integrated Technologies and Programming (TPI)** course in the Computer Science program at UNISAGRADO.

---

## 🎯 Goal

Build a simple tool to record income and expenses and track the balance, while practicing:

- **desktop GUI** development with Tkinter;
- **local persistence** with SQLite and parameterized SQL;
- **input validation** (dates, amounts, required fields);
- exposing the same rules as a **REST API** with Flask;
- **automated tests** with `unittest`;
- packaging with **Docker**.

---

## ✨ Features

### Desktop app (`cadastro_clientes.py`)

- **Login and user registration** in dedicated windows.
- **Entry registration** with a date (DD/MM/YYYY), category (Entrada = income or Saída = expense), description, and amount.
- **Validation** of required fields, date format and existence (for example, `31/02` is rejected), and numeric amounts.
- **History** table with **date-range filters** (start and end date) and a **category filter**.
- **Edit and delete** the selected entry.
- **Balance** recalculated according to the applied filters.

The interface text is in Portuguese.

### REST API (`api.py`)

| Method | Route | Description |
|---|---|---|
| `POST` | `/registro` | Registers a user (name, email, SHA-256-hashed password) |
| `POST` | `/login` | Authenticates by email and password |
| `POST` | `/lancamentos` | Creates an entry linked to a user |
| `GET` | `/lancamentos?usuario_id=` | Lists the user's entries, newest first |
| `PUT` | `/lancamentos/<id>` | Updates an entry |
| `DELETE` | `/lancamentos/<id>` | Deletes an entry |
| `GET` | `/saldo?usuario_id=` | Calculates the balance (income − expenses) |

Example:

```bash
curl -X POST http://127.0.0.1:5000/lancamentos \
  -H "Content-Type: application/json" \
  -d '{"data":"01/01/2024","tipo":"entrada","valor":1000,"descricao":"Salário","usuario_id":1}'
```

---

## 🗄️ Data model

The project evolved in two stages and currently has **two schemas**:

| | Desktop app | API and tests |
|---|---|---|
| Users | `usuarios(id, username, senha)` | `usuarios(id, nome, email, senha)` |
| Entries | `lancamentos(id, data, categoria, descricao, valor)` | `lancamentos(id, data, tipo, valor, descricao, usuario_id)` |
| Password | plain text | SHA-256 hash |
| Entries per user | no | yes (`usuario_id`) |

The versioned database (`controle_financeiro.db`) follows the desktop schema and contains only test data. The API schema is the more complete version: it links every entry to a user and restricts `tipo` to `entrada` (income) or `saida` (expense).

---

## 🛠️ Tech stack

- **Python 3**
- **Tkinter / ttk**: desktop interface
- **SQLite** (`sqlite3`): local database
- **Flask**: REST API
- **hashlib**: password hashing in the API
- **unittest**: automated tests
- **Docker**: API image

---

## ▶️ Running it

### 1. Clone and install

```bash
git clone https://github.com/pedromcd/TPI.git
cd TPI
pip install flask requests pillow
```

> `requirements.txt` also lists `tk` and `sqlite3`, which are already part of the standard Python installation, so installing the dependencies manually, as above, is the safest route.

### 2. Configure the database path

The files use an absolute Windows path in the `DB_PATH` constant. Before running, change `DB_PATH` in both `cadastro_clientes.py` and `api.py` to a path on your machine, for example:

```python
DB_PATH = "controle_financeiro.db"
```

### 3. Run

```bash
python cadastro_clientes.py   # desktop app
python api.py                 # API at http://127.0.0.1:5000
```

### 4. Tests

```bash
python -m unittest test_app.py
```

The tests cover date validation, table creation, user registration, entry insertion, and balance calculation on the API schema.

### Docker (API)

```bash
docker build -t financecontrol .
docker run -p 5000:5000 financecontrol
```

---

## 🧩 Structure

```text
TPI/
├── cadastro_clientes.py     # Desktop app (Tkinter): login, entries, history, filters, and balance
├── api.py                   # REST API (Flask) with the per-user schema
├── test_app.py              # unittest tests
├── controle_financeiro.db   # Sample SQLite database (test data)
├── requirements.txt
└── Dockerfile               # API image
```

---

## ⚠️ Known limitations

This is an academic project, and these are the points I would fix in a next version:

- **Two database schemas:** the desktop app and the API do not share the same data model yet.
- **Plain-text password on desktop:** only the API hashes passwords, and with plain SHA-256. bcrypt or Argon2 in both would be the right choice.
- **Hard-coded database path** instead of an environment variable.
- **Tests coupled to the GUI:** `test_app.py` imports `cadastro_clientes.py`, which opens the login window on import.
- **Docker:** the API calls `app.run()` without `host="0.0.0.0"`, so it needs that change to be reachable from outside the container.

## 🚧 Next steps

- Unify the schema and make the desktop app consume the API.
- Separate business logic from the interface so it can be tested in isolation.
- Configure the database through an environment variable.
- Use bcrypt for passwords and add token authentication to the API.

---

## 👥 Authors

Team project:

- Guilherme Borges
- Pedro Marques Correa Domingues
- Kauê Alcântara
- Lucas Borges
- Vinicius Trabuco
