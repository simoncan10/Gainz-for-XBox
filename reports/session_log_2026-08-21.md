# Session Log — 2026-08-21

Ongoing prompt-by-prompt record for documentation and recreatability, per standing
instruction to log every exchange (prompt + actions) from now on. See
[session_log_2026-08-20.md](session_log_2026-08-20.md) for the prior session that
built the base pipeline.

## Prompt-by-prompt log

1. **Prompt:** "Keep this as a must do. For the following, always document in a note
   of what we were discussing and what you were doing. So write down the prompt and
   your actions. My next demand would be, I need you to use the four scripts to
   create a clean dataset mentioning that we have one additional new script now,
   called find underscore indie, which was made by a classmate of mine, and we need
   to use all four of this now to create the full new dataset. Please save it in
   processed data."

   **Action:**
   - Located the classmate's new script at `src/find_indie` (no `.py` extension,
     module docstring names it `find_indie_games.py`). It cross-references
     `data/processed/tags_one_row_per_app.csv` and a one-hot genres file to flag
     every `app_id` where "Indie" appears in tags and/or genres, writing
     `indie_games.csv` / `.xlsx`.
   - Found two blockers and fixed them:
     - `openpyxl` wasn't installed (needed for the script's `.xlsx` output) — installed it.
     - The script pointed at `data/processed/onehot/genres_onehot.csv`, but the real
       file lives at `data/processed/genres_onehot.csv` (the `onehot/` folder only
       had a stray placeholder). Fixed the `GENRES_PATH` constant in
       `src/find_indie` to point at the correct location.
   - Updated `src/combine_datasets.py` to also load `indie_games.csv` and add an
     `is_indie` boolean column (True if the app_id appears in the indie script's
     output), alongside the existing owners/price/review join.
   - Ran all four scripts in order:
     `extract_owners_price.py` → `extract_reviews.py` → `find_indie` →
     `combine_datasets.py`.
   - Result: `data/processed/combined.csv` now has 140,067 rows with columns
     `app_id, owners_range, price_cents, review_score, total_bucket_range, is_indie`
     (89,638 rows flagged indie). Also produced `data/processed/indie_games.csv`
     and `.xlsx` (89,648 rows) as a byproduct of running `find_indie`.

## Pipeline (updated)

| Order | Script | Input | Output |
|---|---|---|---|
| 1 | `src/extract_owners_price.py` | `data/raw/super raw/steamspy_insights.csv` | `data/processed/owners_price_buckets.csv` |
| 2 | `src/extract_reviews.py` | `data/raw/super raw/reviews.csv` | `data/processed/review_amount_buckets.csv` |
| 3 | `src/find_indie` (classmate's script) | `data/processed/tags_one_row_per_app.csv`, `data/processed/genres_onehot.csv` | `data/processed/indie_games.csv`, `.xlsx` |
| 4 | `src/combine_datasets.py` | outputs of 1, 2, 3 | `data/processed/combined.csv` |

To recreate `combined.csv` from scratch, run in that order from the repo root:

```
python src/extract_owners_price.py
python src/extract_reviews.py
python src/find_indie
python src/combine_datasets.py
```

Requires `pandas` and `openpyxl` installed (used by `find_indie`).
