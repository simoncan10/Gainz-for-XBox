# Stage 2 — Cleaning report

Built from `artifacts/01_profile.json`. All transformations are in `sql/01_*.sql` .. `sql/06_validate.sql`, run via `python3 sql/_run_sql.py <script>` (a thin executor; all logic lives in the SQL). Every script re-reads either the raw CSVs (staging scripts) or the Parquet already produced (build/validate scripts) — never a CSV touched twice. Re-running the full pipeline from scratch twice produces byte-identical Parquet files (verified via md5sum on every output file).

## Canonical tables produced

| Table | Grain | Rows | File |
|---|---|---|---|
| `fact_games` | one row per `app_id` (the games.csv universe: games **and** demos) | 140,082 | `parquet/fact_games.parquet` |
| `categories_long` | one row per (app_id, category) | 522,582 | `parquet/categories_long.parquet` |
| `genres_long` | one row per (app_id, genre) | 353,339 | `parquet/genres_long.parquet` |
| `tags_long` | one row per (app_id, tag) | 1,744,632 | `parquet/tags_long.parquet` |
| `games_stage`, `reviews_stage`, `steamspy_stage` | one row per app_id | 140,082 / 140,082 / 140,077 | intermediate staging, kept for audit |

`fact_games` is built with LEFT JOINs from `games_stage` (the verified 1:1 primary-key table) against `reviews_stage`, `steamspy_stage`, and pre-aggregated summaries of the three long tables. No row from games.csv was ever dropped by a join.

## Rules applied, in execution order

