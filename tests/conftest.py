import os

import psycopg2
import pytest

POSTGRES_DSN = os.getenv(
    "POSTGRES_TEST_DSN",
    "dbname=de_test user=de_test password=de_test host=localhost port=5432"
)

@pytest.fixture(scope="module")
def pg_conn():
    """
    Set up a PostgreSQL connection for testing. Ensures a clean schema and sample data for all tests.
    """
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
