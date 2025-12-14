
create view resumo_soja as 
select 
    ano,
    UF, 
    sum(valor_producao) as producao_total, 
    sum(area_colhida) as area_total, 
    (nullif(sum(valor_producao),0)* 1.0 / nullif(sum(area_colhida),0)) as produtividade
from producao_soja 
group by ano, UF