import os

import psycopg2
import pytest

from enhanced_de_prompt_engineering.utils.benchmark import (
    parse_explain_output,
    run_explain_analyze,
)

POSTGRES_DSN = os.getenv(
    "POSTGRES_TEST_DSN",
    "dbname=de_test user=de_test password=de_test host=localhost port=5432"
)

@pytest.fixture(scope="module")
def pg_conn():
    """Set up a PostgreSQL connection for testing benchmarking utils."""
    conn = psycopg2.connect(POSTGRES_DSN)
    yield conn
    conn.close()

def test_run_explain_analyze_and_parse(pg_conn):
    """
    Test that run_explain_analyze and parse_explain_output work on a real table query.
    Only require execution_time_ms; buffer metrics are optional for small queries.
    """
    query = "SELECT * FROM orders LIMIT 1;"
    output = run_explain_analyze(pg_conn, query)
    metrics = parse_explain_output(output)
    assert 'execution_time_ms' in metrics
    # Buffer metrics may not be present for trivial queries; check if present
    if 'shared_read_blocks' in metrics:
        assert isinstance(metrics['shared_read_blocks'], int)
    if 'shared_hit_blocks' in metrics:
        assert isinstance(metrics['shared_hit_blocks'], int)
