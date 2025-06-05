# Task 1
A nightly job generates the “Yesterday Revenue & Refunds” CSV for Finance.
Since feature growth, the query now takes ~70 s on the warehouse (PostgreSQL 15).
Finance needs it below 15 s to meet the SLA.

## SQL
```sql
SELECT
  o.order_id,
  o.customer_id,
  SUM(CASE WHEN oi.status = 'FULFILLED' THEN oi.quantity * oi.unit_price ELSE 0 END) AS gross_sales,
  COALESCE(r.total_refund, 0) AS total_refund,
  c.iso_code                                   AS currency
FROM orders o
LEFT JOIN order_items oi
      ON oi.order_id = o.order_id
LEFT JOIN (
  SELECT
      order_id,
      SUM(amount) AS total_refund
  FROM refunds
  WHERE created_at::date = CURRENT_DATE - 1
  GROUP BY order_id
) r ON r.order_id = o.order_id
LEFT JOIN currencies c
      ON c.currency_id = o.currency_id
WHERE o.created_at::date = CURRENT_DATE - 1
GROUP BY
  o.order_id, o.customer_id, r.total_refund, c.iso_code
ORDER BY gross_sales DESC;
```

## Goal
Prompt ChatGPT to spot bottlenecks (two big sequential scans, three hash joins, spill risk).
Ask it for at least two optimisation strategies, e.g.
Rewrite with window functions to remove the self-aggregating sub-query.
Filter early by moving status='FULFILLED' and the date predicate into CTEs.
Create a partial index on order_items(created_at, status, order_id) WHERE status=‘FULFILLED’.


In Cursor: In the repo open revenue_report.sql, highlight the query, press Ctrl + K →
“Rewrite to use a single window-function to pass over order_items (partition by order_id) and JOIN that result to orders. Eliminate the refunds sub-query by turning it into a window sum on refunds with a FILTER clause. Add EXPLAIN ANALYZE before and after.”

Experiment and try ChatGPT as well as Cursor.
