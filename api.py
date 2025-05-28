import os
from flask import Flask, request, jsonify
import sqlite3
import hashlib
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)

DB_PATH = r"C:\Users\Guilherme\Desktop\AppCadastro\cadastro_clientes.db"
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")

# Inicializa Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

def conectar():
    return sqlite3.connect(DB_PATH)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# ---------------------------------------
# REGISTRO DE USUÁRIO (local SQLite)
# ---------------------------------------
@app.route('/registro', methods=['POST'])
def registrar_usuario():
    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not (nome and email and senha):
        return jsonify({"erro": "Preencha todos os campos"}), 400

    senha_hash = hash_senha(senha)

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, senha_hash)
            )
            conn.commit()
        return jsonify({"mensagem": "Usuário registrado com sucesso"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"erro": "E-mail já cadastrado"}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ---------------------------------------
# LOGIN via token Firebase (token JWT enviado no header Authorization)
# ---------------------------------------
@app.route('/login', methods=['POST'])
def login():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"erro": "Token não fornecido"}), 401

    token = auth_header.replace("Bearer ", "")

    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']

        # Procura usuário local no SQLite pelo uid Firebase (campo firebase_uid)
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, email FROM usuarios WHERE firebase_uid = ?", (uid,))
            usuario = cursor.fetchone()
            if usuario:
                return jsonify({
                    "mensagem": "Login via Firebase OK",
                    "usuario_id": usuario[0],
                    "nome": usuario[1],
                    "email": usuario[2]
                }), 200
            else:
                return jsonify({"erro": "Usuário não cadastrado localmente"}), 401

    except Exception as e:
        return jsonify({"erro": "Token inválido ou expirado"}), 401

# ---------------------------------------
# CADASTRAR LANÇAMENTO
# ---------------------------------------
@app.route('/lancamentos', methods=['POST'])
def criar_lancamento():
    dados = request.get_json()
    campos = ["data", "tipo", "valor", "descricao", "usuario_id"]

    if not all(dados.get(c) for c in campos):
        return jsonify({"erro": "Preencha todos os campos"}), 400

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO lancamentos (data, tipo, valor, descricao, usuario_id)
                VALUES (?, ?, ?, ?, ?)
            """, [dados[c] for c in campos])
            conn.commit()
        return jsonify({"mensagem": "Lançamento adicionado com sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ---------------------------------------
# LISTAR LANÇAMENTOS POR USUÁRIO
# ---------------------------------------
@app.route('/lancamentos', methods=['GET'])
def listar_lancamentos():
    usuario_id = request.args.get("usuario_id")
    if not usuario_id:
        return jsonify({"erro": "ID do usuário é obrigatório"}), 400

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lancamentos WHERE usuario_id = ? ORDER BY data DESC", (usuario_id,))
            colunas = [desc[0] for desc in cursor.description]
            resultados = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ---------------------------------------
# ATUALIZAR LANÇAMENTO
# ---------------------------------------
@app.route('/lancamentos/<int:id>', methods=['PUT'])
def atualizar_lancamento(id):
    dados = request.get_json()
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE lancamentos
                SET data = ?, tipo = ?, valor = ?, descricao = ?
                WHERE id = ?
            """, (dados.get("data"), dados.get("tipo"), dados.get("valor"), dados.get("descricao"), id))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"erro": "Lançamento não encontrado"}), 404
        return jsonify({"mensagem": "Lançamento atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ---------------------------------------
# DELETAR LANÇAMENTO
# ---------------------------------------
@app.route('/lancamentos/<int:id>', methods=['DELETE'])
def deletar_lancamento(id):
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM lancamentos WHERE id = ?", (id,))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"erro": "Lançamento não encontrado"}), 404
        return jsonify({"mensagem": "Lançamento excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ---------------------------------------
# SALDO DO USUÁRIO
# ---------------------------------------
@app.route('/saldo', methods=['GET'])
def calcular_saldo():
    usuario_id = request.args.get("usuario_id")
    if not usuario_id:
        return jsonify({"erro": "ID do usuário é obrigatório"}), 400

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tipo, SUM(valor) FROM lancamentos
                WHERE usuario_id = ?
                GROUP BY tipo
            """, (usuario_id,))
            totais = dict(cursor.fetchall())
            saldo = totais.get("entrada", 0) - totais.get("saida", 0)
        return jsonify({"saldo": saldo}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
