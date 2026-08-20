"""Extract review_score and total (review count) from reviews.csv and bucket total.

Buckets follow a 1-2-5 log scale, same style as the owners_range buckets:
0-10, 10-50, 50-100, 100-500, 500-1,000, 1,000-5,000, ... with a final
open-ended bucket for anything above the last edge.
"""
import argparse
import csv
from pathlib import Path

SRC = Path("data/raw/super raw/reviews.csv")
DST = Path("data/processed/review_amount_buckets.csv")

BUCKET_EDGES = [0, 10, 50, 100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000]


def bucket_for(total: int):
    """Return (bucket_number, label) for a total review count."""
    for i in range(len(BUCKET_EDGES) - 1):
        low, high = BUCKET_EDGES[i], BUCKET_EDGES[i + 1]
        if low <= total < high:
            return i + 1, f"{low:,} - {high:,}"
    low = BUCKET_EDGES[-1]
    return len(BUCKET_EDGES), f"{low:,}+"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", type=Path, default=SRC)
    parser.add_argument("--dst", type=Path, default=DST)
    args = parser.parse_args()

    rows = []
    skipped = 0
    with args.src.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            app_id = row.get("app_id", "")
            score = row.get("review_score")
            total = row.get("total")
            if total is None or not total.strip().isdigit():
                skipped += 1
                continue
            total = int(total.strip())
            bucket_num, bucket_label = bucket_for(total)
            rows.append(
                {
                    "app_id": app_id,
                    "review_score": score.strip() if score else "",
                    "total": total,
                    "total_bucket": bucket_num,
                    "total_bucket_range": bucket_label,
                }
            )

    args.dst.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["app_id", "review_score", "total", "total_bucket", "total_bucket_range"]
    with args.dst.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.dst} ({skipped} rows skipped for missing/malformed total).")
    print("Total buckets (number: range):")
    for i in range(len(BUCKET_EDGES) - 1):
        print(f"  {i + 1}: {BUCKET_EDGES[i]:,} - {BUCKET_EDGES[i + 1]:,}")
    print(f"  {len(BUCKET_EDGES)}: {BUCKET_EDGES[-1]:,}+")


if __name__ == "__main__":
    main()
