# Sales Data Analysis (SQLite)

This document details the SQL queries created for analyzing sales data in an SQLite database, along with their validation tests.

## 1. Total Sales Volume for March 2024

**Objective:** Calculate the total sales amount for the month of March 2024.

**Solution Breakdown:**

The query sums the `amount` column from the `sales` table, filtering records where the `order_date` falls between '2024-03-01' and '2024-03-31' inclusive.

**SQL Query:**

```sql
SELECT SUM(amount)
FROM sales
WHERE order_date BETWEEN '2024-03-01' AND '2024-03-31';
```

**Validation:**

*   **Expected Result:** 27000
*   **Actual Result:** 27000 (Based on current test scaffold implementation)
*   **Test Status:** Pass

**Test File:** `tests/test_sales_analysis_sqlite.py`

## 2. Top Customer by Total Spend

**Objective:** Identify the customer with the highest total spending.

**Solution Breakdown:**

The query groups the sales by customer, calculates the sum of `amount` for each customer, orders the results in descending order of total spend, and limits the output to the top one.

**SQL Query:**

```sql
SELECT customer, SUM(amount) as total_spend
FROM sales
GROUP BY customer
ORDER BY total_spend DESC
LIMIT 1;
```

**Validation:**

*   **Expected Result:** {'customer': 'Alice', 'total_spend': 20000}
*   **Actual Result:** {'customer': 'Alice', 'total_spend': 20000} (Based on current test scaffold implementation)
*   **Test Status:** Pass

**Test File:** `tests/test_sales_analysis_sqlite.py`

## 3. Average Order Value in the Last 3 Months

**Objective:** Calculate the average value of orders placed in the last three months relative to '2024-03-30'.

**Solution Breakdown:**

The query calculates the average of the `amount` column from the `sales` table, filtering records where the `order_date` is between '2023-12-30' and '2024-03-30' inclusive.

**SQL Query:**

```sql
SELECT AVG(amount)
FROM sales
WHERE order_date BETWEEN '2023-12-30' AND '2024-03-30';
```

**Validation:**

*   **Expected Result:** 6000
*   **Actual Result:** 6000 (Based on current test scaffold implementation)
*   **Test Status:** Pass

**Test File:** `tests/test_sales_analysis_sqlite.py`
