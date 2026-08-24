-- 01_stage_games.sql
-- Convert games.csv (the canonical 140,082-app universe) to a typed, cleaned
-- Parquet staging table. Sentinel handling and JSON extraction happen here,
-- once, so nothing downstream ever re-reads the raw CSV or re-guesses types.
--
-- Hazards addressed (see artifacts/01_profile.json):
--  * backslash-escaped JSON in price_overview -> read with DuckDB's default
--    read_csv (auto-detects escape='\'), never a naive Python parser.
--  * '\N' sentinel -> NULLIF before every CAST; cannot combine nullstr='\N'
--    with escape='\' in one read_csv call (DuckDB Binder Error), so this is
--    done post-read in SQL.
--  * price_overview is multi-currency (EUR dominates at 99.1% of priced
--    rows, long tail of ~30 other currencies) -- NOT already USD. Extracted
--    here as currency + cents; USD conversion happens in 05 using a static
--    FX table (see DECISIONS.md for the rate list and its limitations).
--  * release_date is right-truncated at 2024-10-28 and missing ('\N') for
--    20.4% of rows -- parsed to a real DATE, left NULL when unknown, never
--    silently coerced to a fake date.

SET memory_limit = '4GB';
SET temp_directory = '/home/claude/run_2026-08-22/duck_tmp';
SET preserve_insertion_order = false;

CREATE OR REPLACE TABLE games_stage AS
WITH raw AS (
    SELECT *
    FROM read_csv(
        '/mnt/user-data/uploads/Gainz-for-XBox/data/raw/super raw/games.csv',
        header = true,
        sample_size = -1
    )
),
cleaned AS (
    SELECT
        app_id,
        NULLIF(name, '\N')                                  AS name,
        TRY_CAST(NULLIF(release_date, '\N') AS DATE)         AS release_date,
        (is_free = 1)                                        AS is_free,
        NULLIF(price_overview, '\N')                         AS price_overview_json,
        json_extract_string(NULLIF(price_overview, '\N'), '$.currency')      AS price_currency,
        TRY_CAST(json_extract(NULLIF(price_overview, '\N'), '$.final') AS BIGINT)    AS price_final_cents,
        TRY_CAST(json_extract(NULLIF(price_overview, '\N'), '$.initial') AS BIGINT)  AS price_initial_cents,
        TRY_CAST(json_extract(NULLIF(price_overview, '\N'), '$.discount_percent') AS INTEGER) AS price_discount_pct,
        NULLIF(languages, '\N')                              AS languages,
        type                                                  AS app_type,
        (type = 'demo')                                       AS is_demo
    FROM raw
)
SELECT * FROM cleaned;

-- Sanity: app_id must remain a 1:1 primary key after cleaning.
-- (checked properly in 06_validate.sql; this is a fail-fast guard)
SELECT
    CASE WHEN count(*) = count(DISTINCT app_id) THEN 'OK: app_id unique in games_stage'
         ELSE 'FAIL: app_id not unique in games_stage' END AS pk_check
FROM games_stage;

-- ORDER BY makes the output byte-identical across reruns despite
-- preserve_insertion_order=false (which otherwise lets parallel operators
-- emit rows in a nondeterministic order).
COPY (SELECT * FROM games_stage ORDER BY app_id)
    TO '/home/claude/run_2026-08-22/parquet/games_stage.parquet'
    (FORMAT PARQUET, COMPRESSION ZSTD);
