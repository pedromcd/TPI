from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)
DB_PATH = r"C:\Users\Guilherme\Desktop\AppCadastro\cadastro_clientes.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# ----------------------------
# CADASTRO DE USUÁRIO
# ----------------------------
@app.route('/registro', methods=['POST'])
def registrar_usuario():
    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not (nome and email and senha):
        return jsonify({"erro": "Preencha todos os campos"}), 400

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                           (nome, email, hash_senha(senha)))
            conn.commit()
        return jsonify({"mensagem": "Usuário registrado com sucesso"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"erro": "E-mail já cadastrado"}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ----------------------------
# LOGIN
# ----------------------------
@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get("email")
    senha = hash_senha(dados.get("senha"))

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
            usuario = cursor.fetchone()
            if usuario:
                return jsonify({"mensagem": "Login bem-sucedido", "usuario_id": usuario[0], "nome": usuario[1]}), 200
            return jsonify({"erro": "Credenciais inválidas"}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ----------------------------
# CADASTRAR LANÇAMENTO
# ----------------------------
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

# ----------------------------
# HISTÓRICO DE LANÇAMENTOS POR USUÁRIO
# ----------------------------
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

# ----------------------------
# ATUALIZAR LANÇAMENTO
# ----------------------------
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

# ----------------------------
# DELETAR LANÇAMENTO
# ----------------------------
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

# ----------------------------
# SALDO DO USUÁRIO
# ----------------------------
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

# ----------------------------
# INICIAR SERVIDOR
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
