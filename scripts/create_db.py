#%%

import pandas as pd
import sqlite3

#%%

#criando o df
df = pd.read_csv('C:\\Users\\Pedro\\Documents\\projetos\\projeto-IBGE\\dados\\dados_gold.csv', sep=';')
df


# %%

#criando conexao
conn = sqlite3.connect('C:/Users/Pedro/Documents/projetos/projeto-IBGE/soja_producao.db')

# %%

#criando tabela
df.to_sql('producao_soja', conn, if_exists='replace', index=False)

# %%

#testando conexao
query = "SELECT * FROM producao_soja LIMIT 5;"
print(pd.read_sql_query(query, conn))

# %%

#teste primeira query 
#1. Liste os 5 municípios com maior produção total de soja no último ano disponível.

query1 = "select municipio, quantidade_produzida from producao_soja where ano=(select max(ano) from producao_soja) order by valor_producao desc limit 5;"
df_query1=pd.read_sql_query(query1, conn)
df_query1.head()

# %%

#teste segunda query
#2. Calcule a produtividade média (ton/ha) da soja por estado.

query2 = "select UF, avg(cast(quantidade_produzida as real)/nullif(area_colhida,0)) as produtividade_media from producao_soja group by UF"
df_query2 = pd.read_sql_query(query2, conn)
df_query2.head()

# %%

#teste terceira query
#3. Mostre a evolução anual da produção total por estado nos últimos 10 anos.

query3 = "select UF, SUM(CASE WHEN ano = 2014 THEN quantidade_produzida ELSE 0 END) AS '2014', SUM(CASE WHEN ano = 2015 THEN quantidade_produzida ELSE 0 END) AS '2015', SUM(CASE WHEN ano = 2016 THEN quantidade_produzida ELSE 0 END) AS '2016', SUM(CASE WHEN ano = 2017 THEN quantidade_produzida ELSE 0 END) AS '2017', SUM(CASE WHEN ano = 2018 THEN quantidade_produzida ELSE 0 END) AS '2018', SUM(CASE WHEN ano = 2019 THEN quantidade_produzida ELSE 0 END) AS '2019', SUM(CASE WHEN ano = 2020 THEN quantidade_produzida ELSE 0 END) AS '2020', SUM(CASE WHEN ano = 2021 THEN quantidade_produzida ELSE 0 END) AS '2021', SUM(CASE WHEN ano = 2022 THEN quantidade_produzida ELSE 0 END) AS '2022', SUM(CASE WHEN ano = 2023 THEN quantidade_produzida ELSE 0 END) AS '2023', SUM(CASE WHEN ano = 2024 THEN quantidade_produzida ELSE 0 END) AS '2024' from producao_soja group by UF order by UF;"
df_query3=pd.read_sql_query(query3, conn)
df_query3.head()


# %%

#teste quarta query
#4. Identifique o estado com maior variação percentual de produção no período.

query4 = "with producao_ano as (select UF, min(ano) as ano_inicial, max(ano) as ano_final, sum(case when ano = (select min(ano) from producao_soja) then valor_producao else 0 end) as producao_inicial, sum(case when ano = (select max(ano) from producao_soja) then valor_producao else 0 end) as producao_final from producao_soja group by UF) select UF, producao_inicial, producao_final, ((producao_final - producao_inicial)*100/nullif(producao_inicial,0)) as variacao_percentual from producao_ano order by variacao_percentual desc limit 5"
df_query4=pd.read_sql_query(query4, conn)
df_query4

# %%

#teste quinta query
#5. Crie uma view chamada 'resumo_soja' com os campos: ano, uf, producao_total, area_total
#e produtividade.
query5 = "create view resumo_soja as select ano, UF, sum(valor_producao) as producao_total, sum(area_colhida) as area_total, (nullif(sum(valor_producao),0)* 1.0 / nullif(sum(area_colhida),0)) as produtividade from producao_soja group by ano, UF;"
pd.read_sql_query(query5,conn)

#%%

#verificar a view recem criada
df_query5=pd.read_sql_query("select * from resumo_soja limit 5", conn)
df_query5

# %%
