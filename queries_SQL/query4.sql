with producao_ano as (
    select 
        UF,
        min(ano) as ano_inicial,
        max(ano) as ano_final,
        sum(case
                when ano = (select min(ano) from producao_soja)
                then valor_producao
                else 0
            end) as producao_inicial,
        sum(case
                when ano = (select max(ano) from producao_soja)
                then valor_producao
                else 0
            end) as producao_final
    from producao_soja
    group by UF
)
select
    UF,
    producao_inicial,
    producao_final,
    ((producao_final - producao_inicial)*100/nullif(producao_inicial,0)) as variacao_percentual
from producao_ano
order by variacao_percentual desc
limit 5