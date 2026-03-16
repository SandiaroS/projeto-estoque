import tkinter as tk
import banco


def cadastrar_usuario():
    banco.cadastrar_usuario()


def cadastrar_produto():
    banco.cadastrar_produto()


janela = tk.Tk()
janela.title("Sistema de Estoque")
janela.geometry("400x300")

titulo = tk.Label(janela, text="Sistema de Estoque", font=("Arial", 14))
titulo.pack(pady=15)

btn_usuario = tk.Button(janela, text="Cadastrar Usuário", width=25, command=cadastrar_usuario)
btn_usuario.pack(pady=5)

btn_produto = tk.Button(janela, text="Cadastrar Produto", width=25, command=cadastrar_produto)
btn_produto.pack(pady=5)

btn_sair = tk.Button(janela, text="Sair", width=25, command=janela.quit)
btn_sair.pack(pady=15)

janela.mainloop()