import sqlite3
from datetime import datetime

# CONEXAO COM O BANCO
conn = sqlite3.connect("estoque.db")
cursor = conn.cursor()

# CRIAR TABELAS
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


# VALIDACAO DO FORMATO DE PREENCHIMENTO DA DATA
def validar_data(data_str):

    try:
        data = datetime.strptime(data_str, "%Y-%m-%d")
        hoje = datetime.today()

        if data > hoje:
            return False

        return True

    except ValueError:
        return False


# CADASTRAR USUARIO
def cadastrar_usuario(nome):

    cursor.execute(
        "INSERT INTO usuarios(nome) VALUES(?)",
        (nome,)
    )

    conn.commit()


# LISTA DE USUARIOS CADASTRADOS 
def listar_usuarios():

    cursor.execute("SELECT id, nome FROM usuarios")

    return cursor.fetchall()


# CADASTRO DE PRODUTOS NOVOS
def cadastrar_produto(nome, quantidade, data, usuario_id):

    cursor.execute(
        "INSERT INTO produtos (nome, quantidade, data_criacao) VALUES (?, ?, ?)",
        (nome, quantidade, data)
    )

    conn.commit()

    id_produto = cursor.lastrowid

    #REGISTRA MOVIMENTACAO DATA E RESPONSAVEL
    cursor.execute("""
        INSERT INTO movimentacoes (produto_id, usuario_id, tipo, quantidade, data)
        VALUES (?, ?, ?, ?, ?)
    """, (id_produto, usuario_id, "cadastro", quantidade, data))

    conn.commit()


# LISTAGEM DE PRODUTOS JA CADASTRADOS E SUAS QUANTIDADES
def listar_produtos():

    cursor.execute("SELECT id, nome, quantidade FROM produtos")

    return cursor.fetchall()


# ENTRADA DE PRODUTOS NO ESTOQUE
def entrada_estoque(produto_id, usuario_id, quantidade, data):

    cursor.execute("SELECT quantidade FROM produtos WHERE id=?", (produto_id,))
    estoque = cursor.fetchone()

    if estoque is None:
        return "produto_nao_existe"

    nova_qtd = estoque[0] + quantidade #ATUALIZA ESTOQUE AUTOMATICO

    cursor.execute(
        "UPDATE produtos SET quantidade=? WHERE id=?",
        (nova_qtd, produto_id)
    )

    #REGISTRA MOVIMENTACAO DATA E RESPONSAVEL
    cursor.execute("""
    INSERT INTO movimentacoes(produto_id,usuario_id,tipo,quantidade,data)
    VALUES(?,?,?,?,?)
    """, (produto_id, usuario_id, "entrada", quantidade, data))

    conn.commit()


# SAIDA DOS PRODUTOS DO ESTOQUE
def saida_estoque(produto_id, usuario_id, quantidade, data):

    cursor.execute("SELECT quantidade FROM produtos WHERE id=?", (produto_id,))
    estoque = cursor.fetchone()

    if estoque is None:
        return "produto_nao_existe"

    if quantidade > estoque[0]: #VALIDA ESTOQUE ANTES DA SAIDA
        return "estoque_insuficiente"

    nova_qtd = estoque[0] - quantidade #ATUALIZA ESTOQUE AUTOMATICO

    cursor.execute(
        "UPDATE produtos SET quantidade=? WHERE id=?",
        (nova_qtd, produto_id)
    )

    #REGISTRA MOVIMENTACAO DATA E RESPONSAVEL
    cursor.execute("""
    INSERT INTO movimentacoes(produto_id,usuario_id,tipo,quantidade,data)
    VALUES(?,?,?,?,?) 
    """, (produto_id, usuario_id, "saida", quantidade, data))

    conn.commit()


# RELATORIO DE MOVIMENTACAO DO ESTOQUE
def relatorio_movimentacoes():

    cursor.execute("""
    SELECT p.nome, u.nome, m.tipo, m.quantidade, m.data
    FROM movimentacoes m
    JOIN produtos p ON m.produto_id = p.id
    JOIN usuarios u ON m.usuario_id = u.id
    ORDER BY m.data
    """)

    return cursor.fetchall()