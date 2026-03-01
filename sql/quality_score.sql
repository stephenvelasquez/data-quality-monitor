with completeness as (
    select 'stg_orders' as table_name, count(*) as total_rows,
        sum(case when _is_negative_amount then 1 else 0 end) as invalid_rows,
        1.0 - (sum(case when _is_negative_amount then 1 else 0 end)::float / nullif(count(*),0)) as score
    from stg_orders
)
select table_name, round(score * 100, 1) as quality_score, total_rows, invalid_rows
from completeness order by quality_score asc
