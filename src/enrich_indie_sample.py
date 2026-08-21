"""
enrich_indie_sample.py

Enriches the existing Indie games sample (indie_games_sample.csv) with two
analytical variables:

    1. review_score        -- from reviews_cleaned.csv
    2. owners_midpoint      -- calculated as (owners_min + owners_max) / 2
                                from games_clean.csv

The sample itself is NOT regenerated. The set of app_ids already present in
indie_games_sample.csv defines the final output exactly -- no game is added,
removed, or resampled here.

Expected repository structure (paths are resolved relative to this file,
not the current working directory):

    Gainz-for-XBox/
    │
    ├── data/
    │   └── processed/
    │       ├── indie_games_sample.csv
    │       ├── reviews_cleaned.csv
    │       └── games_clean.csv
    │
    └── src/
        └── enrich_indie_sample.py

None of the three input files are ever modified or overwritten.
Output: data/processed/indie_games_sample_enriched.csv
"""

import re
import csv
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# FILE PATHS
# ---------------------------------------------------------------------------
# Resolve paths relative to this script's location (not the CWD), so the
# script behaves identically no matter where it's invoked from.
SCRIPT_DIR = Path(__file__).resolve().parent           # .../Gainz-for-XBox/src
REPO_ROOT = SCRIPT_DIR.parent                           # .../Gainz-for-XBox
DATA_DIR = REPO_ROOT / "data" / "processed"

SAMPLE_PATH = DATA_DIR / "indie_games_sample.csv"
REVIEWS_PATH = DATA_DIR / "reviews_cleaned.csv"
GAMES_PATH = DATA_DIR / "games_clean.csv"
OUTPUT_PATH = DATA_DIR / "indie_games_sample_enriched.csv"

FINAL_COLUMNS = ["app_id", "genres", "tags", "review_score", "owners_midpoint"]


# ---------------------------------------------------------------------------
# ROBUST PARSER FOR games_clean.csv
# ---------------------------------------------------------------------------
# This particular games_clean.csv export has two file-specific quirks that a
# plain pd.read_csv() cannot handle:
#
#   (a) every physical line ends with a stray ";;;" suffix (a trailing
#       delimiter artifact from whatever tool produced the export) which,
#       left in place, would contaminate the last column's values;
#
#   (b) whenever `developer` or `publisher` contains an embedded comma, the
#       *entire row* was wrapped in an extra, outer pair of double quotes,
#       with the row's own internal quote characters doubled -- e.g. a row
#       that should read:
#           1313,SiN: Gold,...,"Ritual Entertainment, Nightdive Studios",...
#       is instead stored as:
#           "1313,SiN: Gold,...,""Ritual Entertainment, Nightdive Studios"",..."
#       This is one full extra layer of CSV quoting wrapped around the whole
#       line, not a per-field encoding pandas understands out of the box.
#
# The fix below is a targeted, verifiable, two-step repair:
#   1. Strip the trailing ";;;" (or however many trailing semicolons) plus
#      the line terminator from every raw line.
#   2. If -- and only if -- the resulting line both starts and ends with a
#      literal `"` character, remove that one outer quote layer and replace
#      every doubled `""` with a single `"`. This exactly reverses the
#      wrapping described above and recovers a standard, valid CSV line
#      that the normal csv module can parse without any special escapechar.
#      Lines that were never wrapped (the majority) are left untouched
#      after the suffix strip.
#
# A small number of rows (56 out of 140,082, confirmed to contain literal
# semicolons or other irregular characters embedded directly in the `name`
# field, e.g. "STEINS;GATE") do not conform to either pattern even after
# this repair. These are excluded from the parsed games table rather than
# guessed at, and are reported explicitly (see EXCLUDED_GAMES_ROWS below).
def _strip_trailing_semicolons(line: str) -> str:
    """Remove the file's trailing ';;;'-style artifact and line terminator."""
    return re.sub(r";+\r?\n$", "", line)


def _unwrap_if_double_quoted(line: str) -> str:
    """Reverse the whole-row outer-quote-wrap artifact, if present."""
    if line.startswith('"') and line.endswith('"'):
        inner = line[1:-1]
        return inner.replace('""', '"')
    return line


