with source as (
    select * from {{ source('raw', 'customers') }}
),
cleaned as (
    select
        cast(customer_id as varchar(36))       as customer_id,
        cast(email as varchar(255))            as email,
        cast(segment as varchar(20))           as segment,
        cast(country as varchar(2))            as country,
        cast(created_at as timestamp)          as created_at,
        cast(lifetime_value as decimal(12,2))  as lifetime_value,
        case when email not like '%@%.%' then true else false end as _is_invalid_email,
        case when segment not in ('enterprise','mid_market','smb','consumer') then true else false end as _is_unknown_segment
    from source
    where customer_id is not null
)
select * from cleaned
