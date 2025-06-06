select
    customer,
    SUM(amount) as total_spend
from orders
group by customer
order by total_spend desc
limit 1;