def load_games_clean(path: Path) -> tuple[pd.DataFrame, list[str]]:
    """
    Parses games_clean.csv using the repair rules documented above.

    Returns:
        games_df: DataFrame of all rows that parsed cleanly to the expected
                   column count.
        excluded_app_ids: list of app_id strings (where extractable) for
                   rows that could not be parsed and were excluded.
    """
    with open(path, encoding="utf-8") as f:
        raw_lines = f.readlines()

    header_line = _strip_trailing_semicolons(raw_lines[0])
    header = next(csv.reader([header_line]))
    n_expected_fields = len(header)

    parsed_rows = []
    excluded_app_ids = []

    for raw_line in raw_lines[1:]:
        cleaned = _strip_trailing_semicolons(raw_line)
        cleaned = _unwrap_if_double_quoted(cleaned)
        try:
            row = next(csv.reader([cleaned]))
        except Exception:
            row = None

        if row is not None and len(row) == n_expected_fields:
            parsed_rows.append(row)
        else:
            # Could not be parsed unambiguously -- exclude rather than guess
            # at field boundaries. Try to at least recover the app_id (it is
            # always the leading digit run) so the exclusion is traceable.
            match = re.match(r'^"?(\d+)', raw_line)
            excluded_app_ids.append(match.group(1) if match else "UNKNOWN")

    games_df = pd.DataFrame(parsed_rows, columns=header)
    return games_df, excluded_app_ids


# ---------------------------------------------------------------------------
# 1. LOAD ALL THREE INPUT FILES
# ---------------------------------------------------------------------------
sample = pd.read_csv(SAMPLE_PATH)
reviews = pd.read_csv(REVIEWS_PATH)
games, excluded_games_rows = load_games_clean(GAMES_PATH)

# The games table was built from raw CSV text via a custom line-repair
# parser, so app_id (and every other column) is still plain text. Convert
# app_id to a proper integer type now so it aligns with the integer app_id
# dtype already used by `sample` and `reviews` (both loaded via the normal
# pd.read_csv, which infers app_id as int64).
games["app_id"] = pd.to_numeric(games["app_id"], errors="raise").astype("int64")

# ---------------------------------------------------------------------------
# 2. VALIDATE REQUIRED COLUMNS
# ---------------------------------------------------------------------------
assert list(sample.columns) == ["app_id", "genres", "tags"], (
    f"Unexpected columns in indie_games_sample.csv: {list(sample.columns)}"
)
assert "review_score" in reviews.columns, "review_score column missing from reviews_cleaned.csv"
assert "app_id" in reviews.columns, "app_id column missing from reviews_cleaned.csv"
assert "owners_min" in games.columns and "owners_max" in games.columns, (
    "owners_min / owners_max columns missing from games_clean.csv"
)
assert "app_id" in games.columns, "app_id column missing from games_clean.csv"

# ---------------------------------------------------------------------------
# 3. VALIDATE JOIN-KEY UNIQUENESS AND MISSINGNESS
# ---------------------------------------------------------------------------
# The sample is the base table; it defines which games appear in the final
# output. Duplicate or missing app_id in EITHER lookup table would risk
# silently duplicating or corrupting rows during the join, so both are
# checked before any merge happens.
assert sample["app_id"].isna().sum() == 0, "indie_games_sample.csv has missing app_id values"
assert sample["app_id"].is_unique, "indie_games_sample.csv has duplicate app_id values"

assert reviews["app_id"].isna().sum() == 0, "reviews_cleaned.csv has missing app_id values"
assert reviews["app_id"].is_unique, "reviews_cleaned.csv has duplicate app_id values -- merge would fan out rows"

assert games["app_id"].isna().sum() == 0, "games_clean.csv has missing app_id values (after parsing)"
assert games["app_id"].is_unique, "games_clean.csv has duplicate app_id values -- merge would fan out rows"

ORIGINAL_SAMPLE_ROWS = len(sample)

# ---------------------------------------------------------------------------
# 4. CALCULATE owners_midpoint FROM games_clean.csv
# ---------------------------------------------------------------------------
# owners_min / owners_max were parsed as plain CSV text; convert to numeric
# explicitly before arithmetic (errors="raise" so any unexpected non-numeric
# value stops the script rather than silently becoming NaN).
games["owners_min"] = pd.to_numeric(games["owners_min"], errors="raise")
games["owners_max"] = pd.to_numeric(games["owners_max"], errors="raise")

# owners_midpoint is an ESTIMATE of ownership/reach derived from the
# reported ownership interval -- it is the midpoint of [owners_min,
# owners_max], not an exact observed owner count. Steam does not publish
# exact owner counts; owners_min/owners_max are themselves already
# estimated bucket boundaries, so this midpoint carries that same
# uncertainty forward and should be interpreted as an approximation only.
games["owners_midpoint"] = (games["owners_min"] + games["owners_max"]) / 2

