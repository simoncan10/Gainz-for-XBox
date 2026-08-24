"""
Stage 1 (data-profiler) for the two large raw files.

Streams descriptions.csv and promotional.csv without loading them into memory,
and measures the one thing that decides whether they are worth using at all:
how much of the existing scored dataset they actually cover.

Writes a small profile (JSON + Markdown) into data/processed/ so it can be
reviewed without moving the gigabyte of source data anywhere.

Run from the repo root:
    python profile_bigfiles.py
"""

import csv, json, os, sys
from collections import Counter

# Descriptions can be tens of KB in a single field; the default limit is 128 KB
# but on some Windows builds sys.maxsize overflows the C long, so step down.
limit = sys.maxsize
while True:
    try:
        csv.field_size_limit(limit)
        break
    except OverflowError:
        limit = int(limit / 10)

RAW = os.path.join("data", "raw", "super raw")
PROC = os.path.join("data", "processed")
TARGETS = ["descriptions.csv", "promotional.csv"]
REFERENCE = os.path.join(PROC, "pipeline_dataset.csv")


def load_reference_ids(path):
    """app_ids already in the scored pipeline — the population we care about."""
    ids = set()
    if not os.path.exists(path):
        print(f"  ! reference not found: {path}")
        return ids
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        r = csv.DictReader(f, escapechar="\\")
        key = next((c for c in (r.fieldnames or []) if c.lower() in ("app_id", "appid")), None)
        if not key:
            print(f"  ! no app_id column in {path}: {r.fieldnames}")
            return ids
        for row in r:
            v = (row.get(key) or "").strip()
            if v:
                ids.add(v)
    return ids


def profile(path, ref_ids):
    name = os.path.basename(path)
    size = os.path.getsize(path)
    print(f"\n=== {name}  ({size/1e6:.1f} MB) ===")

    rows = 0
    ids = set()
    dupes = 0
    # per-column: non-empty count, total text length, max length
    nonempty, total_len, max_len = Counter(), Counter(), Counter()
    samples = {}

    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        # escapechar per the games.csv gotcha documented in the README —
        # these exports use backslash-escaped quotes, not doubled quotes.
        r = csv.DictReader(f, escapechar="\\")
        cols = r.fieldnames or []
        idcol = next((c for c in cols if c.lower() in ("app_id", "appid")), None)

        for row in r:
            rows += 1
            if idcol:
                v = (row.get(idcol) or "").strip()
                if v:
                    if v in ids:
                        dupes += 1
                    ids.add(v)
            for c in cols:
                val = row.get(c) or ""
                n = len(val.strip())
                if n:
                    nonempty[c] += 1
                    total_len[c] += n
                    if n > max_len[c]:
                        max_len[c] = n
                    # keep one short-ish example per column to show what it holds
                    if c not in samples and 20 < n < 240:
                        samples[c] = val.strip().replace("\n", " ")
            if rows % 25000 == 0:
                print(f"  ...{rows:,} rows", end="\r")

    matched = len(ids & ref_ids) if ref_ids else 0
    cov_of_ref = 100.0 * matched / len(ref_ids) if ref_ids else 0.0
    cov_of_self = 100.0 * matched / len(ids) if ids else 0.0

    prof = {
        "file": name,
        "bytes": size,
        "rows": rows,
        "columns": [
            {
                "name": c,
                "nonempty": nonempty[c],
                "null_rate": round(100.0 * (rows - nonempty[c]) / rows, 2) if rows else None,
                "avg_len": round(total_len[c] / nonempty[c], 1) if nonempty[c] else 0,
                "max_len": max_len[c],
                "sample": samples.get(c, "")[:200],
            }
            for c in (r.fieldnames or [])
        ],
        "id_column": idcol,
        "distinct_ids": len(ids),
        "duplicate_id_rows": dupes,
        "matched_reference_ids": matched,
        "pct_of_reference_covered": round(cov_of_ref, 2),
        "pct_of_own_ids_in_reference": round(cov_of_self, 2),
    }

    print(f"  rows={rows:,}  distinct_ids={len(ids):,}  dupes={dupes:,}")
    print(f"  covers {cov_of_ref:.1f}% of the {len(ref_ids):,} scored app_ids")
    return prof


def main():
    if not os.path.isdir(RAW):
        sys.exit(f"Run this from the repo root — {RAW} not found.")

    print(f"Reading reference ids from {REFERENCE} ...")
    ref = load_reference_ids(REFERENCE)
    print(f"  {len(ref):,} app_ids in the scored pipeline")

    out = {"reference_ids": len(ref), "files": []}
    for t in TARGETS:
        p = os.path.join(RAW, t)
        if os.path.exists(p):
            out["files"].append(profile(p, ref))
        else:
            print(f"  ! missing: {p}")

    os.makedirs(PROC, exist_ok=True)
    jpath = os.path.join(PROC, "profile_bigfiles.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    mpath = os.path.join(PROC, "profile_bigfiles.md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write("# Profile — descriptions.csv / promotional.csv\n\n")
        f.write(f"Reference population: **{out['reference_ids']:,}** scored app_ids "
                f"(`pipeline_dataset.csv`)\n\n")
        for fp in out["files"]:
            f.write(f"## {fp['file']}\n\n")
            f.write(f"- {fp['bytes']/1e6:.1f} MB, {fp['rows']:,} rows, "
                    f"{fp['distinct_ids']:,} distinct ids, {fp['duplicate_id_rows']:,} duplicate-id rows\n")
            f.write(f"- **Covers {fp['pct_of_reference_covered']}% of the scored population**; "
                    f"{fp['pct_of_own_ids_in_reference']}% of its own ids are in that population\n\n")
            f.write("| column | null % | avg len | max len | sample |\n|---|---|---|---|---|\n")
            for c in fp["columns"]:
                s = c["sample"].replace("|", "\\|")[:110]
                f.write(f"| `{c['name']}` | {c['null_rate']} | {c['avg_len']} | {c['max_len']} | {s} |\n")
            f.write("\n")

    print(f"\nWrote:\n  {jpath}\n  {mpath}")


if __name__ == "__main__":
    main()
