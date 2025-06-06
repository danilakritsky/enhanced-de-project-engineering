select SUM(amount)
from orders
where order_date between '2024-03-01' and '2024-03-31';
