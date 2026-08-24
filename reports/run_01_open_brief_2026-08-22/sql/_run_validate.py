#!/usr/bin/env python3
"""Runs 06_validate.sql statement-by-statement so every SELECT's output is
printed (the generic _run_sql.py runner only surfaces the last statement's
result). Validation-only plumbing; all check logic lives in the .sql file."""
import sys
import duckdb

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'sql/06_validate.sql'
    with open(path) as f:
        raw = f.read()
    # strip full-line comments before splitting, so a comment block followed
    # by a real statement in the same ';'-delimited chunk isn't discarded
    lines = [ln for ln in raw.splitlines() if not ln.strip().startswith('--')]
    script = '\n'.join(lines)
    statements = [s.strip() for s in script.split(';') if s.strip()]
    con = duckdb.connect()
    for stmt in statements:
        con.execute(stmt)
        try:
            df = con.fetchdf()
            if len(df):
                print(df.to_string(index=False))
                print()
        except Exception:
            pass

if __name__ == "__main__":
    main()
