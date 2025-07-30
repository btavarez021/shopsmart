with base as (
    select * from {{ ref('stg_customers') }}
),
customer_deduped as(
select 
    customer_id
    ,customer_name
    , customer_email
    , customer_phone
    , customer_address
    , updated_at
    ,row_number() OVER(partition by customer_id order by updated_at desc) as rn
from base
)

select * 
from customer_deduped
where rn = 1