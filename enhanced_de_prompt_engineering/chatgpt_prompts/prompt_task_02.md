Create a detailed, step-by-step plan to build the project, starting from a high-level blueprint.
This is an end to end plan that will be given an LLM agent to guide it in solving the task.
Treat the agent as a proficient data engineer.
You need to write the instructions in a way so that any LLM agent will find it straightforward and easy to follow. The plan should also promote iterative development, with clearly defined subtasks.

Break the plan into smaller, incremental tasks that are easy to test and implement safely, while still moving the project forward.
Iterate on the task breakdown until each step is the right size, no big jumps, no isolated code.
Once finalized, turn each step into a well-structured code-generation prompt for an LLM.

Use test-driven development, follow best practices, and ensure that each prompt builds on the last, with all code fully integrated.
Tests should be written before queries, as is expected with TDD.
Format each prompt clearly using markdown, tagged as code. Avoid leaving unused or disconnected code.

The LLM should provide the solution to the task in a markdown file, with explanations.
Code should be saved in respective source files.

You should not make any make assumptions about the project's strucuture let the LLM agent figure it out itself.
LLM should respect the current project structure and the existing solutions to the previous task should not be modified.
In order to understand the repo outline better LLM should start with scanning the existing files and directories, and only after that move on with working on the solution.
Source files should be placed into respective directories identified by the LLM during repo structure analysis.



This is the second task that LLM should solve.
IMPORTANT Don't solve the task yourself, don't generate any code, don't suggest project structure, filenames  - simply provide a step by step plan, and emphasize project goals and ahering to the existing project structure.

The deliverables that we need to provide are SQL files with the queries, tests for running the queries, and step by step analysis outlining each step the Agent takes when solving the task.

IMPORTANT Return the plan as a single markdown block and make sure to not use ANY nested markdown blocks.

# Task 2

## Goal:
Write SQL queries to analyze sales data for an online store.
Tools to Use:
SQLite Online


CursorAI/ChatGPT to generate and refine SQL queries


Input Data (Script to Populate the Table):
Run this script in SQLite Online:

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer TEXT,
    amount REAL,
    order_date DATE
);

INSERT INTO orders (customer, amount, order_date) VALUES
('Alice', 5000, '2024-03-01'),
('Bob', 8000, '2024-03-05'),
('Alice', 3000, '2024-03-15'),
('Charlie', 7000, '2024-02-20'),
('Alice', 10000, '2024-02-28'),
('Bob', 4000, '2024-02-10'),
('Charlie', 9000, '2024-03-22'),
('Alice', 2000, '2024-03-30');
```


## Tasks:
Calculate the total sales volume for March 2024.
Find the customer who spent the most overall.
Calculate the average order value for the last three months.


## Expected Results:
Total sales for March: 27,000
Top-spending customer: Alice (20,000 )
Average order value (total sales / number of orders): 6,000
