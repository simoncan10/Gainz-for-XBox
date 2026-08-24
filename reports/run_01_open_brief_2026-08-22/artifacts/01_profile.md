# Stage 1 — Data Profile

Steam catalogue snapshot, ~140k apps, dated approximately December 2024. Six raw CSVs profiled; all queries run via DuckDB 1.5.5 against the files directly (no file loaded into memory or context).

## App universe

**games.csv is the canonical app table.** `app_id` is a true, verified primary key: 140,082 rows, 140,082 distinct `app_id` values, zero full-row duplicates. Every other file's `app_id` values are a subset of games.csv's (0 orphans found in either direction) — games.csv is the safe base table to build any downstream join against.

## File inventory

| File | Bytes | Rows | Encoding |
|---|---|---|---|
| categories.csv | 14,307,957 | 522,582 | utf-8 |
| games.csv | 33,633,019 | 140,082 | utf-8 |
| genres.csv | 6,986,851 | 353,339 | utf-8 |
| reviews.csv | 14,104,049 | 140,082 | utf-8 |
| steamspy_insights.csv | 18,172,366 | 140,077 | us-ascii |
| tags.csv | 38,195,484 | 1,744,632 | us-ascii |

## Primary keys

| File | Key | Unique? | Evidence |
|---|---|---|---|
| games.csv | app_id | Yes | count = distinct = 140,082 |
| reviews.csv | app_id | Yes | count = distinct = 140,082 |
| steamspy_insights.csv | app_id | Yes | count = distinct = 140,077 |
| categories.csv | (app_id, category) | Yes | 0 duplicate pairs; app_id alone is NOT unique (3.9 rows/app avg) |
| genres.csv | (app_id, genre) | Yes | 0 duplicate pairs; app_id alone NOT unique (2.9 rows/app avg) |
| tags.csv | (app_id, tag) | Yes | 0 duplicate pairs; app_id alone NOT unique (14.8 rows/app avg) |

## Join coverage against games.csv (140,082 apps) — the decision-relevant numbers

| Table | Games matched | Coverage | Reverse coverage (table→games) |
|---|---|---|---|
| categories.csv | 134,393 | **95.94%** | 100.00% |
| genres.csv | 122,458 | **87.42%** | 100.00% |
| tags.csv | 117,505 | **83.88%** | 100.00% |
| reviews.csv | 140,082 | **100.00%** | 100.00% |
| steamspy_insights.csv | 140,077 | **99.996%** | 100.00% |

No table contains an `app_id` absent from games.csv. The only real gaps are on the games→{categories,genres,tags} side: an inner join to tags.csv alone drops 16.12% of the catalogue (22,577 apps), to genres.csv drops 12.58% (17,624 apps), to categories.csv drops 4.06% (5,689 apps). A downstream segment analysis that inner-joins on genre or tag must explicitly account for this shrinkage or state it as a caveat.

## Date coverage (games.csv `release_date`)

- Castable to a real date: 111,564 of 140,082 rows (79.6%). The remaining 28,518 rows (20.4%) hold the literal string `\N` — no date at all, not a parse failure.
- Range: **1997-06-30 to 2024-10-28**.
- 2024 is right-truncated: monthly counts run Jan (1,773) through Oct (2,502) and then **zero** in November and December, despite the snapshot being dated ~December 2024. The 22,022 releases attributed to "2024" is a 10-month total, not a full year — comparing it to 2023's full-year 18,217 as if both were complete years will read as a bigger 2024 boom than actually happened, or mask a real slowdown, depending which way the true Nov–Dec count would have gone.
- Per-year counts (full table in `01_profile.json`): rows are negligible before 2006, then grow roughly monotonically to a peak of 18,217 in 2023.

## Hazards, ranked by how much damage they can do to a downstream claim

1. **Backslash-escaped JSON/HTML breaks naive CSV parsing — confirmed and quantified.** `games.csv.price_overview` and `reviews.csv.reviews` embed `\"` (backslash-escaped quotes), not doubled CSV quotes. Reproduced directly: Python's `csv.reader` with no `escapechar` misaligns 76,334 of 140,082 games.csv rows (**54.49%**, not the ~13% suggested by prior sniffing — the real number is over half the file). Reading `type` positionally after misalignment collapses the correct game count from 122,191 to 45,857 — a **62% loss**, which silently drops named indie titles from any `type=='game'` filter. **DuckDB's own `read_csv_auto` sniffer already detects `escape='\'` correctly with zero configuration** — verified by running the naive-detect and explicit-`escape='\'` reads side by side and confirming identical row counts (140,082) and identical type distributions (122,191 game / 17,891 demo). The hazard is real for pandas/plain-Python pipelines; it is not a hazard for DuckDB's default reader. The same escaping pattern reappears in reviews.csv's free-text `reviews` column and will raise a strict-mode CSV error if `escape` is pinned to anything other than backslash or auto-detect.

2. **steamspy_insights.csv's playtime columns are entirely dead.** `playtime_average_forever`, `playtime_average_2weeks`, `playtime_median_forever`, `playtime_median_2weeks` are the constant `0` for all 140,077 rows — zero variance, not just high null rate. Since Game Pass is a subscription business where engagement/playtime is the metric that matters most, this dataset supplies **no usable playtime signal at all**, from any file. This should shape what the downstream analysis is allowed to claim about engagement.

3. **`\N` as a null sentinel defeats default typing and conflicts with the escape fix.** The literal 2-character string `\N` marks missing values in games.csv (`release_date`, `price_overview`, `languages`, 20 rows of `name`), reviews.csv (10 of 13 columns), and steamspy_insights.csv (`developer`, `publisher`, `price`, `initial_price`, `discount`). DuckDB refuses to combine `nullstr='\N'` with `escape='\'` in one `read_csv` call (Binder Error) — the fix has to be `NULLIF(col,'\N')` + `CAST` applied after reading, not at read time, file by file.

4. **Pricing coverage on games.csv is materially incomplete.** 63,748 of 140,082 rows (45.5%) have no `price_overview` at all; critically, 30,089 of the 106,421 rows flagged `is_free=0` (paid) — 28.3% of nominally-paid titles — also lack captured price data. Any price-based segmentation built only from `price_overview` silently excludes over a quarter of paid titles.

5. **Sparse columns in reviews.csv give false confidence.** `metacritic_score` is populated for only 3.4% of apps, `recommendations` for 12.3%, and `steamspy_score_rank` for essentially none (0.04%, 51 rows). These are fine for spot-checking specific AAA titles but cannot support catalogue-wide claims.

6. **owners_range in steamspy_insights.csv has almost no resolution where it matters.** 83.2% of all 140,077 apps fall in the single lowest bucket (`0 .. 20,000` owners) — it cannot distinguish a niche title from a modest mid-size hit, only separate the long tail from actual hits.

7. **developer/publisher missing for ~35% of apps** in steamspy_insights.csv — any studio- or publisher-level rollup understates its true population by roughly a third unless backfilled.

8. **Long-table fan-out risk.** Joining games.csv to tags.csv, genres.csv, or categories.csv on `app_id` alone multiplies rows 14.8x, 2.9x, and 3.9x respectively (verified: 1,744,632 / 117,505 ≈ 14.85 for tags). Any aggregate computed after such a join without first deduplicating or pre-aggregating the long side will overcount.

## Files produced

- `/home/claude/run_2026-08-22/artifacts/01_profile.json` — full machine-readable profile (schemas, per-column null/distinct/min/max, primary keys, join coverage, ranked hazards)
- `/home/claude/run_2026-08-22/artifacts/01_profile.md` — this document
