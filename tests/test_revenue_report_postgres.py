from decimal import Decimal
from typing import Any, List, Tuple

# Use shared pg_conn fixture from conftest.py

def convert_decimals(row: Tuple[Any, ...]) -> Tuple[Any, ...]:
    """Convert Decimal values in a tuple to float for comparison."""
    return tuple(float(x) if isinstance(x, Decimal) else x for x in row)

def run_revenue_report_query_pg(conn, query: str) -> List[Tuple]:
    """Helper to run the revenue report query and return all results."""
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()

def create_indexes(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_order_items_fulfilled
            ON order_items (order_id, created_at)
            WHERE status = 'FULFILLED';
        CREATE INDEX IF NOT EXISTS idx_refunds_recent
            ON refunds (order_id, created_at)
            WHERE created_at = '2024-06-10';
        CREATE INDEX IF NOT EXISTS idx_orders_created_at
            ON orders (created_at);
    """)
    conn.commit()

def drop_indexes(conn):
    cur = conn.cursor()
    cur.execute("""
        DROP INDEX IF EXISTS idx_order_items_fulfilled;
        DROP INDEX IF EXISTS idx_refunds_recent;
        DROP INDEX IF EXISTS idx_orders_created_at;
    """)
    conn.commit()

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

def test_revenue_report_no_indexes(pg_conn):
    """
    Test the revenue report query with no indexes (simulate cold start).
    """
    drop_indexes(pg_conn)
    with open("enhanced_de_prompt_engineering/queries/revenue_report.sql") as f:
        query = f.read()
    results = run_revenue_report_query_pg(pg_conn, query)
    results = [convert_decimals(row) for row in results]
    expected = [
        (100, 10, 100.0, 20.0, 'USD'),
        (101, 11, 100.0, 10.0, 'EUR'),
    ]
    assert results == expected

def test_revenue_report_with_indexes(pg_conn):
    """
    Test the revenue report query with recommended indexes.
    """
    create_indexes(pg_conn)
    with open("enhanced_de_prompt_engineering/queries/revenue_report.sql") as f:
        query = f.read()
    results = run_revenue_report_query_pg(pg_conn, query)
    results = [convert_decimals(row) for row in results]
    expected = [
        (100, 10, 100.0, 20.0, 'USD'),
        (101, 11, 100.0, 10.0, 'EUR'),
    ]
    assert results == expected
