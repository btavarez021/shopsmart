with raw_orders as (
    select 
        PRICE as product_price,
        ORDERID as order_id,
        QUANTITY as order_qty,
        ORDERDATE as order_date,
        PRODUCTID as product_id,
        CUSTOMERID as customer_id
    FROM 
    {{ source('raw', 'orders') }}
)
select 
    order_id, 
    order_date, 
    order_qty,
    product_id,
    product_price
    product_category,
    customer_id
from raw_orders