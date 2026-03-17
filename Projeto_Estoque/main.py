import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import banco

# ------------------------
# VALIDA CAMPOS NUMERICOS
# ------------------------

def validar_inteiro(valor):
    if valor == "":
        return True
    return valor.isdigit()


def validar_data_input(valor):
    permitido = "0123456789-"
    return all(c in permitido for c in valor)


# ------------------------
# CADASTRAR USUÁRIO
# ------------------------

def tela_cadastrar_usuario():

    janela = tk.Toplevel()
    janela.title("Cadastrar Usuário")
    janela.geometry("300x200")

    tk.Label(janela, text="Nome do usuário").pack()

    nome = tk.Entry(janela)
    nome.pack()

    def salvar():

        if nome.get() == "":
            messagebox.showerror("Erro", "Informe um nome")
            return

        banco.cadastrar_usuario(nome.get())

        messagebox.showinfo("Sucesso", "Usuário cadastrado")

        janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)


# ------------------------
# CADASTRAR PRODUTO
# ------------------------

def tela_cadastrar_produto():

    usuarios = banco.listar_usuarios()

    if len(usuarios) == 0:
        messagebox.showerror("Erro","Cadastre um usuário primeiro")
        return

    janela = tk.Toplevel()
    janela.title("Cadastrar Produto")
    janela.geometry("350x300")

    tk.Label(janela, text="Nome do produto").pack()
    nome = tk.Entry(janela)
    nome.pack()

    tk.Label(janela, text="Quantidade inicial").pack()
    quantidade = tk.Entry(
        janela,
        validate="key",
        validatecommand=vcmd_int
    )
    quantidade.pack()

    tk.Label(janela, text="Data (YYYY-MM-DD)").pack()
    data = tk.Entry(
        janela,
        validate="key",
        validatecommand=vcmd_data
    )
    data.pack()

    tk.Label(janela, text="Usuário").pack()

    usuario_var = tk.StringVar()
    usuario_menu = tk.OptionMenu(
        janela,
        usuario_var,
        *[f"{u[0]} - {u[1]}" for u in usuarios]
    )
    usuario_menu.pack()

    def salvar():

        if not banco.validar_data(data.get()):
            messagebox.showerror("Erro","Data inválida")
            return

        usuario_id = int(usuario_var.get().split(" - ")[0])

        banco.cadastrar_produto(
            nome.get(),
            int(quantidade.get()),
            data.get(),
            usuario_id
        )

        messagebox.showinfo("Sucesso","Produto cadastrado")

        janela.destroy()

    tk.Button(janela,text="Salvar",command=salvar).pack(pady=10)


# ------------------------
# LISTAR PRODUTOS
# ------------------------

def tela_listar_produtos():

    janela = tk.Toplevel()
    janela.title("Produtos")

    produtos = banco.listar_produtos()

    for p in produtos:

        texto = f"ID_Produto {p[0]} | Produto: {p[1]} | Quantidade: {p[2]}"

        tk.Label(janela,text=texto).pack()


# ------------------------
# ENTRADA ESTOQUE
# ------------------------

def tela_entrada():

    produtos = banco.listar_produtos()
    usuarios = banco.listar_usuarios()

    if len(produtos) == 0:
        messagebox.showerror("Erro","Nenhum produto cadastrado")
        return

    janela = tk.Toplevel()
    janela.title("Entrada de Estoque")
    janela.geometry("350x300")

    tk.Label(janela,text="Produto").pack()

    produto_var = tk.StringVar()
    tk.OptionMenu(
        janela,
        produto_var,
        *[f"{p[0]} - {p[1]} (Estoque: {p[2]})" for p in produtos]
    ).pack()

    tk.Label(janela,text="Usuário").pack()

    usuario_var = tk.StringVar()
    tk.OptionMenu(
        janela,
        usuario_var,
        *[f"{u[0]} - {u[1]}" for u in usuarios]
    ).pack()

    tk.Label(janela,text="Quantidade").pack()
    quantidade = tk.Entry(
        janela,
        validate="key",
        validatecommand=vcmd_int
    )
    quantidade.pack()

    tk.Label(janela,text="Data (YYYY-MM-DD)").pack()
    data = tk.Entry(
        janela,
        validate="key",
        validatecommand=vcmd_data
    )
    data.pack()

    def registrar():

        if not banco.validar_data(data.get()):
            messagebox.showerror("Erro","Data inválida")
            return

        produto_id = int(produto_var.get().split(" - ")[0])
        usuario_id = int(usuario_var.get().split(" - ")[0])

        banco.entrada_estoque(
            produto_id,
            usuario_id,
            int(quantidade.get()),
            data.get()
        )

        messagebox.showinfo("Sucesso","Entrada registrada")

        janela.destroy()

    tk.Button(janela,text="Registrar",command=registrar).pack(pady=10)


