-- Optimized revenue report query using CTEs (Postgres only)
-- Task 1: Optimize revenue report query from ~70s to <15s.
-- See enhanced_de_prompt_engineering/analyses/analysis-task-01.md for detailed analysis and plan.

-- Checklist based on plan-task-01.md Step 8:
-- [ ] Under 15s on large data (Requires benchmarking on production-scale data)
-- [x] Uses indexes where possible (Indexes recommended in analysis and tested)
-- [x] Test coverage exists (Implemented using pytest)
-- [x] Output schema unchanged (Verified in tests)

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
    where created_at::date = current_date - 1
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    gs.gross_sales,
    coalesce(r.total_refund, 0) as total_refund,
    c.iso_code as currency
from orders as o
    left join gross_sales_per_order as gs on o.order_id = gs.order_id
    left join refunds_per_order as r on o.order_id = r.order_id
    left join currencies as c on o.currency_id = c.currency_id
where o.created_at::date = current_date - 1
order by gs.gross_sales desc;
