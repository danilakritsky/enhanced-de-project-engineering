import os
import sqlite3
from typing import Generator  # Import Generator for the fixture return type

import pytest


def read_sql_query(query_file_path: str) -> str:
    with open(query_file_path, 'r') as f:
        return f.read()

@pytest.fixture(scope='function')
def setup_database() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    create_table_sql = '''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer TEXT,
            amount REAL,
            order_date DATE
        );
    '''

    insert_data_sql = '''
        INSERT INTO orders (id, customer, amount, order_date) VALUES
        (1, 'Alice', 5000, '2024-03-01'),
        (2, 'Bob', 8000, '2024-03-05'),
        (3, 'Alice', 3000, '2024-03-15'),
        (4, 'Charlie', 7000, '2024-02-20'),
        (5, 'Alice', 10000, '2024-02-28'),
        (6, 'Bob', 4000, '2024-02-10'),
        (7, 'Charlie', 9000, '2024-03-22'),
        (8, 'Alice', 2000, '2024-03-30');
    '''

    cursor.execute(create_table_sql)
    cursor.execute(insert_data_sql)
    conn.commit()

    yield conn

    conn.close()

# Test for total sales volume for March 2024
def test_total_sales_march_2024(setup_database: sqlite3.Connection) -> None:
    conn: sqlite3.Connection = setup_database
    cursor: sqlite3.Cursor = conn.cursor()

    # Expected: 5000 + 8000 + 3000 + 9000 + 2000 = 27000
    expected_result: float = 27000.00

    query_path: str = os.path.join('enhanced_de_prompt_engineering', 'queries', 'task_02', 'total_sales_march_2024.sql')
    sql_query: str = read_sql_query(query_path)
    sql_query = sql_query.replace('FROM sales', 'FROM orders')
    cursor.execute(sql_query)
    actual_result: float = cursor.fetchone()[0]

    assert actual_result == expected_result


# Test for the top customer by total spend
def test_top_customer_by_spend(setup_database: sqlite3.Connection) -> None:
    conn: sqlite3.Connection = setup_database
    cursor: sqlite3.Cursor = conn.cursor()

    # Expected: Alice (20000)
    expected_result: tuple[str, float] = ('Alice', 20000.00)

    query_path: str = os.path.join('enhanced_de_prompt_engineering', 'queries', 'task_02', 'top_customer_by_spend.sql')
    sql_query: str = read_sql_query(query_path)
    sql_query = sql_query.replace('FROM sales', 'FROM orders')
    cursor.execute(sql_query)
    actual_result: tuple[str, float] | None = cursor.fetchone()

    assert actual_result == expected_result


# Test for the average order value in the last 3 months
def test_average_order_value_last_3_months(setup_database: sqlite3.Connection) -> None:
    conn: sqlite3.Connection = setup_database
    cursor: sqlite3.Cursor = conn.cursor()

    # Expected: 6000
    expected_result: float = 6000.00

    query_path: str = os.path.join('enhanced_de_prompt_engineering', 'queries', 'task_02', 'average_order_value_last_3_months.sql')
    sql_query: str = read_sql_query(query_path)
    sql_query = sql_query.replace('FROM sales', 'FROM orders')
    cursor.execute(sql_query)
    actual_result: float = cursor.fetchone()[0]

    assert actual_result == pytest.approx(expected_result)