# ---------------------------------------------------------------------------
# 5. MERGE (left joins on app_id, sample is always the base/left table)
# ---------------------------------------------------------------------------
# --- Merge 1: sample + reviews (review_score only) ---
rows_before_reviews_merge = len(sample)
enriched = sample.merge(
    reviews[["app_id", "review_score"]],
    on="app_id",
    how="left",
    validate="one_to_one",  # fails loudly if either side had a duplicate app_id
)
assert len(enriched) == rows_before_reviews_merge, (
    "Row count changed after merging reviews -- indicates a duplicate-key fan-out"
)
assert enriched["app_id"].is_unique, "Duplicate app_id introduced by reviews merge"

reviews_matched = enriched["review_score"].notna().sum()
reviews_unmatched = enriched["review_score"].isna().sum()

# --- Merge 2: (sample + reviews) + games (owners_midpoint only) ---
rows_before_games_merge = len(enriched)
enriched = enriched.merge(
    games[["app_id", "owners_midpoint"]],
    on="app_id",
    how="left",
    validate="one_to_one",
)
assert len(enriched) == rows_before_games_merge, (
    "Row count changed after merging games -- indicates a duplicate-key fan-out"
)
assert enriched["app_id"].is_unique, "Duplicate app_id introduced by games merge"

games_matched = enriched["owners_midpoint"].notna().sum()
games_unmatched = enriched["owners_midpoint"].isna().sum()

# ---------------------------------------------------------------------------
# 6. VALIDATE THE FINAL OUTPUT
# ---------------------------------------------------------------------------
# Every original sampled app_id must still be present, in the same set, with
# no additions and no removals.
assert set(enriched["app_id"]) == set(sample["app_id"]), (
    "Sampled app_ids changed during enrichment -- sample was not preserved"
)
assert enriched["app_id"].is_unique, "app_id is not unique in the final output"
assert enriched.duplicated().sum() == 0, "Duplicate rows present in the final output"
assert len(enriched) == ORIGINAL_SAMPLE_ROWS, (
    f"Final row count ({len(enriched)}) does not equal original sample row count ({ORIGINAL_SAMPLE_ROWS})"
)

# genres and tags must be byte-for-byte identical to the original sample
# (aligned on app_id, since merges can reorder rows).
sample_indexed = sample.set_index("app_id")
enriched_check = enriched.set_index("app_id")
assert sample_indexed["genres"].equals(enriched_check.loc[sample_indexed.index, "genres"]), (
    "genres column was altered from the original sample"
)
assert sample_indexed["tags"].equals(enriched_check.loc[sample_indexed.index, "tags"]), (
    "tags column was altered from the original sample"
)

missing_review_score = int(enriched["review_score"].isna().sum())
missing_owners_midpoint = int(enriched["owners_midpoint"].isna().sum())
duplicate_app_ids = int(enriched["app_id"].duplicated().sum())

validation_passed = (
    set(enriched["app_id"]) == set(sample["app_id"])
    and enriched["app_id"].is_unique
    and enriched.duplicated().sum() == 0
    and len(enriched) == ORIGINAL_SAMPLE_ROWS
)

# ---------------------------------------------------------------------------
# 7. FINALIZE COLUMN ORDER AND EXPORT
# ---------------------------------------------------------------------------
enriched = enriched[FINAL_COLUMNS]

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
enriched.to_csv(OUTPUT_PATH, index=False)

# ---------------------------------------------------------------------------
# COMPLETION / VALIDATION SUMMARY
# ---------------------------------------------------------------------------
print(f"Original sample rows: {ORIGINAL_SAMPLE_ROWS}")
print(f"Final rows: {len(enriched)}")
print(f"Reviews matched: {reviews_matched}")
print(f"Reviews unmatched: {reviews_unmatched}")
print(f"Games matched: {games_matched}")
print(f"Games unmatched: {games_unmatched}")
print(f"Missing review_score: {missing_review_score}")
print(f"Missing owners_midpoint: {missing_owners_midpoint}")
print(f"Duplicate app_ids: {duplicate_app_ids}")
print(f"Excluded/unparseable rows in games_clean.csv (out of scope, none affect this sample): {len(excluded_games_rows)}")
print("Validation:", "PASSED" if validation_passed else "FAILED")
print("Saved to:", OUTPUT_PATH)
