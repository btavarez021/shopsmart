with raw_customers as (
    select 
          customerid  as customer_id
        , name as customer_name
        , email as customer_email
        , phone as customer_phone
        , address as customer_address
        , _AIRBYTE_EXTRACTED_AT as updated_at  -- pass-through from raw
     from {{ source('raw', 'customers') }}
)

select 
    customer_id, 
    customer_name, 
    customer_email, 
    customer_phone, 
    customer_address,
    updated_at
from raw_customers