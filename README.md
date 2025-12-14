# 📊 Análise

**Tema:** Produção de Soja no Brasil (IBGE – Produção Agrícola Municipal)

**Ferramentas Utilizadas:** Python, SQLite, SQL, Power BI

---

## 🧩 1. Contexto

Este projeto tem como objetivo analisar a produção de soja no Brasil com base nos dados da **Produção Agrícola Municipal (PAM)**, disponibilizados pelo IBGE.

A base contém informações anuais de cada município brasileiro sobre:

* Área colhida (hectares)
* Quantidade produzida (toneladas)
* Valor da produção (mil R$)

O período analisado compreende os últimos **10 anos disponíveis** na base de dados.

**Fonte:**
IBGE – Produção Agrícola Municipal (PAM)

---

## ⚙️ 2. Etapa 1 – Criação e Estruturação do Banco de Dados

### 🔹 2.1. Criação do Banco SQLite

A base original foi tratada em Python (pandas) e exportada para o formato SQLite.

A tabela principal criada possui a seguinte estrutura:

| Coluna               | Descrição                        |
| -------------------- | -------------------------------- |
| ano                  | Ano de referência                |
| uf                   | Unidade da Federação             |
| municipio            | Nome do município                |
| area_colhida         | Área colhida (ha)                |
| quantidade_produzida | Produção total (ton)             |
| valor_producao       | Valor total da produção (mil R$) |

---

### 🔹 2.2. Consultas SQL Desenvolvidas

#### 1️⃣ Maiores produtores do último ano disponível

```sql
SELECT municipio, SUM(quantidade_produzida) AS producao_total
FROM producao_soja
WHERE ano = (SELECT MAX(ano) FROM producao_soja)
GROUP BY municipio
ORDER BY producao_total DESC
LIMIT 5;
```

#### 2️⃣ Produtividade média (ton/ha) por estado

```sql
SELECT uf, 
       SUM(quantidade_produzida) / SUM(area_colhida) AS produtividade_media
FROM producao_soja
GROUP BY uf
ORDER BY produtividade_media DESC;
```

#### 3️⃣ Evolução anual da produção por estado (últimos 10 anos)

```sql
SELECT uf, ano, SUM(quantidade_produzida) AS producao_total
FROM producao_soja
GROUP BY uf, ano
ORDER BY uf, ano;
```

#### 4️⃣ Estado com maior variação percentual de produção no período

```sql
WITH producao_inicial_final AS (
    SELECT
        uf,
        MIN(ano) AS ano_inicial,
        MAX(ano) AS ano_final,
        SUM(CASE WHEN ano = (SELECT MIN(ano) FROM producao_soja)
                 THEN quantidade_produzida ELSE 0 END) AS producao_inicial,
        SUM(CASE WHEN ano = (SELECT MAX(ano) FROM producao_soja)
                 THEN quantidade_produzida ELSE 0 END) AS producao_final
    FROM producao_soja
    GROUP BY uf
)
SELECT
    uf,
    producao_inicial,
    producao_final,
    ((producao_final - producao_inicial) * 100.0 / NULLIF(producao_inicial, 0)) AS variacao_percentual
FROM producao_inicial_final
ORDER BY variacao_percentual DESC
LIMIT 5;
```

#### 5️⃣ Criação da view `resumo_soja`

```sql
CREATE VIEW resumo_soja AS
SELECT
    ano,
    uf,
    SUM(quantidade_produzida) AS producao_total,
    SUM(area_colhida) AS area_total,
    (SUM(quantidade_produzida) / SUM(area_colhida)) AS produtividade
FROM producao_soja
GROUP BY ano, uf;
```

---

## 📈 3. Etapa 2 – Desenvolvimento do Dashboard no Power BI

### 🔹 3.1. Conexão com o Banco SQLite

A conexão foi realizada via Power BI Desktop → Obter Dados → Banco de Dados → SQLite Database.

Após o carregamento das tabelas e da view `resumo_soja`, foram criadas as seguintes visualizações.

### 🔹 3.2. Perguntas de Negócio Respondidas

1. **Produção total e área colhida no último ano**
   Indicadores de valor total e área colhida agregados.

2. **Evolução da produção e produtividade ao longo dos anos**
   Gráfico de linhas com série temporal.

3. **Estados com maior produção**
   Mapa geográfico e ranking horizontal.

4. **Estados com maior produtividade (ton/ha)**
   Gráfico de barras ordenado.

5. **Relação entre área colhida e produção total**
   Gráfico de dispersão com correlação positiva.

---

## 🧠 4. Principais Insights

* A produção de soja cresceu de forma consistente ao longo da última década, porém com um declive na produtividade nos últimos anos.
* O estado do Mato Grosso se destaca como o maior produtor nacional.
* A produtividade média nacional (ton/ha) vem aumentando, refletindo avanços tecnológicos evidentes, principalmente no ramo da gestão agrícola e produção consciente.
* Existe correlação direta entre área colhida e produção, sendo verificado um crescimento expressivo na área colhida e produção nos últimos anos, variáveis diretamente proporcionais.

---

## 📦 5. Entregáveis

| Arquivo             | Descrição                                                       |
| ------------------- | --------------------------------------------------------------- |
| producao_soja.db    | Banco de dados SQLite com tabela e view `resumo_soja`           |
| consultas.sql       | Arquivo com todas as queries utilizadas                         |
| dashboard_soja.pbix | Dashboard interativo desenvolvido no Power BI                   |
| relatorio_final.pdf | Documento com descrição do processo, consultas SQL e conclusões |

---

## 🧰 Tecnologias e Ferramentas Utilizadas

* Python (pandas, sqlite3) – Limpeza e estruturação dos dados
* SQLite – Armazenamento e consultas SQL
* Power BI – Conexão com banco, modelagem e visualização de dados
* Excel – Apoio na análise exploratória
* GitHub – Versionamento e compartilhamento do projeto

---

## 🚀 Próximos Passos (opcional)

* Criar KPIs comparativos de produtividade entre anos
* Incorporar dados climáticos (chuva e temperatura) para análises preditivas
* Migrar o banco para PostgreSQL e automatizar a atualização dos dados
