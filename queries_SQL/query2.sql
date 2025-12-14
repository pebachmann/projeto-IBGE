select
    UF,
    avg(cast(quantidade_produzida as real)/nullif(area_colhida,0)) as produtividade_media
from producao_soja
group by UF