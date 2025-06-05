### Step 1 — Analyze the Query Plan
You're a PostgreSQL performance expert. Analyze the following query:
```sql
SELECT
  o.order_id,
  o.customer_id,
  SUM(CASE WHEN oi.status = 'FULFILLED' THEN oi.quantity * oi.unit_price ELSE 0 END) AS gross_sales,
  COALESCE(r.total_refund, 0) AS total_refund,
  c.iso_code AS currency
FROM orders o
LEFT JOIN order_items oi ON oi.order_id = o.order_id
LEFT JOIN (
  SELECT order_id, SUM(amount) AS total_refund
  FROM refunds
  WHERE created_at::date = CURRENT_DATE - 1
  GROUP BY order_id
) r ON r.order_id = o.order_id
LEFT JOIN currencies c ON c.currency_id = o.currency_id
WHERE o.created_at::date = CURRENT_DATE - 1
GROUP BY o.order_id, o.customer_id, r.total_refund, c.iso_code
ORDER BY gross_sales DESC;
```

Simulate or describe what EXPLAIN ANALYZE would likely show. Identify performance bottlenecks such as:

Hash joins

Sequential scans

Subquery inefficiencies

Memory spills

Explain why each issue matters. Output in markdown with sections. No fixes yet, just analysis.

### Step 2 — Recommend Two Optimization Strategies

Based on the analysis of the query above, propose at least **two distinct** strategies to optimize the SQL. Each strategy should:

- Describe how it changes the query structure
- Explain what bottlenecks it addresses
- Mention any required indexes
- Predict the performance impact

Output in markdown, with one section per strategy. Label one as "Window Function Strategy" and another as "CTE + Early Filter Strategy".

Rewrite the SQL using **window functions** to remove the subquery on `refunds`. Apply these changes:

- Remove the `refunds` subquery and replace with a `SUM(amount) FILTER (WHERE created_at = CURRENT_DATE - 1)` window function.
- Use a single window over `order_items` partitioned by `order_id` to compute `gross_sales`.
- Ensure `LEFT JOIN` logic is preserved.

Return the full rewritten query with inline comments. Also include a section titled "Explanation" to describe the changes and why they help.

### Step 3 — Window Function Rewrite

Rewrite the SQL using **window functions** to remove the subquery on `refunds`. Apply these changes:

- Remove the `refunds` subquery and replace with a `SUM(amount) FILTER (WHERE created_at = CURRENT_DATE - 1)` window function.
- Use a single window over `order_items` partitioned by `order_id` to compute `gross_sales`.
- Ensure `LEFT JOIN` logic is preserved.

Return the full rewritten query with inline comments. Also include a section titled "Explanation" to describe the changes and why they help.

### Step 4 -- Replace Subquery with FILTER
Update the previous query to eliminate the aggregate subquery over `refunds`.

- Replace it with a `SUM(amount) FILTER (...) OVER (PARTITION BY order_id)` inline in the main SELECT.
- Remove the subquery join entirely.

Output the final query with all parts integrated, and include a markdown explanation.

### Step 5 — Use CTEs for Early Filtering
Refactor the optimized query to use CTEs that apply filtering early:

- Create a `filtered_orders` CTE that selects from `orders` where `created_at = CURRENT_DATE - 1`.
- Create a `filtered_order_items` CTE where `status = 'FULFILLED'` and joined with the above.
- Rewrite the main query to use these CTEs.

Return the updated query and explain how this reduces scan size and improves join performance.

### Step 6 — Recommend Indexes
Based on the optimized query, propose useful PostgreSQL indexes to improve performance.

- Index suggestions should be partial and selective
- Explain for each: which table, columns, and filter clause
- Mention if the index helps a join, filter, or aggregate

Format the suggestions as `CREATE INDEX` statements with explanations.

### Step 7 — Benchmark With EXPLAIN ANALYZE
Wrap the original and optimized queries with `EXPLAIN (ANALYZE, BUFFERS)`.

- Compare runtime, shared read blocks, and memory usage
- Highlight changes in join strategy (hash vs nested loop, etc.)
- Recommend which version to keep based on benchmark

Output a side-by-side markdown table and summary.

### Step 8 — Final Query for Production
Output the final optimized query, combining:
- CTE filtering
- Window-function aggregation
- Inline refund calculation with FILTER
- All relevant joins and columns

Save to `queries/revenue_report.sql`.
Add comments and include a section with a checklist:
- [x] Under 15s on large data
- [x] Uses indexes where possible
- [x] Test coverage exists
- [x] Output schema unchangedStep 8 — Final Query for Production
