select
    municipio,
    quantidade_produzida
from producao_soja
where ano=(select max(ano) from producao_soja)   
order by valor_producao desc
limit 5;