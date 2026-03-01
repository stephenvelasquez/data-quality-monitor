with orders as (
    select * from {{ ref('stg_orders') }}
    where not _is_negative_amount and not _is_future_date and status != 'cancelled'
),
aggregated as (
    select
        order_date, channel, currency,
        count(distinct order_id)   as order_count,
        count(distinct customer_id) as unique_customers,
        sum(total_amount)          as gross_revenue,
        avg(total_amount)          as avg_order_value
    from orders
    group by order_date, channel, currency
)
select *,
    avg(gross_revenue) over (partition by channel, currency order by order_date rows between 6 preceding and current row) as revenue_7d_ma,
    gross_revenue - lag(gross_revenue) over (partition by channel, currency order by order_date) as revenue_dod_change
from aggregated
