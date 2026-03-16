import sqlite3

# conectar banco
conn = sqlite3.connect("estoque.db")
cursor = conn.cursor()
conn.row_factory = sqlite3.Row

# criar tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT,
quantidade INTEGER,
data_criacao TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS movimentacoes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
produto_id INTEGER,
usuario_id INTEGER,
tipo TEXT,
quantidade INTEGER,
data TEXT
)
""")

conn.commit()

# validacao da data

from datetime import datetime

def validar_data():

    while True:

        data_str = input("Data (YYYY-MM-DD): ")

        try:
            data = datetime.strptime(data_str, "%Y-%m-%d")

            hoje = datetime.today()

            if data > hoje:
                print("Erro: a data não pode ser futura.")
            else:
                return data_str

        except ValueError:
            print("Erro: data inválida. Use o formato YYYY-MM-DD.")


# cadastrar usuario
def cadastrar_usuario():
    nome = input("Nome do usuário: ")

    cursor.execute(
        "INSERT INTO usuarios(nome) VALUES(?)",
        (nome,)
    )

    conn.commit()
    print("Usuário cadastrado")


# lista dos usuários

def listar_usuarios():

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    if len(usuarios) == 0:
        return None

    print("\n--- USUÁRIOS CADASTRADOS ---\n")

    for u in usuarios:
        print(f"ID_Usuario = {u[0]} | Nome = {u[1]}")

    return usuarios    


# cadastrar produto

from datetime import date
def cadastrar_produto():

    usuarios = listar_usuarios()

    if usuarios is None:
        print("\nNão existem usuários cadastrados.")
        print("Cadastre um usuário antes de cadastrar um produto.\n")
        return

    # validar ID do usuário
    while True:
        usuario_id = int(input("\nID do usuário que está cadastrando: "))

        cursor.execute("SELECT * FROM usuarios WHERE id=?", (usuario_id,))
        usuario = cursor.fetchone()

        if usuario is None:
            print("\nErro: não há usuário vinculado a esse ID.")
            print("Utilize um dos IDs da lista mostrada acima.\n")
        else:
            break

    nome = input("Nome do produto: ")

    quantidade = int(input("Quantidade inicial: "))

    data = validar_data()

    cursor.execute(
        "INSERT INTO produtos (nome, quantidade, data_criacao) VALUES (?, ?, ?)",
        (nome, quantidade, data)
    )

    conn.commit()

    id_produto = cursor.lastrowid

    cursor.execute("""
        INSERT INTO movimentacoes (produto_id, usuario_id, tipo, quantidade, data)
        VALUES (?, ?, ?, ?, ?)
    """, (id_produto, usuario_id, "cadastro", quantidade, data))

    conn.commit()

    print("\nProduto cadastrado com sucesso!")

# listar produtos
def listar_produtos():

    cursor.execute("SELECT id, nome, quantidade FROM produtos")
    produtos = cursor.fetchall()

    if len(produtos) == 0:
        print("\nNenhum produto cadastrado.\n")
        return None

    print("\n--- PRODUTOS CADASTRADOS ---\n")

    for p in produtos:
        print(f"ID_Produtos = {p[0]} | Produto = {p[1]} | Quantidade = {p[2]}")

    return produtos


# entrada estoque
def entrada_estoque():

    produtos = listar_produtos()

    if produtos is None:
        return

    # escolher produto válido
    while True:
        produto = int(input("\nID do produto: "))

        cursor.execute("SELECT quantidade FROM produtos WHERE id=?", (produto,))
        estoque = cursor.fetchone()

        if estoque is None:
            print("Erro: ID de produto não cadastrado.")
            print("Escolha um ID da lista mostrada acima.")
        else:
            break

    usuarios = listar_usuarios()

    if usuarios is None:
        print("\nNenhum usuário cadastrado.")
        return

    # escolher usuário válido
    while True:
        usuario = int(input("\nID do usuário: "))

        cursor.execute("SELECT * FROM usuarios WHERE id=?", (usuario,))
        usuario_existe = cursor.fetchone()

        if usuario_existe is None:
            print("Erro: ID de usuário não cadastrado.")
            print("Escolha um ID da lista mostrada acima.")
        else:
            break

    quantidade = int(input("Quantidade recebida: "))

    data = validar_data()

    nova_qtd = estoque[0] + quantidade

    cursor.execute(
        "UPDATE produtos SET quantidade=? WHERE id=?",
        (nova_qtd, produto)
    )

    cursor.execute("""
    INSERT INTO movimentacoes(produto_id,usuario_id,tipo,quantidade,data)
    VALUES(?,?,?,?,?)
    """, (produto, usuario, "entrada", quantidade, data))

    conn.commit()

    print("\nEntrada registrada com sucesso!")


# saída estoque
def saida_estoque():

    produtos = listar_produtos()

    if produtos is None:
        return

    # escolher produto válido
    while True:
        produto = int(input("\nID do produto: "))

        cursor.execute("SELECT quantidade FROM produtos WHERE id=?", (produto,))
        estoque = cursor.fetchone()

        if estoque is None:
            print("Erro: ID de produto não cadastrado.")
            print("Escolha um ID da lista mostrada acima.")
        else:
            break

    usuarios = listar_usuarios()

    if usuarios is None:
        print("\nNenhum usuário cadastrado.")
        return

    # escolher usuário válido
    while True:
        usuario = int(input("\nID do usuário: "))

        cursor.execute("SELECT * FROM usuarios WHERE id=?", (usuario,))
        usuario_existe = cursor.fetchone()

        if usuario_existe is None:
            print("Erro: ID de usuário não cadastrado.")
            print("Escolha um ID da lista mostrada acima.")
        else:
            break

    # validar quantidade
    while True:
        quantidade = int(input("Quantidade retirada: "))

        if quantidade > estoque[0]:
            print("\nEstoque insuficiente.")
            print("Estoque atual:", estoque[0])
        else:
            break

    data = validar_data()

    nova_qtd = estoque[0] - quantidade

    cursor.execute(
        "UPDATE produtos SET quantidade=? WHERE id=?",
        (nova_qtd, produto)
    )

    cursor.execute("""
    INSERT INTO movimentacoes(produto_id,usuario_id,tipo,quantidade,data)
    VALUES(?,?,?,?,?)
    """, (produto, usuario, "saida", quantidade, data))

    conn.commit()

    print("\nSaída registrada com sucesso!")


# relatorio de movimentanção

def relatorio_movimentacoes():

    cursor.execute("""
    SELECT p.nome, u.nome, m.tipo, m.quantidade, m.data
    FROM movimentacoes m
    JOIN produtos p ON m.produto_id = p.id
    JOIN usuarios u ON m.usuario_id = u.id
    ORDER BY m.data
    """)

    registros = cursor.fetchall()

    print("\n--- RELATÓRIO DE MOVIMENTAÇÕES ---\n")

    for r in registros:
        produto, usuario, tipo, quantidade, data = r
        print(f"Produto: {produto}")
        print(f"Usuário: {usuario}")
        print(f"Tipo: {tipo}")
        print(f"Quantidade: {quantidade}")
        print(f"Data: {data}")
        print("-" * 30)


# menu
while True:

    print("\n--- SISTEMA ESTOQUE ---")
    print("1 Cadastrar usuário")
    print("2 Cadastrar produto")
    print("3 Listar produtos")
    print("4 Entrada estoque")
    print("5 Saída estoque")
    print("6 Relatório de movimentações")
    print("0 Sair")

    op = input("Escolha: ")

    if op == "1":
        cadastrar_usuario()

    elif op == "2":
        cadastrar_produto()

    elif op == "3":
        listar_produtos()

    elif op == "4":
        entrada_estoque()

    elif op == "5":
        saida_estoque()

    elif op == "6":
        relatorio_movimentacoes()

    elif op == "0":
        break

    else:
        print("Opção inválida")
