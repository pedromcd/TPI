import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

DB_PATH = r"C:\Users\Guilherme\Desktop\AppCadastro\controle_financeiro.db"

CATEGORIAS = ["Entrada", "Saída"]

def validar_data(data: str) -> bool:
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def conectar_banco():
    return sqlite3.connect(DB_PATH)

def inicializar_banco():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lancamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        categoria TEXT NOT NULL,
        valor REAL NOT NULL,
        descricao TEXT,
        usuario_id INTEGER NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
''')
    
    conn.commit()
    conn.close()

def hash_senha(senha):
    import hashlib
    return hashlib.sha256(senha.encode()).hexdigest()

def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def abrir_tela_cadastro():
    cadastro_janela = tk.Toplevel()
    cadastro_janela.title("Cadastro de Usuário")
    centralizar_janela(cadastro_janela, 300, 200)

    tk.Label(cadastro_janela, text="Novo usuário:").pack(pady=(10, 0))
    entrada_novo_usuario = tk.Entry(cadastro_janela)
    entrada_novo_usuario.pack()

    tk.Label(cadastro_janela, text="Senha:").pack(pady=(10, 0))
    entrada_nova_senha = tk.Entry(cadastro_janela, show="*")
    entrada_nova_senha.pack()

    def cadastrar_usuario():
        usuario = entrada_novo_usuario.get().strip()
        senha = entrada_nova_senha.get().strip()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)", (usuario, senha))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            cadastro_janela.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Usuário já existe.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")

    tk.Button(cadastro_janela, text="Cadastrar", command=cadastrar_usuario, bg="#4CAF50", fg="white").pack(pady=20)

def fazer_login():
    usuario = entrada_usuario.get().strip()
    senha = entrada_senha.get().strip()

    if not usuario or not senha:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND senha=?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario}!")
        janela_login.destroy()
        abrir_app_principal()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

def validar_data(data_str):
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def salvar_lancamento():
    data = entrada_data.get().strip()
    categoria = categoria_var.get()
    descricao = entrada_descricao.get().strip()
    valor_str = entrada_valor.get().strip()

    if not data or not categoria or not descricao or not valor_str:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    if not validar_data(data):
        messagebox.showerror("Erro", "Data inválida. Use DD/MM/AAAA.")
        return

    try:
        valor = float(valor_str)
    except ValueError:
        messagebox.showerror("Erro", "Valor deve ser um número.")
        return

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO lancamentos (data, categoria, descricao, valor)
        VALUES (?, ?, ?, ?)
    ''', (data, categoria, descricao, valor))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Lançamento salvo com sucesso!")

    entrada_data.delete(0, tk.END)
    categoria_var.set(CATEGORIAS[0])
    entrada_descricao.delete(0, tk.END)
    entrada_valor.delete(0, tk.END)

