#!/usr/bin/env python3
"""Generic runner: executes a .sql file (may contain multiple ; separated
statements) against DuckDB. Not itself a transformation -- the transformation
logic lives entirely in the .sql files under sql/. Usage:

    python3 sql/_run_sql.py sql/01_stage_games.sql
"""
import sys
import duckdb

def main():
    if len(sys.argv) != 2:
        print("usage: _run_sql.py <script.sql>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    with open(path) as f:
        script = f.read()
    con = duckdb.connect()
    con.execute(script)
    try:
        rows = con.fetchall()
        if rows:
            cols = [d[0] for d in con.description] if con.description else []
            if cols:
                print(" | ".join(cols))
            for r in rows:
                print(r)
    except Exception:
        pass
    print(f"OK: {path}")

if __name__ == "__main__":
    main()
