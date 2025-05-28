import unittest
import sqlite3
import os
from datetime import datetime
from cadastro_clientes import validar_data, conectar_banco, inicializar_banco, hash_senha

DB_PATH = r"C:\Users\Guilherme\Desktop\AppCadastro\cadastro_clientes.db"

class TestControleFinanceiro(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Inicializa o banco de dados para testes
        inicializar_banco()

    def test_validar_data_valida(self):
        self.assertTrue(validar_data("25/12/2024"))

    def test_validar_data_invalida(self):
        self.assertFalse(validar_data("2024-12-25"))
        self.assertFalse(validar_data("31/02/2023"))
        self.assertFalse(validar_data("abc"))

    def test_tabelas_existem(self):
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        self.assertIsNotNone(cursor.fetchone())

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lancamentos'")
        self.assertIsNotNone(cursor.fetchone())

        conn.close()

    def test_registro_usuario(self):
        conn = conectar_banco()
        cursor = conn.cursor()

        nome = "Teste Usuário"
        email = "teste@example.com"
        senha = "senha123"
        senha_hash = hash_senha(senha)

        # Remove se já existir
        cursor.execute("DELETE FROM usuarios WHERE email = ?", (email,))

        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha_hash)
        )
        conn.commit()

        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado[1], nome)

    def test_inserir_lancamento(self):
        conn = conectar_banco()
        cursor = conn.cursor()

        # Buscar o ID do usuário de teste
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", ("teste@example.com",))
        usuario = cursor.fetchone()
        self.assertIsNotNone(usuario)
        usuario_id = usuario[0]

        cursor.execute('''
            INSERT INTO lancamentos (data, tipo, valor, descricao, usuario_id)
            VALUES (?, ?, ?, ?, ?)
        ''', ("01/01/2024", "entrada", 500.0, "Salário", usuario_id))
        conn.commit()

        cursor.execute("SELECT * FROM lancamentos WHERE usuario_id = ?", (usuario_id,))
        resultados = cursor.fetchall()
        conn.close()

        self.assertGreater(len(resultados), 0)

    def test_calculo_saldo(self):
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM usuarios WHERE email = ?", ("teste@example.com",))
        usuario_id = cursor.fetchone()[0]

        # Limpa lançamentos anteriores do usuário
        cursor.execute("DELETE FROM lancamentos WHERE usuario_id = ?", (usuario_id,))
        conn.commit()

        # Inserir entradas e saídas
        lancamentos = [
            ("01/01/2024", "entrada", 1000.0, "Salário"),
            ("05/01/2024", "saida", 200.0, "Mercado"),
            ("10/01/2024", "saida", 150.0, "Internet"),
        ]
        for data, tipo, valor, descricao in lancamentos:
            cursor.execute('''
                INSERT INTO lancamentos (data, tipo, valor, descricao, usuario_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (data, tipo, valor, descricao, usuario_id))
        conn.commit()

        cursor.execute("""
            SELECT tipo, SUM(valor) FROM lancamentos
            WHERE usuario_id = ?
            GROUP BY tipo
        """, (usuario_id,))
        totais = dict(cursor.fetchall())

        entrada = totais.get("entrada", 0)
        saida = totais.get("saida", 0)
        saldo = entrada - saida

        conn.close()
        self.assertEqual(saldo, 650.0)

if __name__ == '__main__':
    unittest.main()
