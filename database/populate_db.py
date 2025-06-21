from faker import Faker
import sqlite3
import random
import os
import pandas as pd
from sqlalchemy import Integer, String, Float, DateTime

# Carregar o arquivo Excel
file_path = "raw_data.xlsx"
df = pd.read_excel(file_path)

# Removing rows where '"Quantidade Vendida" value 
df = df[df["Quantidade Vendida"] != 0]

# Removing invalid combination of "Status do Pedido" and "Forma de Pagamento"
df = df.drop(df[(df["Status do Pedido"]=="Pago") & (df["Forma de Pagamento"] is None)].index)

# Removing empty values on columns "Data da Venda", "Região", "Vendedor", "Produto" and "Status do Pedido"
df = df.dropna(subset=["Data da Venda", "Região", "Vendedor", "Produto", "Status do Pedido"])

# Removing duplicates values
df = df.drop_duplicates()


# Inicializar Faker
faker = Faker("pt_BR")

# Padronizar nomes das colunas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Criar IDs únicos para entidades
df["produto_id"] = df["produto"].astype("category").cat.codes + 1
df["vendedor_id"] = df["vendedor"].astype("category").cat.codes + 1
df["categoria_id"] = df["categoria_do_produto"].astype("category").cat.codes + 1

# Gerar id_loja aleatório por venda (simulando múltiplas lojas por região)
regiao_lojas = {regiao: [i for i in range(1 + j*3, 4 + j*3)] for j, regiao in enumerate(df["região"].unique())}
df["loja_id"] = df["região"].apply(lambda r: random.choice(regiao_lojas[r]))

# Criar dicionários para tabelas normalizadas
produtos = df[["produto_id", "produto", "categoria_do_produto", "valor_do_produto"]].drop_duplicates().rename(columns={
    "produto": "name",
    "categoria_do_produto": "category",
    "valor_do_produto": "unit_price"
})

vendedores = df[["vendedor_id", "vendedor"]].drop_duplicates().rename(columns={"vendedor": "name"})

clientes = df[["cliente_id"]].drop_duplicates()
clientes["name"] = [faker.name() for _ in range(len(clientes))]

lojas = pd.DataFrame([
    {"store": loja_id, "region": regiao, "address": faker.address().replace("\n", ", ")}
    for regiao, lojas_ids in regiao_lojas.items()
    for loja_id in lojas_ids
])

vendas = df[[
    "data_da_venda", "produto_id", "cliente_id", "vendedor_id", "loja_id",
    "quantidade_vendida", "forma_de_pagamento", "status_do_pedido"
]].copy()
vendas["id_venda"] = range(1, len(vendas)+1)


# Renomear colunas antes de inserir
produtos = produtos.rename(columns={"produto_id": "product_id"})
vendedores = vendedores.rename(columns={"vendedor_id": "seller_id"})
clientes = clientes.rename(columns={"cliente_id": "client_id"})
vendas_sql = vendas.rename(columns={
    "id_venda": "sale_id",
    "data_da_venda": "date",
    "produto_id": "product_id",
    "cliente_id": "client_id",
    "vendedor_id": "seller_id",
    "loja_id": "store_id",
    "quantidade_vendida": "quantity",
    "forma_de_pagamento": "payment",
    "status_do_pedido": "status"
})
vendas_sql['date'] = pd.to_datetime(vendas_sql['date'], format="%d/%m/%Y %H:%M")
vendas_sql['date'] = vendas_sql['date'].astype(str)

dtype_map = {
    'date': String(),
    'product_id': Integer(),
    'client_id': Integer(),
    'seller_id': Integer(),
    'store_id': Integer(),
    'quantity': Integer(),
    'payment': String(),
    'status': String(),
    'id_venda': Integer()
}

# Reabrir conexão
conn = sqlite3.connect("vendas_retail.db")

produtos.to_sql("products", conn, if_exists="replace", index=False)
vendedores.to_sql("sellers", conn, if_exists="replace", index=False)
clientes.to_sql("clients", conn, if_exists="replace", index=False)
lojas.to_sql("stores", conn, if_exists="replace", index=False)
vendas_sql.to_sql("sales", conn, if_exists="replace", index=False)

conn.commit()

queries = {
    "Total de vendas por produto": '''
        SELECT p.name AS product, SUM(v.quantity) AS total_vendido
        FROM sales v
        JOIN products p ON v.product_id = p.product_id
        GROUP BY v.product_id
        ORDER BY total_vendido DESC
        LIMIT 10;
    ''',

    "Faturamento total por loja": '''
        SELECT l.store, l.region, SUM(p.unit_price * v.quantity) AS faturamento
        FROM sales v
        JOIN stores l ON v.store_id = l.store
        JOIN products p ON v.product_id = p.product_id
        GROUP BY l.store
        ORDER BY faturamento DESC
        LIMIT 10;
    ''',

    "Ranking de vendedores por número de pedidos": '''
        SELECT ve.name AS vendedor, COUNT(v.sale_id) AS total_pedidos
        FROM sales v
        JOIN sellers ve ON v.seller_id = ve.seller_id
        GROUP BY ve.name
        ORDER BY total_pedidos DESC
        LIMIT 10;
    ''',

    "Detalhamento de uma venda específica (id_venda = 1)": '''
        SELECT v.sale_id, v.date, c.name AS cliente, ve.name AS vendedor, 
               p.name AS product, v.quantity, v.payment, v.status
        FROM sales v
        JOIN clients c ON v.client_id = c.client_id
        JOIN sellers ve ON v.seller_id = ve.seller_id
        JOIN products p ON v.product_id = p.product_id
        WHERE v.sale_id = 1;
    ''',

    "Vendas por forma de pagamento": '''
        SELECT payment, COUNT(*) AS total_vendas
        FROM sales
        GROUP BY payment
        ORDER BY total_vendas DESC;
    ''',

    "Faturamento por categoria de produto": '''
        SELECT p.category, SUM(p.unit_price * v.quantity) AS faturamento
        FROM sales v
        JOIN products p ON v.product_id = p.product_id
        GROUP BY p.category
        ORDER BY faturamento DESC;
    '''
}

# Executar e exibir resultados
print("Exemplos de queries para testar o Banco de dados")
for titulo, query in queries.items():
    print(f"\n--- {titulo} ---")
    df = pd.read_sql_query(query, conn)
    print(df)

# Fechar conexão
conn.close()
