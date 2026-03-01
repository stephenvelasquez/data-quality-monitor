with source as (
    select * from {{ source('raw', 'orders') }}
),
cleaned as (
    select
        cast(order_id as varchar(36))        as order_id,
        cast(customer_id as varchar(36))     as customer_id,
        cast(order_date as date)             as order_date,
        cast(total_amount as decimal(12,2))  as total_amount,
        cast(currency as varchar(3))         as currency,
        cast(status as varchar(20))          as status,
        cast(channel as varchar(20))         as channel,
        cast(created_at as timestamp)        as created_at,
        case when total_amount < 0 then true else false end        as _is_negative_amount,
        case when order_date > current_date then true else false end as _is_future_date,
        case when customer_id is null then true else false end      as _is_orphan_order
    from source
    where order_id is not null
)
select * from cleaned
