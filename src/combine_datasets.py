"""Combine owners/price buckets and review amount buckets into one CSV, joined on app_id."""
import argparse
import csv
from pathlib import Path

OWNERS_PRICE_SRC = Path("data/processed/owners_price_buckets.csv")
REVIEWS_SRC = Path("data/processed/review_amount_buckets.csv")
DST = Path("data/processed/combined.csv")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owners-price-src", type=Path, default=OWNERS_PRICE_SRC)
    parser.add_argument("--reviews-src", type=Path, default=REVIEWS_SRC)
    parser.add_argument("--dst", type=Path, default=DST)
    args = parser.parse_args()

    with args.reviews_src.open(encoding="utf-8") as f:
        reviews_by_app = {row["app_id"]: row for row in csv.DictReader(f)}

    rows = []
    unmatched = 0
    with args.owners_price_src.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            review_row = reviews_by_app.get(row["app_id"])
            if review_row is None:
                unmatched += 1
                continue
            rows.append(
                {
                    "app_id": row["app_id"],
                    "owners_range": row["owners_range"],
                    "price_cents": row["price_cents"],
                    "review_score": review_row["review_score"],
                    "total_bucket_range": review_row["total_bucket_range"],
                }
            )

    args.dst.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "app_id",
        "owners_range",
        "price_cents",
        "review_score",
        "total_bucket_range",
    ]
    with args.dst.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.dst} ({unmatched} app_ids had no matching reviews row).")


if __name__ == "__main__":
    main()
