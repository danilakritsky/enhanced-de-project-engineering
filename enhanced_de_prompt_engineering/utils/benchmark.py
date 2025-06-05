from typing import Dict

import psycopg2


def run_explain_analyze(conn: psycopg2.extensions.connection, query: str) -> str:
    """
    Run EXPLAIN (ANALYZE, BUFFERS) on the given query and return the output as a string.
    """
    cur = conn.cursor()
    cur.execute(f"EXPLAIN (ANALYZE, BUFFERS) {query}")
    rows = cur.fetchall()
    return "\n".join(row[0] for row in rows)


def parse_explain_output(output: str) -> Dict[str, float]:
    """
    Parse EXPLAIN ANALYZE output for key metrics (execution time, shared read/hit blocks).
    Returns a dictionary of metrics.
    """
    metrics = {}
    for line in output.splitlines():
        if 'Execution Time' in line:
            metrics['execution_time_ms'] = float(line.split(':')[1].strip().split()[0])
        if 'Shared Read Blocks' in line:
            metrics['shared_read_blocks'] = int(line.split(':')[1].strip())
        if 'Shared Hit Blocks' in line:
            metrics['shared_hit_blocks'] = int(line.split(':')[1].strip())
    return metrics
