# 📦 Project Plan: Task 2 – Sales Data Analysis Using SQL

## 🧠 Project Objective
Create and validate SQL queries that analyze sales data stored in an SQLite database. Queries should provide accurate and reproducible results for total March 2024 sales, the top customer by spend, and the average order value over the last three months. Deliverables include SQL scripts, corresponding automated tests, and detailed analysis steps.

## 👨‍🔧 Agent Instructions
You are a data engineering agent working iteratively with a project repository. Your task is to **generate new code only**, never modify existing files unless explicitly told to. Begin every task by understanding the current repository structure to integrate your work seamlessly. All work must be version-safe, test-driven, and well-documented.

---

## 🔁 Step-by-Step Iterative Plan

### Phase 1: Repository Scanning

**Task 2.1**:  
Scan the repository to understand:
- Directory layout
- Naming conventions
- Existing scripts, modules, or test patterns
- Where SQL queries and test logic are stored

*Goal*: Identify the appropriate locations to place query scripts, test cases, and markdown explanations.

---

### Phase 2: Test-First Query Development

**Task 2.2**:  
Create a test scaffold for validating the query: *total sales volume for March 2024*.  
Include:
- Test name and purpose
- Expected result: `27000`
- Strategy to isolate March 2024 sales
- Stub for SQL query to be implemented in the next step

**Task 2.3**:  
Write SQL query to compute total sales for March 2024.
Store the query in the appropriate source directory.
Ensure:
- Uses correct date filtering logic (`order_date` between `2024-03-01` and `2024-03-31`)
- Returns single numeric result

---

**Task 2.4**:  
Create a test scaffold for the query: *find the top customer by total spend*.  
Include:
- Expected result: `Alice (20000)`
- Strategy: `GROUP BY customer`, `SUM(amount)`, `ORDER BY total DESC LIMIT 1`

**Task 2.5**:  
Write SQL query to compute top-spending customer.
Store and link this with the appropriate test.

---

**Task 2.6**:  
Create a test scaffold for the query: *average order value in the last 3 months*.  
Include:
- Expected result: `6000`
- Strategy: `AVG(amount)` where order date is within 3 months of last order (`2024-03-30`)
- Validate number of orders and total amount

**Task 2.7**:  
Write SQL query to compute average order value.
Include logic for defining "last 3 months" window.
Store SQL and validate with test.

---

### Phase 3: Documentation & Outputs

**Task 2.8**:  
Create a single markdown file that:
- Explains each query’s logic and validation
- Lists expected vs. actual results
- Shows tests run and their pass/fail status

**Task 2.9**:  
Ensure all SQL queries are saved in standalone `.sql` files and tests are located with other test cases.

---

## 🔍 Summary of Deliverables

- `.sql` files for each query, named per repo conventions
- Test files for each SQL file with clear assertions
- Markdown analysis file detailing:
  - Query objective
  - Step-by-step solution breakdown
  - Query result and validation
- All files placed in correct directories as discovered by the LLM agent during repository scan

---

## 🔒 Constraints
- Never edit existing files
- Queries must run in SQLite syntax
- All results must be validated through tests
- Use test-driven development principles throughout
