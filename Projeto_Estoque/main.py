import tkinter as tk
from tkinter import messagebox
import banco

# cadastrar usuario
def tela_cadastrar_usuario():

    janela = tk.Toplevel()

    janela.title("Cadastrar Usuário")
    janela.geometry("300x200")

    tk.Label(janela, text="Nome do usuário").pack()

    nome = tk.Entry(janela)
    nome.pack()

    def salvar():

        banco.cadastrar_usuario(nome.get())

        messagebox.showinfo("Sucesso", "Usuário cadastrado")

        janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)


# listar produtos
def tela_listar_produtos():

    janela = tk.Toplevel()

    janela.title("Produtos")

    produtos = banco.listar_produtos()

    for p in produtos:

        texto = f"ID {p[0]} | {p[1]} | Qtd: {p[2]}"

        tk.Label(janela, text=texto).pack()


# tela principal
app = tk.Tk()

app.title("Sistema de Estoque")
app.geometry("400x350")

tk.Label(app, text="Sistema de Controle de Estoque", font=("Arial",14)).pack(pady=20)

tk.Button(app, text="Cadastrar Usuário", width=25, command=tela_cadastrar_usuario).pack(pady=5)

tk.Button(app, text="Listar Produtos", width=25, command=tela_listar_produtos).pack(pady=5)

tk.Button(app, text="Sair", width=25, command=app.quit).pack(pady=20)

app.mainloop()