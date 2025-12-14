#%%
import pandas as pd

#%%

# Lendo o arquivo
file_path = "C:\\Users\\Pedro\\Documents\\projetos\\projeto-IBGE\\dados\\tabela1612-producao.csv"
df = pd.read_csv(file_path, sep = ";", skiprows=4)
df = df.iloc[:-23]

#%%

# arrumando colunas para o melt
df.columns=["municipio",
           "area_colhida-2014","quantidade_produzida-2014","valor_producao-2014",
           "area_colhida-2015","quantidade_produzida-2015","valor_producao-2015",
           "area_colhida-2016","quantidade_produzida-2016","valor_producao-2016",
           "area_colhida-2017","quantidade_produzida-2017","valor_producao-2017",
           "area_colhida-2018","quantidade_produzida-2018","valor_producao-2018",
           "area_colhida-2019","quantidade_produzida-2019","valor_producao-2019",
           "area_colhida-2020","quantidade_produzida-2020","valor_producao-2020",
           "area_colhida-2021","quantidade_produzida-2021","valor_producao-2021",
           "area_colhida-2022","quantidade_produzida-2022","valor_producao-2022",
           "area_colhida-2023","quantidade_produzida-2023","valor_producao-2023",
           "area_colhida-2024","quantidade_produzida-2024","valor_producao-2024"]
df.info()
# %%

# aplicando o melt
df_melt = pd.melt(
    df,
    id_vars=["municipio"],
    value_vars=["area_colhida-2014","quantidade_produzida-2014","valor_producao-2014",
           "area_colhida-2015","quantidade_produzida-2015","valor_producao-2015",
           "area_colhida-2016","quantidade_produzida-2016","valor_producao-2016",
           "area_colhida-2017","quantidade_produzida-2017","valor_producao-2017",
           "area_colhida-2018","quantidade_produzida-2018","valor_producao-2018",
           "area_colhida-2019","quantidade_produzida-2019","valor_producao-2019",
           "area_colhida-2020","quantidade_produzida-2020","valor_producao-2020",
           "area_colhida-2021","quantidade_produzida-2021","valor_producao-2021",
           "area_colhida-2022","quantidade_produzida-2022","valor_producao-2022",
           "area_colhida-2023","quantidade_produzida-2023","valor_producao-2023",
           "area_colhida-2024","quantidade_produzida-2024","valor_producao-2024"
        ],
        var_name="descricao_dados",
        value_name="valores"
)
df_melt.head(10)

df_bronze = df_melt

# %%

# separando o ano da descricao
df_bronze[["descricao", "ano"]]= df_bronze["descricao_dados"].str.rsplit('-', n=1, expand=True)


#%%

# alterando formato de data
df_bronze['ano'] = pd.to_datetime(df_bronze["ano"], format ="%Y")


#%%

# alterando formato de data
df_bronze["ano"] = df_bronze["ano"].dt.year


#%%

# definindo a descricao como variavel categorica
df_bronze["descricao"] = df_bronze["descricao"].astype("category")


#%%

#separando municipio do UF
df_bronze[["municipio", "UF"]]= df_bronze["municipio"].str.rsplit(' ', n=1, expand=True)


#%%

#reorganizando colunas
ordem = ['ano', 'UF', 'municipio', 'descricao', 'valores']
df_bronze = df_bronze[ordem]
df_bronze


#%%

#tratando zeros
df_bronze["valores"]=df_bronze['valores'].replace('-', 0)


#%%

#limpando espacos nos valores
df_bronze["valores"]=df_bronze["valores"].str.strip()


#%%

#convertendo para numerico e valores invalidos viram nan
df_bronze['valores'] = pd.to_numeric(df_bronze['valores'], errors='coerce')


#%%

#alterando tipo
df_bronze['valores'] = df_bronze['valores'].astype('float')


#%%

#limpando coluna de UF com ()
df_bronze['UF']=df_bronze['UF'].str.replace('(','', regex=False).str.replace(')','', regex=False)

# %%

#colocando 0 para nan
df_bronze['valores']=df_bronze['valores'].fillna(0)

df_silver = df_bronze

#%%

#criando colunas para variavel categorica
df_pivot= df_silver.pivot_table(
    index=['ano', 'UF', 'municipio'],
    columns='descricao',
    values='valores'
).reset_index()

df_gold = df_pivot

#%%

#exportando dados
df_gold.to_csv('C:\\Users\\Pedro\\Documents\\projetos\\projeto-IBGE\\dados\\dados_gold.csv', index=False, sep=';', encoding='utf-8-sig')

# %%
