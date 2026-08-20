"""Extract owners_range and price from steamspy_insights.csv.

owners_range comes from SteamSpy already pre-bucketed, as a string like
"1,000,000 .. 2,000,000". This just cleans up the formatting to
"1,000,000 - 2,000,000".
"""
import argparse
import csv
from pathlib import Path

SRC = Path("data/raw/super raw/steamspy_insights.csv")
DST = Path("data/processed/owners_price_buckets.csv")


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
            raw_range = row.get("owners_range", "").strip()
            raw_price = row.get("price", "").strip()
            if ".." not in raw_range:
                skipped += 1
                continue
            owners_range = raw_range.replace("..", "-")
            owners_range = " ".join(owners_range.split())
            has_price = raw_price.isdigit()
            rows.append(
                {
                    "app_id": row.get("app_id", ""),
                    "owners_range": owners_range,
                    "price_cents": int(raw_price) if has_price else "",
                    "price_usd": round(int(raw_price) / 100, 2) if has_price else "",
                }
            )

    args.dst.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["app_id", "owners_range", "price_cents", "price_usd"]
    with args.dst.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    missing_price = sum(1 for r in rows if r["price_usd"] == "")
    print(
        f"Wrote {len(rows)} rows to {args.dst} "
        f"({skipped} rows skipped for malformed owners_range, "
        f"{missing_price} rows have missing price)."
    )


if __name__ == "__main__":
    main()
