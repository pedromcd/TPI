**English** | [Português](README.md)

# FinanceControl

**FinanceControl** is a desktop personal finance app, built to offer a simple and efficient way to record and track income and expenses. The application was built with Python, using the Tkinter library for the graphical interface and SQLite as the local database, for practicality and performance.

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [How to Use](#️-how-to-use)
- [Credits](#-credits)

## 📌 Project Overview

**FinanceControl** was created to organize financial entries in a practical way, allowing any user to view and manage their balance easily. The system includes a login screen where users authenticate and a main interface with complete features for managing their finances.

The focus is on usability and clear financial information, with a detailed history, real-time balance calculation, and options to edit and delete entries.

## ✅ Features

- **User Login**: Secure authentication screen with hashed passwords.
- **Entry Registration**: Record income and expenses with a description, amount, date, and transaction type.
- **History View**: Display all previous entries with filters by date and type.
- **Edit and Delete**: Entries can be modified or removed directly from the history.
- **Balance Calculation**: Automatic balance updates based on the entries.
- **Responsive Interface**: Layout adapted to a 1280x720 resolution with a custom background image.

## 🛠 Technologies Used

- Python 3
- Tkinter (graphical interface)
- Docker
- Git and GitHub
- SQLite (local database)
- `hashlib` (password hashing)
- `unittest` (automated tests)

## ▶️ How to Use

### 1. Prerequisites

- [Python 3](https://www.python.org/downloads/)

### 2. Installation

```bash
git clone https://github.com/pedromcd/TPI.git
cd TPI
```

Create and activate a virtual environment (optional):

```bash
python -m venv venv
# Activation:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Running the Application

```bash
python app.py
```

### 4. Running the Tests

```bash
python -m unittest test_app.py
```

## 👥 Credits

- Guilherme Borges  
- Pedro Marques Correa Domingues  
- Kauê Alcântara  
- Lucas Borges  
- Vinicius Trabuco
