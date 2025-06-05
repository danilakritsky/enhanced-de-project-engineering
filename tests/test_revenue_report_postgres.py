import os
from decimal import Decimal
from typing import Any, List, Tuple

import psycopg2
import pytest

POSTGRES_DSN = os.getenv(
    "POSTGRES_TEST_DSN",
    "dbname=de_test user=de_test password=de_test host=localhost port=5432"
)

def convert_decimals(row: Tuple[Any, ...]) -> Tuple[Any, ...]:
    """Convert Decimal values in a tuple to float for comparison."""
    return tuple(float(x) if isinstance(x, Decimal) else x for x in row)

@pytest.fixture(scope="module")
def pg_conn():
    """Set up a PostgreSQL connection for testing. Assumes Dockerized Postgres is running."""
    conn = psycopg2.connect(POSTGRES_DSN)
    cur = conn.cursor()
    # Drop and recreate tables for a clean slate
    cur.execute("""
        DROP TABLE IF EXISTS order_items, refunds, orders, currencies CASCADE;
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            currency_id INTEGER,
            created_at DATE
        );
        CREATE TABLE order_items (
            item_id SERIAL PRIMARY KEY,
            order_id INTEGER,
            status TEXT,
            quantity INTEGER,
            unit_price NUMERIC,
            created_at DATE
        );
        CREATE TABLE refunds (
            refund_id SERIAL PRIMARY KEY,
            order_id INTEGER,
            amount NUMERIC,
            created_at DATE
        );
        CREATE TABLE currencies (
            currency_id INTEGER PRIMARY KEY,
            iso_code TEXT
        );
    """)
    # Insert sample data
    cur.execute("""
        INSERT INTO currencies VALUES (1, 'USD');
        INSERT INTO currencies VALUES (2, 'EUR');

        INSERT INTO orders VALUES (100, 10, 1, '2024-06-10');
        INSERT INTO orders VALUES (101, 11, 2, '2024-06-10');
        INSERT INTO orders VALUES (102, 12, 1, '2024-06-09');

        INSERT INTO order_items (order_id, status, quantity, unit_price, created_at) VALUES
            (100, 'FULFILLED', 2, 50.0, '2024-06-10'),
            (100, 'CANCELLED', 1, 50.0, '2024-06-10'),
            (101, 'FULFILLED', 1, 100.0, '2024-06-10'),
            (102, 'FULFILLED', 1, 75.0, '2024-06-09');

        INSERT INTO refunds (order_id, amount, created_at) VALUES
            (100, 20.0, '2024-06-10'),
            (101, 10.0, '2024-06-10'),
            (102, 5.0, '2024-06-09');
    """)
    conn.commit()
    yield conn
    cur.close()
    conn.close()

def run_revenue_report_query_pg(conn, query: str) -> List[Tuple]:
    """Helper to run the revenue report query and return all results."""
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()

def test_revenue_report_basic_postgres(pg_conn):
    """
    Test the revenue report query for orders on 2024-06-10 in PostgreSQL.
    """
    with open("enhanced_de_prompt_engineering/queries/revenue_report.sql") as f:
        query = f.read()
    results = run_revenue_report_query_pg(pg_conn, query)
    # Convert Decimal to float for comparison
    results = [convert_decimals(row) for row in results]
    expected = [
        (100, 10, 100.0, 20.0, 'USD'),
        (101, 11, 100.0, 10.0, 'EUR'),
    ]
    assert results == expected
