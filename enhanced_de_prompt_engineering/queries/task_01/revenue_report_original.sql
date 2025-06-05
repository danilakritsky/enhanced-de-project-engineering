-- Original revenue report query
with r as (
    select
        order_id,
        SUM(amount) as total_refund
    from refunds
    where created_at::date = CURRENT_DATE - 1
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    SUM(case when oi.status = 'FULFILLED' then oi.quantity * oi.unit_price else 0 end) as gross_sales,
    COALESCE(r.total_refund, 0) as total_refund,
    c.iso_code as currency
from orders as o
    left join order_items as oi on o.order_id = oi.order_id
    left join r on o.order_id = r.order_id
    left join currencies as c on o.currency_id = c.currency_id
where o.created_at::date = CURRENT_DATE - 1
group by o.order_id, o.customer_id, r.total_refund, c.iso_code
order by gross_sales desc;
