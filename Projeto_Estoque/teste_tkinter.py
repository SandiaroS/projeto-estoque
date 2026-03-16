import tkinter as tk

janela = tk.Tk()
janela.title("Teste Tkinter")
janela.geometry("300x200")

texto = tk.Label(janela, text="Tkinter funcionando!")
texto.pack(pady=50)

janela.mainloop()