select order_date, channel, gross_revenue
from {{ ref('fct_daily_revenue') }}
where gross_revenue < 0
