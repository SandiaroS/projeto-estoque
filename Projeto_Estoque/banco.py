import sqlite3
from datetime import datetime

# conectar banco
conn = sqlite3.connect("estoque.db")
cursor = conn.cursor()

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


# validar data
def validar_data(data_str):

    try:
        data = datetime.strptime(data_str, "%Y-%m-%d")
        hoje = datetime.today()

        if data > hoje:
            return False

        return True

    except ValueError:
        return False


# cadastrar usuário
def cadastrar_usuario(nome):

    cursor.execute(
        "INSERT INTO usuarios(nome) VALUES(?)",
        (nome,)
    )

    conn.commit()


# listar usuários
def listar_usuarios():

    cursor.execute("SELECT id, nome FROM usuarios")

    return cursor.fetchall()


# cadastrar produto
def cadastrar_produto(nome, quantidade, data, usuario_id):

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


# listar produtos
def listar_produtos():

    cursor.execute("SELECT id, nome, quantidade FROM produtos")

    return cursor.fetchall()


# entrada estoque
def entrada_estoque(produto_id, usuario_id, quantidade, data):

    cursor.execute("SELECT quantidade FROM produtos WHERE id=?", (produto_id,))
    estoque = cursor.fetchone()

    if estoque is None:
        return "produto_nao_existe"

    nova_qtd = estoque[0] + quantidade

    cursor.execute(
        "UPDATE produtos SET quantidade=? WHERE id=?",
        (nova_qtd, produto_id)
    )

    cursor.execute("""
    INSERT INTO movimentacoes(produto_id,usuario_id,tipo,quantidade,data)
    VALUES(?,?,?,?,?)
    """, (produto_id, usuario_id, "entrada", quantidade, data))

    conn.commit()


# saída estoque
def saida_estoque(produto_id, usuario_id, quantidade, data):

    cursor.execute("SELECT quantidade FROM produtos WHERE id=?", (produto_id,))
    estoque = cursor.fetchone()

    if estoque is None:
        return "produto_nao_existe"

    if quantidade > estoque[0]:
        return "estoque_insuficiente"

    nova_qtd = estoque[0] - quantidade

    cursor.execute(
        "UPDATE produtos SET quantidade=? WHERE id=?",
        (nova_qtd, produto_id)
    )

    cursor.execute("""
    INSERT INTO movimentacoes(produto_id,usuario_id,tipo,quantidade,data)
    VALUES(?,?,?,?,?)
    """, (produto_id, usuario_id, "saida", quantidade, data))

    conn.commit()


# relatório
def relatorio_movimentacoes():

    cursor.execute("""
    SELECT p.nome, u.nome, m.tipo, m.quantidade, m.data
    FROM movimentacoes m
    JOIN produtos p ON m.produto_id = p.id
    JOIN usuarios u ON m.usuario_id = u.id
    ORDER BY m.data
    """)

    return cursor.fetchall()