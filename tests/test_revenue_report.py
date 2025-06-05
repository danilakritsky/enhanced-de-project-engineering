import sqlite3
from typing import List, Tuple

import pytest


@pytest.fixture
def db():
    """Set up an in-memory SQLite database with the required schema and sample data."""
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    # Create tables
    cur.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            currency_id INTEGER,
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            status TEXT,
            quantity INTEGER,
            unit_price REAL,
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE refunds (
            refund_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            amount REAL,
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE currencies (
            currency_id INTEGER PRIMARY KEY,
            iso_code TEXT
        )
    """)
    # Insert sample data
    cur.executescript("""
        INSERT INTO currencies VALUES (1, 'USD');
        INSERT INTO currencies VALUES (2, 'EUR');

        INSERT INTO orders VALUES (100, 10, 1, '2024-06-10');
        INSERT INTO orders VALUES (101, 11, 2, '2024-06-10');
        INSERT INTO orders VALUES (102, 12, 1, '2024-06-09');

        INSERT INTO order_items VALUES (1, 100, 'FULFILLED', 2, 50.0, '2024-06-10');
        INSERT INTO order_items VALUES (2, 100, 'CANCELLED', 1, 50.0, '2024-06-10');
        INSERT INTO order_items VALUES (3, 101, 'FULFILLED', 1, 100.0, '2024-06-10');
        INSERT INTO order_items VALUES (4, 102, 'FULFILLED', 1, 75.0, '2024-06-09');

        INSERT INTO refunds VALUES (1, 100, 20.0, '2024-06-10');
        INSERT INTO refunds VALUES (2, 101, 10.0, '2024-06-10');
        INSERT INTO refunds VALUES (3, 102, 5.0, '2024-06-09');
    """)
    conn.commit()
    yield conn
    conn.close()

def run_revenue_report_query(conn: sqlite3.Connection, query: str) -> List[Tuple]:
    """Helper to run the revenue report query and return all results."""
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()

def test_revenue_report_basic(db):
    """
    Test the revenue report query for orders on 2024-06-10.
    Covers: fulfilled/cancelled items, refunds, multiple currencies.
    """
    query = """
    with gross_sales_per_order as (
        select
            order_id,
            sum(quantity * unit_price) as gross_sales
        from order_items
        where status = 'FULFILLED'
        group by order_id
    ),
    refunds_per_order as (
        select
            order_id,
            coalesce(sum(amount), 0) as total_refund
        from refunds
        where created_at = '2024-06-10'
        group by order_id
    )
    select
        o.order_id,
        o.customer_id,
        gs.gross_sales,
        coalesce(r.total_refund, 0) as total_refund,
        c.iso_code as currency
    from orders o
    left join gross_sales_per_order gs on gs.order_id = o.order_id
    left join refunds_per_order r on r.order_id = o.order_id
    left join currencies c on c.currency_id = o.currency_id
    where o.created_at = '2024-06-10'
    order by gs.gross_sales desc;
    """
    results = run_revenue_report_query(db, query)
    expected = [
        (100, 10, 100.0, 20.0, 'USD'),
        (101, 11, 100.0, 10.0, 'EUR'),
    ]
    assert results == expected

# More tests can be added for edge cases: no refunds, only cancelled, etc.
