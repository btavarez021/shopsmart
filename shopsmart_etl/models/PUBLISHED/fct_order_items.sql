{{ config(
    materialized='incremental',
    unique_key = 'order_id'
)}}

with orders as (
    select * from {{ ref('stg_orders') }}
    {% if is_incremental() %}
    where order_date > (select max(order_date) from {{ this }})
    {% endif %}
),

products as (
    select * from {{ ref('stg_products') }}
),

customers as (
    select * from {{ ref('dim_customers') }}
)

select 
    o.order_id,
    o.order_date,
    o.order_qty,
    o.customer_id,
    c.customer_name,
    c.customer_email,
    c.customer_phone,
    p.product_id,
    p.product_name,
    p.product_category,
    p.product_price,
    o.order_qty * p.product_price  as total_price,
    CURRENT_TIMESTAMP() as etl_date 
from orders o
left join customers c on o.customer_id = c.customer_id
left join products p on o.product_id = p.product_id