1. **`01_stage_games.sql`** — read games.csv with DuckDB's default reader (correctly auto-detects `escape='\'`), `NULLIF(...,'\N')` + `TRY_CAST` on every sentinel-bearing column, `price_overview` JSON parsed into `price_currency` / `price_final_cents` / `price_initial_cents` / `price_discount_pct`, `release_date` parsed to a real `DATE` (left NULL for the 20.4% with no date, never coerced). Row count unchanged: 140,082 in, 140,082 out.
2. **`02_stage_reviews.sql`** — same NULLIF+CAST pattern on all 10 sentinel-typed columns. `steamspy_score_rank` dropped (99.96% null — a dead column). `review_score_description`'s low-volume buckets (`"N user reviews"`, N=1-9) folded into one `'Not enough user reviews'` label in a new `review_score_bucket` column; the raw text is kept in `review_score_description_raw`. 140,082 in, 140,082 out.
3. **`03_stage_steamspy.sql`** — same NULLIF+CAST pattern. The four playtime columns are **dropped entirely** (confirmed constant 0 across all 140,077 rows — zero variance, not high nullness; kept them would risk a false "engagement" chart off an all-zero column). `owners_range` parsed into `owners_low`/`owners_high`/`owners_mid` (linear midpoint of SteamSpy's bucket — a coarse proxy only; 83.2% of the catalogue sits in the bottom bucket so `owners_mid` resolves to 10,000 for most apps and has weak discriminating power above the bottom bin). `is_self_published` derived as `developer = publisher` (case/whitespace-insensitive). Redundant `languages`/`genres` (comma-joined) columns dropped in favor of `games_stage.languages` and the normalized `genres_long` table. 140,077 in, 140,077 out.
4. **`04_stage_long_tables.sql`** — categories/genres/tags.csv are already normalized long tables in the raw source (one row per app+value pair, not comma-separated strings) — converted to Parquet with a defensive `SELECT DISTINCT` on the natural key and `trim()`. No dedup was actually needed (0 duplicate pairs, confirmed in profile and re-verified here) but the guard costs nothing and protects future re-runs against a source change. Rows unchanged: 522,582 / 353,339 / 1,744,632.
5. **`05_build_fact_games.sql`** — builds `fact_games`. Long tables are pre-aggregated into per-app boolean flags and arrays **before** joining, so no fan-out (3.9x/2.9x/14.8x) reaches the fact table. All derived columns below. 140,082 rows in fact_games (unchanged from games_stage — every LEFT JOIN preserves the base row count by construction).
6. **`06_validate.sql`** — row counts at each stage, referential integrity (0 orphans on every long-table→fact_games check, 0 PK duplicates), join coverage recomputed from the built table (matches the stage-1 profile exactly: categories 95.94%, genres 87.42%, tags 83.88%, reviews 100.00%, steamspy 99.996%), monetisation-model breakdown, and a 5-record spot check (Counter-Strike, Portal, Team Fortress 2, Dota 2, Counter-Strike 2) traced end to end.

## Derived columns in `fact_games`

- **`monetisation_model`** — `'free'` / `'paid'` / `'paid_price_unknown'`, kept as three distinct states per the brief. `free` = 33,661 (24.0%), `paid` = 80,393 (57.4%), `paid_price_unknown` = 26,028 (18.6%). Never treat `paid_price_unknown` as free or impute a price for it.
- **`price_usd`** / **`price_usd_source`** — see "Price normalization" below.
- **`release_year`**, **`release_cohort`**, **`release_year_is_partial_2024`** — cohort year from `release_date`; the 2024 flag is a standing warning that 2024's count is a 10-month total (right-truncated at 2024-10-28, confirmed zero Nov/Dec rows), not comparable to a full prior year without saying so.
- **`is_demo`** / **`app_type`** — 122,191 `game` / 17,891 `demo` (12.8%). Any catalogue-level investment analysis should normally filter `is_demo = false`; demos are kept, not dropped, so that decision stays with the analyst.
- **`is_indie`** — true if `genres_long` contains `'Indie'` for that app; **NULL** (not false) for the small number of apps whose only genre rows are non-English (see hazard below).
- **`is_self_published`** — `developer = publisher` from SteamSpy data, used as the closest available proxy for "unbacked/self-published" vs "has a distinct publisher" — **this dataset has no real Xbox first-/third-party field**, so this is an analogy, not a factual first/third-party classification (see DECISIONS.md).
- **`has_singleplayer`, `has_multiplayer`, `has_coop`, `has_controller_support`, `has_vr`, `game_mode`** — derived from `categories_long`, pre-aggregated per app. See localization hazard below for a documented gap.
- **`owners_low` / `owners_high` / `owners_mid`** — linear midpoint of SteamSpy's bucketed ownership range. Explicitly a coarse order-of-magnitude proxy, not a count.
- **`n_categories` / `n_genres` / `n_tags`** and the full `categories` / `genres` / `tags` arrays — carried on the fact table for convenience; genre/tag-level analysis should still use the long tables directly to avoid re-deriving fan-out logic.
- **`review_positive_ratio`** — `review_positive / review_total`, NULL when `review_total` is 0 or missing.

## Price normalization — the decision that most constrains price analysis

**Not flagged in the stage-1 profile:** `games.csv`'s `price_overview` is priced in the **storefront's local currency**, not USD. Distribution across the 76,321 rows with a resolvable currency: EUR 75,623 (99.1%), USD 482, plus a long tail of ~28 other currencies (GBP, RUB, BRL, KRW, JPY, MXN, ...) at single- or double-digit counts each. Treating the raw cents value as USD-cents outright — the naive reading — would have understated "average price" by roughly the EUR/USD gap for 99% of priced rows.

Resolution, in `05_build_fact_games.sql`:
1. **Primary source: `steamspy_insights.price`**, which is already USD cents (verified: app_id 10 Counter-Strike = 999 = $9.99, matching its known USD price). Covers 90,890 of 140,082 rows (64.9%).
2. **Fallback: `games.csv`'s `price_overview`**, converted to USD using a **static, approximate, single-point-in-time (~Dec 2024) FX table** hardcoded in the script for the ~30 observed currencies. Used only for the 819 rows where steamspy has no price but games.csv does.
3. Combined coverage: 91,709 of 140,082 rows (65.5%) — better than either source alone, but still 24.5% of nominally-paid titles (26,028 of 106,421) have **no price data from either source**. These are `paid_price_unknown`, not zero and not imputed.

**This constrains the analysis:** aggregate USD price statistics are reliable for the ~91.7k priced rows (EUR+USD alone are 99.3% of the FX-converted portion, so the approximation error is small in aggregate) but the FX table is not a live/audited feed — do not use it for currency-sensitive or time-sensitive pricing claims, and do not extrapolate price statistics to the `paid_price_unknown` quarter of paid titles.

## New hazard found in this stage, not in the stage-1 profile: category/genre localization

`categories.csv` (and, more weakly, `genres.csv`) record category/genre values in **whatever locale Steam's API happened to return for that app**, not uniformly in English. Measured: 795 of 522,582 category rows (0.15%, spanning 154 of 315 distinct strings) and 303 of 353,339 genre rows (0.09%) are non-ASCII translations of the same underlying ~40-50 canonical category/genre types (e.g. Russian `Кооператив` = "Co-op", Polish `Wieloosobowa` = "Multiplayer"). `tags.csv` was checked and has zero non-ASCII rows.

This was caught by the mandated 5-record spot check, not by aggregate profiling: **Dota 2 (app_id 570) and Counter-Strike 2 (app_id 730)** — two of the most famous titles in the catalogue — both had their category metadata captured in Russian and Polish respectively. A naive English-string match would have silently reported Dota 2 as having no multiplayer/co-op category at all.

Fix applied: `has_multiplayer` / `has_singleplayer` / `has_coop` / `has_controller_support` / `has_vr` / `is_indie` resolve to **NULL (unknown)**, not `false`, for the 53 apps (of 134,393 with categories, 0.04%) whose category rows are *entirely* non-ASCII, and `game_mode` gets an explicit `'unknown_non_english_metadata'` bucket (53 rows) rather than being folded into `single_player_only`.

**Residual, documented limitation:** the ASCII-character heuristic only catches non-Latin scripts (Cyrillic, CJK, Greek, ...). A Latin-alphabet localization that happens to render in pure ASCII — e.g. Polish `Wieloosobowa` ("multiplayer") — is not caught, and Counter-Strike 2's own category list is a live example (`Wieloosobowa` is present but doesn't match the English `'Multi-player'` string, so its `has_multiplayer` flag is `false`, not `true` — visible directly in the 5-record spot check output). **The multiplayer/co-op/controller/VR/indie flags should be read as a floor, not an exact count**: true prevalence is at or above what the flags show, and the gap is small in aggregate (well under 1% of the catalogue based on measured non-ASCII row rates) but can land on any individual app, including major ones, essentially at random.

## Validation summary (full output in `06_validate.sql` run log)

- Row counts: games_stage 140,082 → fact_games 140,082 (no row lost or gained at any stage).
- Referential integrity: 0 orphaned app_ids from any long table into fact_games; 0 duplicate app_ids in fact_games.
- Join coverage recomputed from the built table matches the stage-1 profile exactly (categories 95.94%, genres 87.42%, tags 83.88%, reviews 100.00%, steamspy 99.996%).
- 5-record spot check (Counter-Strike, Portal, Team Fortress 2, Dota 2, Counter-Strike 2) traced end to end through every derived column — this is what surfaced the localization hazard above.
- Idempotency: full pipeline re-run from scratch twice produces byte-identical Parquet files (md5sum-verified on all 7 output files).
