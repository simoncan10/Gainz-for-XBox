"""End-to-end pipeline: recreates the full master dataset from data/raw every time.

Runs extract_owners_price.py and extract_reviews.py, and builds genres/tags
directly from the raw long-format files (genres.csv, tags.csv) rather than any
processed/intermediate file - so the whole thing is reproducible from data/raw
alone, with no dependency on files that don't have a script to regenerate them.
"Indie" shows up naturally as one value/column among each app's genres/tags where
it applies, rather than as a separate lookup.

Tags are one-hot encoded (one 0/1 column per distinct tag) since there are ~450 of
them - too many values to read comfortably as a single joined string. Those columns
are appended at the end of the row so the readable columns come first.

Output columns:
    app_id, genres, price_cents, review_score, total, owners_range, <one column per tag>
"""
import csv
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw" / "super raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

GENRES_SRC = DATA_RAW / "genres.csv"
TAGS_SRC = DATA_RAW / "tags.csv"
OWNERS_PRICE_SRC = DATA_PROCESSED / "owners_price_buckets.csv"
REVIEWS_SRC = DATA_PROCESSED / "review_amount_buckets.csv"
DST = DATA_PROCESSED / "pipeline_dataset.csv"

STEPS = ["extract_owners_price.py", "extract_reviews.py"]


def run_step(script_name):
    print(f"--- running {script_name} ---")
    subprocess.run([sys.executable, str(SRC_DIR / script_name)], check=True, cwd=PROJECT_ROOT)


def load_genres(path):
    """Group the raw (app_id, genre) long-format file into {app_id: 'g1, g2, ...'}."""
    genres_by_app = defaultdict(list)
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            app_id = row.get("app_id")
            genre = row.get("genre")
            if app_id and genre:
                genres_by_app[app_id].append(genre)
    return {app_id: ", ".join(values) for app_id, values in genres_by_app.items()}


def load_tags(path):
    """Return (tag_columns, {app_id: set(tags)}) from the raw (app_id, tag) file."""
    tags_by_app = defaultdict(set)
    all_tags = set()
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            app_id = row.get("app_id")
            tag = row.get("tag")
            if app_id and tag:
                tags_by_app[app_id].add(tag)
                all_tags.add(tag)
    return sorted(all_tags), tags_by_app


def main():
    for step in STEPS:
        run_step(step)

    genres_by_app = load_genres(GENRES_SRC)
    tag_columns, tags_by_app = load_tags(TAGS_SRC)

    with REVIEWS_SRC.open(encoding="utf-8") as f:
        reviews_by_app = {row["app_id"]: row for row in csv.DictReader(f)}

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    fieldnames = ["app_id", "genres", "price_cents", "review_score", "total", "owners_range"] + tag_columns

    written = 0
    skipped = 0
    with OWNERS_PRICE_SRC.open(encoding="utf-8") as f, DST.open("w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(fieldnames)
        for row in csv.DictReader(f):
            app_id = row["app_id"]
            review_row = reviews_by_app.get(app_id)
            if review_row is None:
                skipped += 1
                continue
            app_tags = tags_by_app.get(app_id, ())
            writer.writerow(
                [
                    app_id,
                    genres_by_app.get(app_id, ""),
                    row["price_cents"],
                    review_row["review_score"],
                    review_row["total"],
                    row["owners_range"],
                ]
                + [1 if tag in app_tags else 0 for tag in tag_columns]
            )
            written += 1

    print(f"\nWrote {written} rows to {DST} ({skipped} app_ids skipped, no matching review row).")
    print(f"One-hot tag columns: {len(tag_columns)}")


if __name__ == "__main__":
    main()
