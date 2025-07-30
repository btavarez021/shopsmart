with raw_products as (
    select 
        NAME as product_name,
        PRICE as product_price,
        CATEGORY as product_category,
        PRODUCTID as product_id
    from {{ source('raw', 'products') }}
)
select 
    product_id, 
    product_name, 
    product_price, 
    product_category
from raw_products