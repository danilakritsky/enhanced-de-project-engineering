-- Optimized revenue report query using CTEs (SQLite/Postgres compatible)
with gross_sales_per_order as (
    select
        order_id,
        sum(quantity * unit_price) as gross_sales
    from order_items
    where status = 'FULFILLED'
    group by order_id
),

refunds_per_order as (
    select
        order_id,
        coalesce(sum(amount), 0) as total_refund
    from refunds
    where created_at = '2024-06-10'
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    gs.gross_sales,
    c.iso_code as currency,
    coalesce(r.total_refund, 0) as total_refund
from orders as o
    left join gross_sales_per_order as gs on o.order_id = gs.order_id
    left join refunds_per_order as r on o.order_id = r.order_id
    left join currencies as c on o.currency_id = c.currency_id
where o.created_at = '2024-06-10'
order by gs.gross_sales desc;
