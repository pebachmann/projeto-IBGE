select
    UF,
    sum(case when ano = 2014 then quantidade_produzida else 0 end) as '2014',
    sum(case when ano = 2015 then quantidade_produzida else 0 end) as '2015',
    sum(case when ano = 2016 then quantidade_produzida else 0 end) as '2016',
    sum(case when ano = 2017 then quantidade_produzida else 0 end) as '2017',
    sum(case when ano = 2018 then quantidade_produzida else 0 end) as '2018',
    sum(case when ano = 2019 then quantidade_produzida else 0 end) as '2019',
    sum(case when ano = 2020 then quantidade_produzida else 0 end) as '2020',
    sum(case when ano = 2021 then quantidade_produzida else 0 end) as '2021',
    sum(case when ano = 2022 then quantidade_produzida else 0 end) as '2022',
    sum(case when ano = 2023 then quantidade_produzida else 0 end) as '2023',
    sum(case when ano = 2024 then quantidade_produzida else 0 end) as '2024'
from producao_soja
group by UF
order by UF