def abrir_historico():
    historico_janela = tk.Toplevel()
    historico_janela.title("Histórico de Lançamentos")
    centralizar_janela(historico_janela, 900, 500)

    filtro_frame = tk.Frame(historico_janela)
    filtro_frame.pack(pady=10)

    tk.Label(filtro_frame, text="Data Inicial (DD/MM/AAAA):").grid(row=0, column=0, padx=5)
    entrada_data_inicial = tk.Entry(filtro_frame, width=12)
    entrada_data_inicial.grid(row=0, column=1, padx=5)

    tk.Label(filtro_frame, text="Data Final (DD/MM/AAAA):").grid(row=0, column=2, padx=5)
    entrada_data_final = tk.Entry(filtro_frame, width=12)
    entrada_data_final.grid(row=0, column=3, padx=5)

    tk.Label(filtro_frame, text="Categoria:").grid(row=0, column=4, padx=5)
    categoria_filtro_var = tk.StringVar()
    categoria_filtro_var.set("Todos")
    categoria_filtro_menu = ttk.Combobox(filtro_frame, textvariable=categoria_filtro_var, values=["Todos"] + CATEGORIAS, state="readonly", width=10)
    categoria_filtro_menu.grid(row=0, column=5, padx=5)

    tabela = ttk.Treeview(historico_janela, columns=("id", "Data", "Categoria", "Descrição", "Valor"), show="headings")
    tabela.pack(fill="both", expand=True)

    for col in ("id", "Data", "Categoria", "Descrição", "Valor"):
        tabela.heading(col, text=col)
        if col == "Descrição":
            tabela.column(col, width=300)
        else:
            tabela.column(col, width=100, anchor="center")

    def carregar_dados():
        for linha in tabela.get_children():
            tabela.delete(linha)

        data_inicio = entrada_data_inicial.get().strip()
        data_fim = entrada_data_final.get().strip()
        categoria_filtro = categoria_filtro_var.get()

        query = "SELECT id, data, categoria, descricao, valor FROM lancamentos WHERE 1=1"
        params = []

        # Filtrar por datas se preenchidas
        if data_inicio:
            if not validar_data(data_inicio):
                messagebox.showerror("Erro", "Data Inicial inválida.")
                return
            dt_inicio = datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
            query += " AND date(substr(data, 7, 4) || '-' || substr(data, 4, 2) || '-' || substr(data, 1, 2)) >= date(?)"
            params.append(dt_inicio)

        if data_fim:
            if not validar_data(data_fim):
                messagebox.showerror("Erro", "Data Final inválida.")
                return
            dt_fim = datetime.strptime(data_fim, "%d/%m/%Y").strftime("%Y-%m-%d")
            query += " AND date(substr(data, 7, 4) || '-' || substr(data, 4, 2) || '-' || substr(data, 1, 2)) <= date(?)"
            params.append(dt_fim)

        # Filtrar por categoria se não for 'Todos'
        if categoria_filtro != "Todos":
            query += " AND categoria = ?"
            params.append(categoria_filtro)

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute(query, params)
        linhas = cursor.fetchall()
        conn.close()

        for row in linhas:
            tabela.insert("", "end", values=row)

        atualizar_saldo(linhas)

    def excluir_selecionado():
        selecionado = tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um lançamento para excluir.")
            return
        item = tabela.item(selecionado)
        id_lanc = item["values"][0]
        confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este lançamento?")
        if confirmar:
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM lancamentos WHERE id=?", (id_lanc,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Lançamento excluído com sucesso.")
            carregar_dados()

    def editar_selecionado():
        selecionado = tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um lançamento para editar.")
            return
        item = tabela.item(selecionado)
        dados = item["values"]
        id_lanc = dados[0]

        editar_janela = tk.Toplevel(historico_janela)
        editar_janela.title("Editar Lançamento")
        centralizar_janela(editar_janela, 350, 350)

        tk.Label(editar_janela, text="Data (DD/MM/AAAA):").pack(pady=(10, 0))
        entrada_data_editar = tk.Entry(editar_janela, width=30)
        entrada_data_editar.insert(0, dados[1])
        entrada_data_editar.pack()

        tk.Label(editar_janela, text="Categoria:").pack(pady=(10, 0))
        categoria_editar_var = tk.StringVar()
        categoria_editar_var.set(dados[2])
        categoria_editar_menu = ttk.Combobox(editar_janela, textvariable=categoria_editar_var, values=CATEGORIAS, state="readonly", width=28)
        categoria_editar_menu.pack()

        tk.Label(editar_janela, text="Descrição:").pack(pady=(10, 0))
        entrada_descricao_editar = tk.Entry(editar_janela, width=30)
        entrada_descricao_editar.insert(0, dados[3])
        entrada_descricao_editar.pack()

        tk.Label(editar_janela, text="Valor:").pack(pady=(10, 0))
        entrada_valor_editar = tk.Entry(editar_janela, width=30)
        entrada_valor_editar.insert(0, dados[4])
        entrada_valor_editar.pack()

        def salvar_edicao():
            nova_data = entrada_data_editar.get().strip()
            nova_categoria = categoria_editar_var.get()
            nova_descricao = entrada_descricao_editar.get().strip()
            valor_str = entrada_valor_editar.get().strip()

            if not nova_data or not nova_categoria or not nova_descricao or not valor_str:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return
            if not validar_data(nova_data):
                messagebox.showerror("Erro", "Data inválida.")
                return
            try:
                novo_valor = float(valor_str)
            except ValueError:
                messagebox.showerror("Erro", "Valor deve ser um número.")
                return

            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE lancamentos SET data=?, categoria=?, descricao=?, valor=?
                WHERE id=?
            ''', (nova_data, nova_categoria, nova_descricao, novo_valor, id_lanc))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Lançamento atualizado com sucesso.")
            editar_janela.destroy()
            carregar_dados()

        tk.Button(editar_janela, text="Salvar", command=salvar_edicao, bg="#4CAF50", fg="white").pack(pady=20)

    def atualizar_saldo(linhas):
        saldo = 0.0
        for linha in linhas:
            valor = linha[4]
            if linha[2] == "Entrada":
                saldo += valor
            else:
                saldo -= valor
        saldo_label.config(text=f"Saldo Atual: R$ {saldo:.2f}")

    botoes_frame = tk.Frame(historico_janela)
    botoes_frame.pack(pady=5)

    tk.Button(botoes_frame, text="Editar Selecionado", command=editar_selecionado, bg="#FF9800", fg="white", width=20).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Excluir Selecionado", command=excluir_selecionado, bg="#F44336", fg="white", width=20).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Aplicar Filtros", command=carregar_dados, bg="#2196F3", fg="white", width=20).pack(side="left", padx=5)

    saldo_label = tk.Label(historico_janela, text="Saldo Atual: R$ 0.00", font=("Segoe UI", 12, "bold"))
    saldo_label.pack(pady=10)

    carregar_dados()

def abrir_app_principal():
    global janela_app
    global entrada_data, categoria_var, entrada_descricao, entrada_valor

    janela_app = tk.Tk()
    janela_app.title("Controle Financeiro")
    centralizar_janela(janela_app, 600, 450)

    frame = tk.Frame(janela_app, padx=30, pady=20)
    frame.pack(expand=True)

    fonte = ("Segoe UI", 12)

    tk.Label(frame, text="Data (DD/MM/AAAA):", font=fonte).pack(pady=(10, 0))
    entrada_data = tk.Entry(frame, font=fonte, width=30)
    entrada_data.pack()

    tk.Label(frame, text="Categoria:", font=fonte).pack(pady=(10, 0))
    categoria_var = tk.StringVar()
    categoria_var.set(CATEGORIAS[0])
    categoria_menu = ttk.Combobox(frame, textvariable=categoria_var, values=CATEGORIAS, state="readonly", font=fonte, width=28)
    categoria_menu.pack()

    tk.Label(frame, text="Descrição:", font=fonte).pack(pady=(10, 0))
    entrada_descricao = tk.Entry(frame, font=fonte, width=30)
    entrada_descricao.pack()

    tk.Label(frame, text="Valor (use número positivo):", font=fonte).pack(pady=(10, 0))
    entrada_valor = tk.Entry(frame, font=fonte, width=30)
    entrada_valor.pack()

    tk.Button(frame, text="Salvar Lançamento", command=salvar_lancamento, bg="#4CAF50", fg="white", font=fonte, width=20).pack(pady=20)
    tk.Button(frame, text="Ver Histórico", command=abrir_historico, bg="#2196F3", fg="white", font=fonte, width=20).pack()

    janela_app.mainloop()

# --- Tela de login ---
janela_login = tk.Tk()
janela_login.title("Login")
centralizar_janela(janela_login, 350, 220)

tk.Label(janela_login, text="Usuário:").pack(pady=(20, 0))
entrada_usuario = tk.Entry(janela_login, width=30)
entrada_usuario.pack()

tk.Label(janela_login, text="Senha:").pack(pady=(10, 0))
entrada_senha = tk.Entry(janela_login, show="*", width=30)
entrada_senha.pack()

btn_frame = tk.Frame(janela_login)
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Entrar", command=fazer_login, bg="#4CAF50", fg="white", width=12).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Cadastrar Usuário", command=abrir_tela_cadastro, bg="#2196F3", fg="white", width=15).grid(row=0, column=1, padx=5)

inicializar_banco()
janela_login.mainloop()