# ------------------------
# SAÍDA ESTOQUE
# ------------------------

def tela_saida():

    produtos = banco.listar_produtos()
    usuarios = banco.listar_usuarios()

    if len(produtos) == 0:
        messagebox.showerror("Erro","Nenhum produto cadastrado")
        return

    janela = tk.Toplevel()
    janela.title("Saída de Estoque")
    janela.geometry("350x300")

    tk.Label(janela,text="Produto").pack()

    produto_var = tk.StringVar()
    tk.OptionMenu(
        janela,
        produto_var,
        *[f"{p[0]} - {p[1]} (Estoque: {p[2]})" for p in produtos]
    ).pack()

    tk.Label(janela,text="Usuário").pack()

    usuario_var = tk.StringVar()
    tk.OptionMenu(
        janela,
        usuario_var,
        *[f"{u[0]} - {u[1]}" for u in usuarios]
    ).pack()

    tk.Label(janela,text="Quantidade").pack()
    quantidade = tk.Entry(
        janela,
        validate="key",
        validatecommand=vcmd_int
    )
    quantidade.pack()

    tk.Label(janela,text="Data (YYYY-MM-DD)").pack()
    data = tk.Entry(
        janela,
        validate="key",
        validatecommand=vcmd_data
    )
    data.pack()

    def registrar():

        if not banco.validar_data(data.get()):
            messagebox.showerror("Erro","Data inválida")
            return

        produto_id = int(produto_var.get().split(" - ")[0])
        usuario_id = int(usuario_var.get().split(" - ")[0])

        retorno = banco.saida_estoque(
            produto_id,
            usuario_id,
            int(quantidade.get()),
            data.get()
        )

        if retorno == "estoque_insuficiente":

            produtos = banco.listar_produtos()

            for p in produtos:
                if p[0] == produto_id:
                    estoque_atual = p[2]
                    break

            messagebox.showerror(
                "Erro",
                f"Estoque insuficiente.\n\nEstoque atual do produto: {estoque_atual}"
            )

            return

        messagebox.showinfo("Sucesso","Saída registrada")

        janela.destroy()

    tk.Button(janela,text="Registrar",command=registrar).pack(pady=10)

# ------------------------
# RELATORIO DO ESTOQUE
# ------------------------

def tela_relatorio():

    janela = tk.Toplevel()
    janela.title("Relatório de Movimentações")
    janela.geometry("700x400")

    # tabela
    tabela = ttk.Treeview(janela)

    tabela["columns"] = ("produto","usuario","tipo","quantidade","data")

    tabela.column("#0", width=0, stretch=tk.NO)

    tabela.column("produto", anchor="w", width=150)
    tabela.column("usuario", anchor="w", width=120)
    tabela.column("tipo", anchor="center", width=100)
    tabela.column("quantidade", anchor="center", width=100)
    tabela.column("data", anchor="center", width=120)

    tabela.heading("produto", text="Produto")
    tabela.heading("usuario", text="Usuário")
    tabela.heading("tipo", text="Tipo")
    tabela.heading("quantidade", text="Quantidade")
    tabela.heading("data", text="Data")

    tabela.pack(fill="both", expand=True)

    # buscar dados
    registros = banco.relatorio_movimentacoes()

    for i, r in enumerate(registros):
        tabela.insert(
            "",
            "end",
            values=(r[0], r[1], r[2], r[3], r[4])
        )
# ------------------------
# TELA PRINCIPAL
# ------------------------

app = tk.Tk()

vcmd_int = (app.register(validar_inteiro), "%P")
vcmd_data = (app.register(validar_data_input), "%P")

app.title("Sistema de Estoque")
app.geometry("400x420")

tk.Label(app,text="Sistema de Controle de Estoque",font=("Arial",14)).pack(pady=20)

tk.Button(app,text="Cadastrar Usuário",width=30,command=tela_cadastrar_usuario).pack(pady=5)

tk.Button(app,text="Cadastrar Produto",width=30,command=tela_cadastrar_produto).pack(pady=5)

tk.Button(app,text="Listar Produtos",width=30,command=tela_listar_produtos).pack(pady=5)

tk.Button(app,text="Entrada de Estoque",width=30,command=tela_entrada).pack(pady=5)

tk.Button(app,text="Saída de Estoque",width=30,command=tela_saida).pack(pady=5)

tk.Button(app,text="Relatório de Movimentações",width=30,command=tela_relatorio).pack(pady=5)

tk.Button(app,text="Sair",width=30,command=app.quit).pack(pady=20)

app.mainloop()